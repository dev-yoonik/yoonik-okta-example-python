import json
from urllib.parse import urlparse, urljoin


class Configuration:

    def __init__(self, config_file="./client_secrets.json"):
        """
        :param config_file: path to configuration file
        """
        self.__load_configuration(self.__read_file(config_file))

    def __load_configuration(self, config: dict):
        """
        Maps configuration data to class objects
        :param config: configuration data
        :return:
        """
        if self.__validate_uri(config["oidc_base_uri"]):
            self.__oidc_base_url = config["oidc_base_uri"]

        self.__provider_name = self.__get_provider_name(self.__oidc_base_url)

        if "issuer_uri" in config:
            issuer = config["issuer_uri"]
            if issuer is not None and issuer.__len__():
                if self.__validate_uri(issuer):
                    self.__issuer_uri = issuer
            else:
                self.__issuer_uri = self.__oidc_base_url

        self.__auth_uri = self.__get_absolute_uri(config["auth_uri"])
        self.__token_uri = self.__get_absolute_uri(config["token_uri"])
        if "token_validation_uri" in config and config["token_validation_uri"] is not None:
            self.__token_validation_uri = self.__get_absolute_uri(config["token_validation_uri"])

        self.__user_info_uri = self.__get_absolute_uri(config["userinfo_uri"])
        self.__redirect_uri = config["redirect_uri"]
        self.__client_id = config["client_id"]
        self.__client_secret = config["client_secret"]
        self.__yk_authentication_uri = config["yoonik_authentication_api_uri"]
        self.__yk_authentication_key = config["yoonik_authentication_api_key"]

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
        hostname = urlparse(url).hostname.split('.')[-2]
        if hostname:
            if "okta" in hostname:
                return "Okta"
            elif "onelogin" in hostname:
                return "OneLogin"
        raise Exception(f"Not supported hostname '{hostname}'.")

    @staticmethod
    def __validate_uri(uri: str) -> bool:
        try:
            result = urlparse(uri)
            return all([result.scheme, result.netloc])
        except:
            raise Exception(f"Bad uri. {uri}")

    @property
    def provider_name(self):
        return self.__provider_name

    @property
    def issuer_uri(self):
        return self.__issuer_uri

    @property
    def auth_uri(self):
        return self.__auth_uri

    @property
    def token_uri(self):
        return self.__token_uri

    @property
    def token_validation_uri(self):
        return self.__token_validation_uri

    @property
    def user_info_uri(self):
        return self.__user_info_uri

    @property
    def redirect_uri(self):
        return self.__redirect_uri

    @property
    def client_id(self):
        return self.__client_id

    @property
    def client_secret(self):
        return self.__client_secret

    @property
    def yk_authentication_uri(self):
        return self.__yk_authentication_uri

    @property
    def yk_authentication_key(self):
        return self.__yk_authentication_key
