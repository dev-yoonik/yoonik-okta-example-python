""" User Repository and Class """
from flask_login import UserMixin


# Simulate user database
USERS_DB = {}


class User(UserMixin):

    """Custom User class."""

    def __init__(self, id_, name, email):
        self.id = id_
        self.name = name
        self.email = email

    def claims(self):
        """Use this method to render all assigned claims on profile page."""
        return {'name': self.name,
                'email': self.email}.items()

    @staticmethod
    def get(user_id) -> 'User':
        """
        Returns the user with the specified user identifier.
        :param user_id: user identifier
        :return: user
        """
        return USERS_DB.get(user_id)

    @staticmethod
    def create(user_id, name, email):
        """
        Create a new user with the specified id, name and email
        :param user_id: user identifier
        :param name: user name
        :param email: user email
        :return:
        """
        USERS_DB[user_id] = User(user_id, name, email)
