""" OneLogin OIDC Provider """
import requests
from services.providers import Provider


class OneLoginProvider(Provider):
    """ OneLogin OIDC Provider Class """

    def __init__(self, config):
        """ Initializer """
        super().__init__(config)
        self._token_validation_uri = config.token_validation_uri

    def get_login_uri(self, oidc_scopes=None):
        # get request params
        if oidc_scopes is None:
            oidc_scopes = self._default_scopes

        query_params = {
            'client_id': self._client_id,
            'redirect_uri': self._redirect_uri,
            'scope': ' '.join(oidc_scopes),
            'response_type': 'code',
        }
        # build request_uri
        request_uri = f"{self._auth_uri}?{requests.compat.urlencode(query_params)}"
        return request_uri

    def is_token_valid(self, token):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        query_params = {
            'token': token,
            'token_type_hint': 'access_token'  # optional
        }

        query_params = requests.compat.urlencode(query_params)

        response = requests.post(
            self._token_validation_uri,
            headers=headers,
            data=query_params,
            auth=(self._client_id, self._client_secret)
        ).json()

        return response["active"]
