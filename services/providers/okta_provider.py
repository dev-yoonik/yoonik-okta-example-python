import asyncio
import requests
from .provider import Provider
from okta_jwt_verifier import IDTokenVerifier
from okta_jwt_verifier import AccessTokenVerifier


class OktaProvider(Provider):

    def __init__(self, config, app_state='ApplicationState', nonce='SampleNonce'):
        super(OktaProvider, self).__init__(config)
        self.__app_state = app_state
        self.__nonce = nonce

    async def __is_access_token_valid(self, token):
        jwt_verifier = AccessTokenVerifier(issuer=self._issuer_uri, audience='api://default')
        try:
            await jwt_verifier.verify(token)
            return True
        except Exception:
            return False

    async def __is_id_token_valid(self, token, nonce):
        jwt_verifier = IDTokenVerifier(issuer=self._issuer_uri,
                                       client_id=self._client_id,
                                       audience='api://default')
        try:
            await jwt_verifier.verify(token, nonce=nonce)
            return True
        except Exception:
            return False

    def get_login_uri(self) -> str:
        # get request params
        query_params = {'client_id': self._client_id,
                        'redirect_uri': self._redirect_uri,
                        'scope': "openid email profile",
                        'state': self.__app_state,
                        'nonce': self.__nonce,
                        'response_type': 'code',
                        'response_mode': 'query'}

        # build request_uri
        request_uri = "{base_url}?{query_params}".format(
            base_url=self._auth_uri,
            query_params=requests.compat.urlencode(query_params)
        )

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

