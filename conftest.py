import pytest
from rest_framework.test import APIClient
# ! this configures the factory to be used by pytest

pytest_plugins = [
    "tests.factories"
]


@pytest.fixture
def client():
    return APIClient()
