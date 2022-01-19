""" Provider Base """
from abc import ABC, abstractmethod
import requests


class Provider(ABC):
    """ Provider base class """

    def __init__(self, config):
        self._name = config.provider_name
        self._client_id = config.client_id
        self._client_secret = config.client_secret
        self._auth_uri = config.auth_uri
        self._issuer_uri = config.issuer_uri
        self._token_uri = config.token_uri
        self._user_info_uri = config.user_info_uri
        self._redirect_uri = config.redirect_uri

        self._default_scopes = ["openid", "profile", "email"]

    @abstractmethod
    def is_token_valid(self, token) -> bool:
        """
        Performs the token validity.
        :param token: access token
        :return:
        """
        ...

    @abstractmethod
    def get_login_uri(self, oidc_scopes) -> str:
        """
        Builds the initializer uri of the authentication code flow.
        :param oidc_scopes: list of specified the oidc scopes
        :return: uri
        """
        ...

    def get_token(self, code, redirect_uri):
        """
        Requests an access token from the providers token endpoint.
        :param code: the code received from the provider
        :param redirect_uri: the redirect uri in which
        :return:
        """
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        query_params = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_uri
        }
        query_params = requests.compat.urlencode(query_params)
        response = requests.post(
            self._token_uri,
            headers=headers,
            data=query_params,
            auth=(self._client_id, self._client_secret),
        ).json()

        # Get tokens and validate
        if not response.get("token_type") or "access_token" not in response:
            return None

        return response["access_token"]

    def get_user_info(self, token):
        """
        Requests the user info from the providers user info endpoint.
        :param token:
        :return:
        """
        user_info = requests.get(
            self._user_info_uri,
            headers={'Authorization': f'Bearer {token}'})
        if not user_info.ok:
            return None
        return user_info.json()

    @property
    def name(self):
        """
        :return: name of the provider
        """
        return self._name
