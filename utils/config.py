""" Configuration to load the json config file """
from yk_utils.files import read_json_from_file
from yk_utils.objects import get_url_domain, get_url, is_valid_url
from utils.exceptions import ProviderNotSupported


class Configuration:
    """ Configuration Class """

    def __init__(self, config_file="./config.json"):
        """
        :param config_file: path to configuration file
        """
        self.__load(read_json_from_file(config_file))

    def __load(self, config: dict):
        """
        Maps configuration data to class objects
        :param config: configuration data
        :return:
        """
        self.oidc_base_url = get_url(config["oidc_base_url"])

        domain = get_url_domain(self.oidc_base_url).lower()
        if domain in ('okta', 'onelogin'):
            self.provider_name = domain
        else:
            raise ProviderNotSupported(f"Provider '{domain}' is not supported.")

        self.auth_url = get_url(self.oidc_base_url, config["auth_url"])
        self.token_url = get_url(self.oidc_base_url, config["token_url"])
        self.user_info_url = get_url(self.oidc_base_url, config["userinfo_url"])

        self.redirect_url = get_url(config["redirect_url"])

        self.client_id = config["client_id"]
        self.client_secret = config["client_secret"]

        self.yk_authentication_url = get_url(config["yoonik_authentication_api_url"])
        self.yk_authentication_key = config["yoonik_authentication_api_key"]

        issuer = config["issuer_url"]
        if issuer:
            if not is_valid_url(issuer):
                # its a relative url
                issuer = get_url(self.oidc_base_url, issuer)

        else:
            issuer = self.oidc_base_url
        self.issuer_url = issuer

        if "token_validation_url" in config and config["token_validation_url"]:
            self.token_validation_url = \
                get_url(self.oidc_base_url, config["token_validation_url"])
        else:
            self.token_validation_url = None
