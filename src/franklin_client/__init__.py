import requests

from .auth import FranklinAuth


class Franklin(object):
    "Franklin API client interface"

    def __init__(self, base_uri, username, password):
        """Construct a new Franklin API client interface

        :param base_uri: Base uri for the Franklin server
        :param username: Franklin username
        :param password: Franklin password
        """
        self.api_version = 'v1'
        self.api_uri = f'{base_uri}/{self.api_version}'

        # Authenticate once using the FranklinAuth class
        self.auth = FranklinAuth(self.api_uri, username, password)

    def _get(self, endpoint, params=None, **kwargs):
        """
        Get data from the end_point, combining base_uri, api uri and end_point. Return the response as decoded json

        :param end_point: end point to get data from
        :param params: Optional params dict

        """
        uri = f'{self.api_uri}/{endpoint}'
        response = requests.get(uri, params=params, auth=self.auth, **kwargs)
        response.raise_for_status()  # Raise exception on request error
        return response.json()

    def get_assay_list(self):
        """Get a list of all organization assays."""
        return self._get(endpoint='assay/list')['assays']  # Note: Should we return the whole response or just the assays list?
