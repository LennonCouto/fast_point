import pytest
from fastapi.testclient import TestClient

from fast_point.app import app


@pytest.fixture
def client():
    return TestClient(app)
