from flask_login import UserMixin


# Simulate user database
USERS_DB = {}


class User(UserMixin):

    """Custom User class."""

    def __init__(self, id_, name, email, yk_authentication_status):
        self.id = id_
        self.name = name
        self.email = email
        self.yk_authentication_status = yk_authentication_status

    def claims(self):
        """Use this method to render all assigned claims on profile page."""
        return {'name': self.name,
                'email': self.email,
                'YooniK Face Authentication Status': self.yk_authentication_status}.items()

    @staticmethod
    def get(user_id):
        return USERS_DB.get(user_id)

    @staticmethod
    def create(user_id, name, email, yk_authentication_status):
        USERS_DB[user_id] = User(user_id, name, email, yk_authentication_status)
