""" Provider Base """
from abc import ABC, abstractmethod
from typing import List, Union
from utils.config import Configuration
import requests


class Provider(ABC):
    """ Provider base class """

    def __init__(self, config: Configuration, default_scopes: List[str] = None):
        """
        OIDC Provider class initializer
        :param config: instance of Configuration
        :param default_scopes: Default OIDC scopes
        """
        if default_scopes is None:
            default_scopes = ["openid", "profile", "email"]
        self._client_id = config.client_id
        self._client_secret = config.client_secret
        self._auth_url = config.auth_url
        self._token_url = config.token_url
        self._user_info_url = config.user_info_url
        self._redirect_url = config.redirect_url
        self._default_scopes = default_scopes

    @abstractmethod
    def is_access_token_valid(self, token: str) -> bool:
        """
        Performs the access token validity.
        :param token: access token
        :return:
        """
        ...

    @abstractmethod
    def get_login_url(self, oidc_scopes: List[str]) -> str:
        """
        Builds the initializer url of the authentication code flow.
        :param oidc_scopes: list of oidc scopes
        :return: url
        """
        ...

    def request_access_token(self, code: str, redirect_url: str) -> Union[str, None]:
        """
        Requests an access token from the providers token endpoint.
        :param code: the code received from the provider
        :param redirect_url: the app redirect url registered in the OIDC provider
        :return: access token
        """
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        query_params = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_url
        }
        query_params = requests.compat.urlencode(query_params)
        response = requests.post(
            self._token_url,
            headers=headers,
            data=query_params,
            auth=(self._client_id, self._client_secret),
        ).json()

        # Get tokens and validate
        if not response.get("token_type") or "access_token" not in response:
            return None

        return response["access_token"]

    def get_user_info(self, token: str) -> Union[dict, None]:
        """
        Requests the user info from the providers user info endpoint.
        :param token: access token
        :return:
        """
        user_info = requests.get(
            self._user_info_url,
            headers={'Authorization': f'Bearer {token}'})
        if not user_info.ok:
            return None
        return user_info.json()
