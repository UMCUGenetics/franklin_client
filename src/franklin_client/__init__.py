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
        """Get data from the end_point, combining api uri and end_point. Return the response as decoded json

        :param end_point: end point to get data from
        :param params: Optional params dict

        """
        uri = f'{self.api_uri}/{endpoint}'
        response = requests.get(uri, params=params, auth=self.auth, **kwargs)
        response.raise_for_status()  # Raise exception on request error
        return response.json()

    def _post(self, endpoint, data=None, **kwargs):
        """Post data to the end_point, combining api uri and end_point. Return the response as decoded json

        :param end_point: end point to post data to
        :param data: Optional dictionary, list of tuples, bytes, or file-like object
        """
        uri = f'{self.api_uri}/{endpoint}'
        response = requests.post(uri, json=data, auth=self.auth, **kwargs)
        response.raise_for_status()
        return response.json()

    def get_assay_list(self):
        """Get a list of all organization assays."""
        return self._get(endpoint='assay/list')['assays']  # Note: Should we return the whole response or just the assays list?

    # def create_analysis_bulk()

    # def create_analysis_shell_case()

    def get_analysis_list(self, analysis_name=None, status=None, created_before=None, created_after=None, assay_id=None):
        """Get a list of all analyses for each assay

        :param analysis_name: Optional filter by the name of the analysis,
            will return analysis where name contains the partial string
        :param status: Optional filter by the status of the analysis (active, suspended, resolved or creating)
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

    def get_analysis_status(self, analysis_ids):
        """Get the status of analysis by ids.

        :param analysis_ids: List of analysis ids
        """
        return self._post(endpoint='analyses/status', data={'analysis_ids': analysis_ids})

    def get_analysis_qc_metrics(self, analysis_id):
        """Get the qc metrics for an analysis

        :param analysis_id: analysis id
        """
        return self._get(endpoint='analysis/qc_metrics', params={'analysis_id': analysis_id})

    def get_analysis_report(self, analysis_id):
        """Get the analysis report for an analysis

        :param analysis_id: analysis id
        """
        try:
            analysis_report = self._get(endpoint='analysis/report', params={'analysis_id': analysis_id})
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 400:  # Franklin api returns status code 400 if no report found
                return None
            else:
                raise
        else:
            return analysis_report

    def get_analysis_signed_report_file(self, analysis_id, format='pdf'):
        """Get the signed report file for an analysis."""
        return self._get(endpoint='analysis/signed_report_file', params={'analysis_id': analysis_id, 'format': format})

    def get_analysis_vcf(self, analysis_id):
        """Get the vcf file for an analysis

        :param analysis_id: analysis id
        """
        return self._get(endpoint='analysis/vcf_location', params={'analysis_id': analysis_id})

    def get_analysis_bam(self, analysis_id):
        """Get the bam file for an analysis

        :param analysis_id: analysis id
        """
        return self._get(endpoint='analysis/bam_location', params={'analysis_id': analysis_id})

    def get_analysis_variants(self, variant_type, analysis_id):
        """Get the variants for an analysis

        :param variant_type: variant type (snp, sv)
        :param analysis_id: analysis id
        """
        if variant_type not in ['snp', 'sv']:
            raise ValueError(f'Invalid variant type: {variant_type}')

        return self._get(endpoint=f'analysis/variants/{variant_type}', params={'analysis_id': analysis_id})

    def get_variant_org_assessments(self, variants):
        """Get the organization assessments (classification) for a list of variants

        :param variants: list of variants
            [{"chromosome": "chr..", "position": 123, "reference": "..", "alternative": "..", "reference_version": "HG38"}, ...]
        """
        return self._post(endpoint='variant/org_assessments', data={'variants': variants})

    def get_variant(self, search_text):  # Todo: Check if this is the correct name -> variant_search?
        """Search for a variant by text

        :param search_text: String that represents a variant in a variety of nomenclatures (c.Dot, p.Dot, chrom position etc.)
        """
        return self._get(endpoint='variant/search', params={'search_text': search_text})

    def parse_variant(self, search_text_input):  # Todo Check if this is the correct name -> parse_search?
        """Search for a variant by text

        :param search_text_input: String that represents a variant in a variety of nomenclatures (c.Dot, p.Dot, chrom position etc.)
        """
        return self._post(endpoint='parse_search', data={'search_text_input': search_text_input})