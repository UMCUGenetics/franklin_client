import requests

from .auth import FranklinAuth


class Franklin(object):
    "Franklin API client interface"

    def __init__(self, base_uri, email, password):
        """Construct a new Franklin API client interface

        Args:
            base_uri (str): Base uri for the Franklin server_
            email (str): Franklin username
            password (str): Franklin password
        """
        self.api_version = 'v1'
        self.api_uri = f'{base_uri}/{self.api_version}'

        # Authenticate once using the FranklinAuth class
        self.auth = FranklinAuth(self.api_uri, email, password)

    def _get(self, endpoint, params=None, **kwargs):
        """Get data from the end_point, combining api uri and end_point.

        Args:
            endpoint (str): Endpoint uri
            params (dict, optional): Get request params. Defaults to None.

        Returns:
            dict: Return the response as decoded json
        """
        uri = f'{self.api_uri}/{endpoint}'
        response = requests.get(uri, params=params, auth=self.auth, **kwargs)
        response.raise_for_status()  # Raise exception on request error
        return response.json()

    def _post(self, endpoint, data=None, **kwargs):
        """Post data to the end_point, combining api uri and end_point.

        Args:
            endpoint (str): Endpoint uri
            data (dict|list of tuples|bytes|file, optional): Post request data. Defaults to None.

        Returns:
            dict: Return the response as decoded json
        """
        uri = f'{self.api_uri}/{endpoint}'
        response = requests.post(uri, json=data, auth=self.auth, **kwargs)
        response.raise_for_status()
        return response.json()

    def get_assay_list(self):
        """Get a list of all organization assays.

        Returns:
            list: List of assays

        """
        return self._get(endpoint='assay/list')['assays']  # Note: Should we return the whole response or just the assays list?

    # def create_analysis_bulk()

    # def create_analysis_shell_case()

    def get_analysis_list(self, analysis_name=None, status=None, created_before=None, created_after=None, assay_id=None):
        """Get a list of all analyses for each assay

        Args:
            analysis_name (str, optional): filter by the name of the analysis,
                will return analysis where name contains the partial string. Defaults to None.
            status (str, optional): filter by the status of the analysis (active, suspended, resolved or creating).
                Defaults to None.
            created_before (str, optional): filter by the date of creation, before (yyyy-MM-dd). Defaults to None.
            created_after (str, optional): filter by the date of creation, after (yyyy-MM-dd). Defaults to None.
            assay_id (str, optional): filter by the assay id. Defaults to None.

        Returns:
            dict: key = assay, item = list of analyses
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

        Args:
            analysis_ids (list): Analysis ids

        Returns:
            list: list of analysis dicts

        """
        return self._post(endpoint='analyses/status', data={'analysis_ids': analysis_ids})

    def get_analysis_qc_metrics(self, analysis_id):
        """Get the qc metrics for an analysis

        Args:
            analysis_id (int): analysis id

        Returns:
            dict: qc metrics
        """
        return self._get(endpoint='analysis/qc_metrics', params={'analysis_id': analysis_id})

    def get_analysis_report(self, analysis_id):
        """Get the analysis report for an analysis

        Args:
            analysis_id (int): analysis id

        Returns:
            dict or None: analysis report
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
        # Todo: Check the correct return type
        """Get the signed report file for an analysis.

        Args:
            analysis_id (int): analysis id
            format (str, optional): report format (pdf, docx). Defaults to 'pdf'.

        Returns:
            dict: signed report file AWS location
        """
        return self._get(endpoint='analysis/signed_report_file', params={'analysis_id': analysis_id, 'format': format})

    def get_analysis_vcf(self, analysis_id):
        """Get the vcf file for an analysis

        Args:
            analysis_id (int): analysis id

        Returns:
            dict: key = vcf_type, item = list of vcf file AWS locations
        """
        return self._get(endpoint='analysis/vcf_location', params={'analysis_id': analysis_id})

    def get_analysis_bam(self, analysis_id):
        """Get the bam file for an analysis

        Args:
            analysis_id (int): analysis id

        Returns:
            dict: key = bam/bai, item = file AWS locations
        """
        return self._get(endpoint='analysis/bam_location', params={'analysis_id': analysis_id})

    def get_analysis_variants(self, variant_type, analysis_id):
        """Get the variants for an analysis

        Args:
            variant_type (str): variant type (snp, sv)
            analysis_id (int): analysis id

        Returns:
            list: list of variants
        """
        if variant_type not in ['snp', 'sv']:
            raise ValueError(f'Invalid variant type: {variant_type}')

        return self._get(endpoint=f'analysis/variants/{variant_type}', params={'analysis_id': analysis_id})['variants']

    def get_variant_org_assessments(self, variants):
        """Get the organization assessments (classification) for a list of variants

        Args:
            variants (list): list of variants
                [
                    {"chromosome": "chr..", "position": 123, "reference": "..", "alternative": "..", "reference_version": "HG38"},
                    ...
                ]
        Returns:
            list: list of variant assessments
        """
        return self._post(endpoint='variant/org_assessments', data={'variants': variants})['variants_assessments']

    def search_variant(self, search_text):  # Todo: Check if this is the correct name -> variant_search?
        """Search for a variant by text

        Args:
            search_text (str): String that represents a variant in a variety of nomenclatures (c.Dot, p.Dot, chrom position etc.)

        Returns:
            dict: dict of variant annotation
        """
        return self._get(endpoint='variant/search', params={'search_text': search_text})['variant_options']
