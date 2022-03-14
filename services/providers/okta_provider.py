""" Okta OIDC Provider """
import requests
from typing import List
from .provider import Provider
from utils.config import Configuration


class OktaProvider(Provider):
    """ Okta OIDC Provider Class """
    def __init__(self,
                 config: Configuration,
                 app_state: str = 'ApplicationState',
                 nonce: str = 'SampleNonce'):
        """
        Okta Provider Class Initializer
        :param config: Configuration instance
        :param app_state: to protect the user from cross site request forgery(CSRF) attacks
        :param nonce: associate a Client session with an ID Token, and to mitigate replay attacks
        """
        super().__init__(config)
        self.__app_state = app_state
        self.__nonce = nonce

    def get_login_url(self, oidc_scopes: List[str] = None) -> str:
        """
        Builds the initializer url of the authentication code flow.
        :param oidc_scopes: list of oidc scopes
        :return: url
        """
        if oidc_scopes is None:
            oidc_scopes = self._default_scopes

        # get request params
        query_params = {
            'client_id': self._client_id,
            'redirect_uri': self._redirect_url,
            'scope': ' '.join(oidc_scopes),
            'state': self.__app_state,
            'nonce': self.__nonce,
            'response_type': 'code',
            'response_mode': 'query'
        }

        # build request_url
        request_url = f"{self._auth_url}?{requests.compat.urlencode(query_params)}"

        return request_url

    def is_access_token_valid(self, token: str) -> bool:
        """ Intended to perform access token validation """
        return True
