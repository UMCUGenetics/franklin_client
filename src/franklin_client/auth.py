import requests


class FranklinAuth(requests.auth.AuthBase):
    "Franklin API authentication"

    def __init__(self, api_uri, email, password):
        """Construct a new Franklin API client authentication

        :param api_uri: API uri
        :param username: Franklin username
        :param password: Franklin password
        """
        # ToDo: Implement some form of cache for the token
        self.token = requests.get(f'{api_uri}/auth/login', params={'email': email, 'password': password}).json()['token']

    def __call__(self, r):
        """"Add the Authorization header to the request.

        :param r: The request to add the Authorization header to
        """

        r.headers['Authorization'] = f'Bearer {self.token}'
        return r
