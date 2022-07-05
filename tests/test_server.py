import prefect
import pytest
from fastapi import status
from fastapi.testclient import TestClient

from prefect_opentelemetry.server import create_prefect_with_opentelemetry


@pytest.fixture
def client():
    app = create_prefect_with_opentelemetry(ephemeral=True)
    test_client = TestClient(app)
    return test_client


def test_factory_return_prefect_app(client):

    response = client.get("/api/admin/version")

    assert response.status_code == status.HTTP_200_OK
    assert prefect.__version__
    assert prefect.__version__ == response.json()
