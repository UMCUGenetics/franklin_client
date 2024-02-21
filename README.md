# Franklin API Python client

![python-package](https://github.com/UMCUGenetics/franklin_client/actions/workflows/python-package.yml/badge.svg)

## Setup from github

```bash
python3 -m venv venv
source venv/bin/activate
pip install git+https://github.com/UMCUGenetics/franklin_client.git@branchname
```

## Setup from github in your requirements.txt

Add this line to your requirements file. Edit "branchname" if needed. Specific version tags and commits can also be used.

```
git+https://github.com/UMCUGenetics/franklin_client.git@branchname#egg=franklin_client
```

## Setup local development environment

```bash
git clone git@github.com:UMCUGenetics/franklin_client.git
cd franklin_client
python3 -m venv venv
source venv/bin/activate
pip install -e .[dev]  # Development environment including flake8 and pytest
```

### Run local pytest

To run pytest locally you need to set the `POSTMAN_FRANKLIN_MOCKUP_URI` environment variable to configure a Postman Franklin mock server.

```bash
export POSTMAN_FRANKLIN_MOCKUP_URI=<uri_to_franklin_mock_server>
pytest .
```

## Example package usage

```python
import franklin_client

franklin = franklin_client.Franklin(
    base_uri='https://api.genoox.com',
    email='your@email.com',
    password='your_password'
)

assays = franklin.get_assay_list()
print(franklin.get_analysis_list(assay_id=assays[0]['id']))
```

## Example CLI usage

```bash
source venv/bin/activate

franklin -h
franklin download_bam <base_uri> <email> <password> <analysis_id>
franklin download_vcf <base_uri> <email> <password> <analysis_id>
```

## Resources

- [Franklin API Documentation (Postman)](https://www.postman.com/genoox-ps/)
- [Postman mock servers](https://learning.postman.com/docs/designing-and-developing-your-api/mocking-data/setting-up-mock/)
