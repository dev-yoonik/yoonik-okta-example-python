""" YooniK Service """
import json
import requests


class YoonikService:
    """ YooniK Service Class """

    def __init__(self, authentication_uri, authentication_key):
        """
        Initializer of YooniK Service
        :param authentication_uri: the authentication endpoint uri of YooniK Authentication API
        :param authentication_key: the authentication api key of YooniK Authentication API
        """
        self.__authentication_uri = authentication_uri
        self.__authentication_key = authentication_key

    def authenticate(self, user_id, user_photo, create_if_new=True):
        """

        :param user_id: user identifier
        :param user_photo: user photo
        :param create_if_new: create a new user if there's no account of the user at YooniK
        :return: Tuple with True if the HTTP Response Code indicates success and False otherwise.
        Plus, its content (dictionary or string respectively).
        """
        payload = {
            'user_id': user_id,
            'user_photo': user_photo,
            'create_if_new': create_if_new
        }
        response = requests.post(
            self.__authentication_uri,
            headers={'x-api-key': self.__authentication_key},
            json=payload
        )

        if response.ok:
            result = json.loads(response.text)
        else:
            result = response.text

        return response.ok, result

    def delete_account(self, user_id):
        """
        Sends an HTTP request to the YooniK Authentication API to delete the specified user account.
        :param user_id: user identifier
        :return: True if HTTP Response Code indicates success. False, otherwise.
        """
        response = requests.delete(
            self.__authentication_uri,
            headers={'x-api-key': self.__authentication_key},
            json={'user_id': user_id}
        )
        return response.ok
