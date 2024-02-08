# franklin_client

Python package for Franklin API

## Install

```
pip install -e .
pip install -e .[dev]  # Development environment including flake8 and pytest
```

## Test

To test set `POSTMAN_FRANKLIN_MOCKUP_URI` environment variable.

```bash
source POSTMAN_FRANKLIN_MOCKUP_URI=<uri_to_franklin_mock_server>
pytest .
```

## Resources

- [Postman API Documentation](https://www.postman.com/genoox-ps/)
