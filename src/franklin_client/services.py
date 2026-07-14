from typing import Any

import requests

from franklin_client.logger import logger


class FranklinAuth(requests.auth.AuthBase):
    """Franklin API authentication"""

    def __init__(self, base_uri: str, email: str, password: str, api_version: str = "v1") -> None:
        """Initialize a new Franklin API client authentication

        Args:
            base_uri: Franklin API uri
            email: Franklin username
            password: Franklin password
            api_version: Franklin API version
        """
        response = requests.get(f"{base_uri}/{api_version}/auth/login", params={"email": email, "password": password})

        if response.status_code == 401:
            raise requests.exceptions.HTTPError(response.text)
        else:
            response.raise_for_status()

        self.token = response.json()["token"]

    def __call__(self, request: requests.Request) -> requests.Request:
        """Add the Authorization header to the request.

        Args:
            r: The request to add the Authorization header to

        Returns:
            request: The requests with added Authorization header
        """
        request.headers["Authorization"] = f"Bearer {self.token}"
        return request


class Franklin(object):
    "Franklin API client interface"

    def __init__(self, base_uri: str, email: str, password: str) -> None:
        """Construct a new Franklin API client interface

        Args:
            base_uri: Base uri for the Franklin server_
            email: Franklin username
            password: Franklin password
        """
        self.base_uri = base_uri

        # Authenticate once using the FranklinAuth class
        self.auth = FranklinAuth(self.base_uri, email, password)

    def _get(self, endpoint: str, params: dict[str, Any] | None = None, api_version: str = "v1", **kwargs) -> dict:
        """Get data from the end_point, combining api uri and end_point.

        Args:
            endpoint: Endpoint uri
            params: Get request params. Defaults to None.
            api_version: Franklin API version. Defaults to "v1".

        Returns:
            Return the response as decoded json
        """
        uri = f"{self.base_uri}/{api_version}/{endpoint}"
        response = requests.get(uri, params=params, auth=self.auth, **kwargs)
        logger.debug(f"GET {response.url} - Status code: {response.status_code}")
        logger.debug(f"Response content: {response.text}")
        response.raise_for_status()  # Raise exception on request error
        return response.json()

    def _post(self, endpoint: str, data: dict[str, Any] | None = None, api_version: str = "v1", **kwargs) -> dict:
        """Post data to the end_point, combining api uri and end_point.

        Args:
            endpoint: Endpoint uri
            data: Post request data. Defaults to None.
            api_version: Franklin API version. Defaults to "v1".

        Returns:
            Return the response as decoded json
        """
        uri = f"{self.base_uri}/{api_version}/{endpoint}"
        response = requests.post(uri, json=data, auth=self.auth, **kwargs)
        logger.debug(f"POST {response.url} - Status code: {response.status_code}")
        logger.debug(f"Response content: {response.text}")
        response.raise_for_status()
        return response.json()

    def get_assays(self) -> list:
        """Get a list of all organization assays.

        Returns:
            List of assays

        """
        return self._get(endpoint="assay/list")["assays"]  # Note: Should we return the whole response or just the assays list?

    def get_analyses(
        self,
        analysis_name: str | None = None,
        status: str | None = None,
        created_before: str | None = None,
        created_after: str | None = None,
        assay_id: str | None = None,
    ) -> dict:
        """Get a list of all analyses for each assay

        Args:
            analysis_name: filter by the name of the analysis, will return analysis where name contains the partial string. Defaults to None.
            status: filter by the status of the analysis (active, suspended, resolved or creating). Defaults to None.
            created_before: filter by the date of creation, before (yyyy-MM-dd). Defaults to None.
            created_after: filter by the date of creation, after (yyyy-MM-dd). Defaults to None.
            assay_id: filter by the assay id. Defaults to None.

        Returns:
            Assays dict with their analyses list, key = assay_id, item = list of analysis dicts
        """
        params = {
            "analysis_name": analysis_name,
            "status": status,
            "created_before": created_before,
            "created_after": created_after,
            "assay_id": assay_id,
        }
        return self._get(endpoint="analyses/list_detailed", params=params)["analyses"]

    def get_analysis(self, analysis_id: str) -> list:
        """Get the analysis by id

        Args:
            analysis_id: Analysis id

        Returns:
            List of analysis dicts

        """
        return self._get(endpoint="analysis", params={"analysis_id": [analysis_id]})

    def get_analysis_qc_metrics(self, analysis_id: str) -> dict:
        """Get the qc metrics for an analysis

        Args:
            analysis_id (str): analysis id

        Returns:
            QC metrics dict for the analysis
        """
        return self._get(endpoint="analysis/qc_metrics", params={"analysis_id": analysis_id})

    def get_analysis_report(self, analysis_id: str) -> dict | None:
        """Get the analysis report for an analysis

        Args:
            analysis_id: analysis id

        Returns:
            Dict with analysis report or None if no report found
        """
        try:
            analysis_report = self._get(endpoint="analysis/report", params={"analysis_id": analysis_id})
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 400:  # Franklin api returns status code 400 if no report found
                return None
            else:
                raise
        else:
            return analysis_report

    def get_analysis_signed_report_file(self, analysis_id: str, format: str = "pdf") -> dict:
        # Todo: Check the correct return type
        """Get the signed report file for an analysis.

        Args:
            analysis_id: analysis id
            format: report format (pdf, docx). Defaults to 'pdf'.

        Returns:
            Dict with signed report file AWS location
        """
        return self._get(endpoint="analysis/signed_report_file", params={"analysis_id": analysis_id, "format": format})

    def get_analysis_vcf(self, analysis_id: str) -> dict:
        """Get the vcf file for an analysis

        Args:
            analysis_id: analysis id

        Returns:
            dict: key = vcf_type, item = list of vcf file AWS locations
        """
        return self._get(endpoint="analysis/vcf_location", params={"analysis_id": analysis_id})

    def get_analysis_bam(self, analysis_id: str) -> dict:
        """Get the bam file for an analysis

        Args:
            analysis_id: analysis id

        Returns:
            Dictonary with file types as keys and list of file AWS locations as values
        """
        return self._get(endpoint="analysis/bam_location", params={"analysis_id": analysis_id})

    def get_analysis_coverage_report(
        self,
        analysis_id: str,
        coverage_type: str = "genes",
        coverage_region: str = "coding",
        virtual_panel_ids: list[str] = [],
    ) -> dict:
        """Get the coverage report for an analysis

        Args:
            analysis_id: analysis id
            coverage_type: coverage type (genes, exons, kit). Defaults to "genes".
            coverage_region: coverage region (coding, targeted). Defaults to "coding".
            virtual_panel_ids (list[str], optional): An list of virtual panel IDs to filter the CSV by specific virtual panels.

        Returns:
            Dict with coverage report AWS location
        """
        return self._post(
            endpoint="analysis/export/coverage_csv",
            data={
                "analysis_id": analysis_id,
                "coverage_type": coverage_type,
                "coverage_region": coverage_region,
                "virtual_panel_ids": virtual_panel_ids,
            },
        )

    def get_analysis_variants(self, variant_type: str, analysis_id: str) -> list:
        """Get the variants for an analysis

        Args:
            variant_type: variant type (snp, sv)
            analysis_id: analysis id

        Returns:
            List of variants
        """
        if variant_type not in ["snp", "sv"]:
            raise ValueError(f"Invalid variant type: {variant_type}")

        return self._get(endpoint=f"analysis/variants/{variant_type}", params={"analysis_id": analysis_id}, api_version="v2")[
            "variants"
        ]

    def get_analysis_workbench_variants(self, analysis_id: str) -> list:
        """Get variants from an analysis workbench (variants selected for review).

        Args:
            analysis_id: analysis id

        Returns:
            List of workbench variants
        """

        return self._get(endpoint="analysis/workbench", params={"analysis_id": analysis_id}, api_version="v1_2")

    def get_variant_org_assessments(self, variants: list[dict[str, Any]]) -> list:
        """Get the organization assessments (classification) for a list of variants

        Args:
            variants: list of variants
                [
                    {"chromosome": "chr..", "position": 123, "reference": "..", "alternative": "..", "reference_version": "HG38"},
                    ...
                ]
        Returns:
            List of variant assessments
        """
        return self._post(endpoint="variant/org_assessments", data={"variants": variants})["variants_assessments"]

    def search_variant(self, search_text: str) -> dict:  # Todo: Check if this is the correct name -> variant_search?
        """Search for a variant by text

        Args:
            search_text: String that represents a variant in a variety of nomenclatures (c.Dot, p.Dot, chrom position etc.)

        Returns:
            Dict of variant annotation
        """
        return self._get(endpoint="variant/search", params={"search_text": search_text})["variant_options"]
