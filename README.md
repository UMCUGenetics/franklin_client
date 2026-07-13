# Franklin API Python client

![test](https://github.com/UMCUGenetics/franklin_client/actions/workflows/test.yml/badge.svg)
![lint](https://github.com/UMCUGenetics/franklin_client/actions/workflows/lint.yml/badge.svg)

## Setup application (development) environment

```bash
git clone git@github.com:UMCUGenetics/franklin_client.git
cd franklin_client
uv sync
pre-commit install
```

### Example CLI usage

Add username and password to `config.toml`.

```bash
uv run franklin -h
uv run franklin download_coverage_report <analysis_id>
uv run franklin download_bam <analysis_id>
uv run franklin download_vcf <analysis_id>
```

### Run local pytest

To run pytest locally you need to set the `POSTMAN_FRANKLIN_MOCKUP_URI` environment variable to configure a Postman Franklin mock server.

```bash
# create .env POSTMAN_FRANKLIN_MOCKUP_URI="<uri_to_franklin_mock_server>"
# or
export POSTMAN_FRANKLIN_MOCKUP_URI="<uri_to_franklin_mock_server>"
uv run pytest
```

### Logger

To modify log levels add `log_level = "LEVEL"` to `config.toml`. Default log level is set to INFO.

## Setup package from github

```bash
python3 -m venv venv
source venv/bin/activate
pip install git+https://github.com/UMCUGenetics/franklin_client.git@branchname
```

### Setup from github in your requirements.txt

Add this line to your requirements file. Edit "branchname" if needed. Specific version tags and commits can also be used.

```sh
git+https://github.com/UMCUGenetics/franklin_client.git@branchname#egg=franklin_client
```

## Example package usage

```python
from franklin_client.services import Franklin

franklin = Franklin(
    base_uri='https://api.genoox.com',
    email='your@email.com',
    password='your_password'
)

assays = franklin.get_assay_list()
print(franklin.get_analysis_list(assay_id=assays[0]['id']))
```

## Resources

- [Franklin API Documentation](https://franklin-api-docs.readme.io)
- [Franklin API Documentation (Postman)](https://www.postman.com/genoox-ps/)
- [Postman mock servers](https://learning.postman.com/docs/designing-and-developing-your-api/mocking-data/setting-up-mock/)
