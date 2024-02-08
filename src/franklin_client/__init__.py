import requests

from .auth import FranklinAuth


class Franklin(object):
    "Franklin API client interface"

    def __init__(self, base_uri, email, password):
        """Construct a new Franklin API client interface

        :param base_uri: Base uri for the Franklin server
        :param email: Franklin email
        :param password: Franklin password
        """
        self.api_version = 'v1'
        self.api_uri = f'{base_uri}/{self.api_version}'

        # Authenticate once using the FranklinAuth class
        self.auth = FranklinAuth(self.api_uri, email, password)

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

    def get_analysis_list(self, analysis_name=None, status=None, created_before=None, created_after=None, assay_id=None):
        """Get a list of all analyses for each assay.

        :param analysis_name: Optional filter by the name of the analysis,
            will return analysis where name contains the partial string
        :param status: Optional filter by the status of the analysis (active\suspended\resolved\creating)
        :param created_before: Optional filter by the date of creation, before (yyyy-MM-dd)
        :param created_after: Optional filter by the date of creation, after (yyyy-MM-dd)
        :param assay_id: Optional filter by the assay id
        """
        params = {
            'analysis_name': analysis_name,
            'status': status,
            'created_before': created_before,
            'created_after': created_after,
            'assay_id': assay_id
        }
        return self._get(endpoint='analyses/list', params=params)['analyses_by_assay']