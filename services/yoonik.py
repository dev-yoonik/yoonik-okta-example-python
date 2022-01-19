import json
import requests


class Yoonik:

    def __init__(self, authentication_uri, authentication_key):
        self.__authentication_uri = authentication_uri
        self.__authentication_key = authentication_key

    def authenticate(self, user_id, user_photo, create_if_new=True):
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
            result = f"{response.text}"

        return response.ok, result

    def delete_account(self, user_id):
        response = requests.delete(
            self.__authentication_uri,
            headers={'x-api-key': self.__authentication_key},
            json={'user_id': user_id}
        )
        return response.ok
