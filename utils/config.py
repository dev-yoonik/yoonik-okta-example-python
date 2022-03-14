""" Configuration to load the json config file """
from yk_utils.files import read_json_from_file
from yk_utils.web import get_url_hostname, build_url, is_valid_url
from utils.exceptions import ProviderNotSupported


class Configuration:
    """ Configuration Class """

    def __init__(self, config_file: str = "./config.json"):
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
        self.oidc_base_url = build_url(config["oidc_base_url"])

        hostname = get_url_hostname(self.oidc_base_url).lower()
        if '.okta.' in hostname:
            hostname = "Okta"
        elif '.onelogin.' in hostname:
            hostname = "OneLogin"
        else:
            raise ProviderNotSupported(f"Provider '{hostname}' is not supported.")
        self.provider_name = hostname

        self.auth_url = build_url(self.oidc_base_url, config["auth_url"])
        self.token_url = build_url(self.oidc_base_url, config["token_url"])
        self.user_info_url = build_url(self.oidc_base_url, config["userinfo_url"])

        self.redirect_url = build_url(config["redirect_url"])

        self.client_id = config["client_id"]
        self.client_secret = config["client_secret"]

        self.yk_authentication_url = build_url(config["yoonik_authentication_api_url"])
        self.yk_authentication_key = config["yoonik_authentication_api_key"]

        if "token_validation_url" in config and config["token_validation_url"]:
            self.token_validation_url = \
                build_url(self.oidc_base_url, config["token_validation_url"])
        else:
            self.token_validation_url = None
