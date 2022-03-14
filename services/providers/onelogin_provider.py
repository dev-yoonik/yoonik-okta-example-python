""" OneLogin OIDC Provider """
import requests
from services.providers import Provider
from utils.config import Configuration
from typing import List


class OneLoginProvider(Provider):
    """ OneLogin OIDC Provider Class """

    def __init__(self, config: Configuration):
        """
        OneLogin Provider Class Initializer
        :param config: Configuration instance
        """
        super().__init__(config)
        self._token_validation_url = config.token_validation_url

    def get_login_url(self, oidc_scopes: List[str] = None) -> str:
        """
        Builds the initializer url of the authentication code flow.
        :param oidc_scopes: list of specified the oidc scopes
        :return: url
        """
        # get request params
        if oidc_scopes is None:
            oidc_scopes = self._default_scopes

        query_params = {
            'client_id': self._client_id,
            'redirect_uri': self._redirect_url,
            'scope': ' '.join(oidc_scopes),
            'response_type': 'code',
        }
        # build request_url
        request_url = f"{self._auth_url}?{requests.compat.urlencode(query_params)}"
        return request_url

    def is_access_token_valid(self, token: str) -> bool:
        """
        Checks if access token is valid.
        :param token: access token
        :return:
        """
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        query_params = {
            'token': token,
            'token_type_hint': 'access_token'  # optional
        }

        query_params = requests.compat.urlencode(query_params)

        response = requests.post(
            self._token_validation_url,
            headers=headers,
            data=query_params,
            auth=(self._client_id, self._client_secret)
        ).json()

        return response["active"]
