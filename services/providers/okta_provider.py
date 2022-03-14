""" Okta OIDC Provider """
import asyncio
import requests
from okta_jwt_verifier import IDTokenVerifier
from okta_jwt_verifier import AccessTokenVerifier
from .provider import Provider


class OktaProvider(Provider):
    """ Okta OIDC Provider Class """
    def __init__(self, config, app_state='ApplicationState', nonce='SampleNonce'):
        super().__init__(config)
        self.name = "Okta"
        self.__app_state = app_state
        self.__nonce = nonce

    def get_login_url(self, oidc_scopes=None) -> str:
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

    def is_token_valid(self, token):
        return True
