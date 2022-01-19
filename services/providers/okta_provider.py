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
        self.__app_state = app_state
        self.__nonce = nonce

    async def __is_access_token_valid(self, token):
        """
        Verifies the validity of the specified access token.
        :param token: access token to validate
        :return: True if valid, False otherwise.
        """
        jwt_verifier = AccessTokenVerifier(issuer=self._issuer_uri, audience='api://default')
        try:
            await jwt_verifier.verify(token)
            return True
        except Exception:
            return False

    async def __is_id_token_valid(self, token, nonce):
        """
        Verifies the validity of the id token within the access token.
        :param token: access token
        :param nonce: nonce used
        :return: True if valid, False otherwise.
        """
        jwt_verifier = IDTokenVerifier(issuer=self._issuer_uri,
                                       client_id=self._client_id,
                                       audience='api://default')
        try:
            await jwt_verifier.verify(token, nonce=nonce)
            return True
        except Exception:
            return False

    def get_login_uri(self, oidc_scopes=None) -> str:
        if oidc_scopes is None:
            oidc_scopes = self._default_scopes

        # get request params
        query_params = {
            'client_id': self._client_id,
            'redirect_uri': self._redirect_uri,
            'scope': ' '.join(oidc_scopes),
            'state': self.__app_state,
            'nonce': self.__nonce,
            'response_type': 'code',
            'response_mode': 'query'
        }

        # build request_uri
        request_uri = f"{self._auth_uri}?{requests.compat.urlencode(query_params)}"

        return request_uri

    def is_token_valid(self, token):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None
        if loop is None:
            loop = asyncio.new_event_loop()

        access_token_validation = self.__is_access_token_valid(token)
        id_token_validation = self.__is_id_token_valid(token, self.__nonce)
        try:
            loop.run_until_complete(
                asyncio.wait([access_token_validation,
                              id_token_validation]))
            return True
        except Exception:
            return False
        finally:
            loop.close()
