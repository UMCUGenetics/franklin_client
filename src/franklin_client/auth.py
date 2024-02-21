import requests


class FranklinAuth(requests.auth.AuthBase):
    """Franklin API authentication"""

    def __init__(self, api_uri, email, password):
        """Initialize a new Franklin API client authentication

        Args:
            api_uri (str): Franklin API uri
            email (str): Franklin username
            password (str): Franklin password

        """
        self.token = requests.get(f'{api_uri}/auth/login', params={'email': email, 'password': password}).json()['token']

    def __call__(self, r):
        """Add the Authorization header to the request.

        Args:
            r (requets): The request to add the Authorization header to

        Returns:
            request: The requests with added Authorization header
        """
        r.headers['Authorization'] = f'Bearer {self.token}'
        return r
