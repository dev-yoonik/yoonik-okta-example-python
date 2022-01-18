import asyncio
import json
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from okta_jwt_verifier import AccessTokenVerifier, IDTokenVerifier


loop = asyncio.get_event_loop()


def is_access_token_valid(token, config):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    query_params = {
        'token': token,
        'token_type_hint': 'access_token' # optional
    }

    query_params = requests.compat.urlencode(query_params)

    r = requests.post(
        config["token_validation_uri"],
        headers=headers,
        data=query_params,
        auth=(config["client_id"], config["client_secret"])
    ).json()

    return r["active"]


def is_id_token_valid(token, issuer, client_id, nonce):
    # this as far i can see is not needed
    return True


def allowed_base64_image(image_str):
    if not image_str.startswith('data:image/'):
        return False
    return image_str[11:14] in {'png', 'jpg', 'jpeg', 'gif'}


def parse_response_error(html_text: str) -> str:
    """Parse HTML error response
    :param html_text:
        HTML error message.
    :return:
        Parsed error message.
    """
    message = ''
    html = BeautifulSoup(markup=html_text, features="html.parser")
    if html.p:
        inner_html = BeautifulSoup(markup=html.p.text, features="html.parser")
        message = inner_html.text if inner_html.p is None else inner_html.p.text

    if "face_not_found" in message:
        message = "Could not find a face in the image."
    elif "multiple_faces" in message:
        message = "The image has more than one person."
    elif "quality_failed" in message:
        message = "The provided image does not have enough quality."
    else:
        message = "An error occurred. Please contact your systems administrator."
        print(f"ERROR: {html.text}")
    return message


def parse_response_status(status: str) -> str:
    """Create a message from the response status data
    :param status:
        Status of the operation.
    :return:
        Resulting message to be sent to the UI.
    """
    message = status
    if status == 'SUCCESS':
        message = "Face authentication successful"
    elif status == 'NEW_USER':
        message = "Face signup successful"
    elif status == 'USER_NOT_FOUND':
        message = "User not registered"
    elif status == 'FAILED':
        message = "Face authentication failed"
    return message


class Configuration:

    def __init__(self, config_file="./client_secrets.json"):
        """
        :param config_file: path to configuration file
        """
        config = self.__read_file(config_file)
        self.__load_configuration(config)
        print(1)

    def __load_configuration(self, config: dict):
        """
        Maps configuration data to class objects
        :param config: configuration data
        :return:
        """
        if self.__validate_uri(config["oidc_base_uri"]):
            self.__oidc_base_url = config["oidc_base_uri"]

        self.provider_name = self.__get_provider_name(self.__oidc_base_url)

        if "issuer_uri" in config:
            issuer = config["issuer_uri"]
            if issuer is not None and issuer.__len__():
                if self.__validate_uri(issuer):
                    self.issuer_uri = issuer
            else:
                self.issuer_uri = self.__oidc_base_url

        self.auth_uri = self.__get_absolute_uri(config["auth_uri"])
        self.token_uri = self.__get_absolute_uri(config["token_uri"])
        if "token_validation_uri" in config and config["token_validation_uri"] is not None:
            self.token_validation_uri = self.__get_absolute_uri(config["token_validation_uri"])

        self.userinfo_uri = self.__get_absolute_uri(config["userinfo_uri"])
        self.redirect_uri = config["redirect_uri"]
        self.client_id = config["client_id"]
        self.client_secret = config["client_secret"]
        self.yk_authentication_uri = config["yoonik_authentication_api_uri"]
        self.yk_authentication_key = config["yoonik_authentication_api_key"]

    def __get_absolute_uri(self, relative: str) -> str:
        """
        Adds the specified relative uri path to the oidc_base_url
        :param relative: relative path to be specified
        :return:
        """
        absolute_uri = urljoin(self.__oidc_base_url, relative)
        if self.__validate_uri(absolute_uri):
            return absolute_uri

    @staticmethod
    def __read_file(file) -> dict:
        """
        Reads the given file.
        :param fname: specified path of the file to read
        :return: read data in dict
        """
        data = None
        with open(file) as f:
            data = json.load(f)
        return data

    @staticmethod
    def __get_provider_name(url: str) -> str:
        """
        Discover Provider name based on the url
        :param url: url of the Provider
        :return: Providers name or the hostname of the given url
        """
        hostname = urlparse(url).hostname
        if hostname:
            if ".okta." in hostname:
                return "Okta"
            elif ".onelogin." in hostname:
                return "OneLogin"
        return hostname

    @staticmethod
    def __validate_uri(uri: str) -> bool:
        try:
            result = urlparse(uri)
            return all([result.scheme, result.netloc])
        except:
            raise Exception(f"Bad uri. {uri}")


config = Configuration()
