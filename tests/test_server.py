import prefect
import pytest
from fastapi import status
from fastapi.testclient import TestClient
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
from prefect.orion.api.server import create_app

from prefect_opentelemetry.server import create_app_with_OTLP, default_trace_provider


@pytest.fixture
def prefect_ephemeral_app():
    def get_app():
        return create_app(ephemeral=True)

    return get_app


@pytest.fixture
def in_memory_exporter():
    return InMemorySpanExporter()


@pytest.fixture
def in_memory_tracer_provider(in_memory_exporter):
    return default_trace_provider(exporter=in_memory_exporter)


@pytest.fixture
def client(prefect_ephemeral_app, in_memory_tracer_provider):
    app = create_app_with_OTLP(
        fastapi_factory=prefect_ephemeral_app, tracer_provider=in_memory_tracer_provider
    )
    test_client = TestClient(app)
    return test_client


def test_factory_return_prefect_app(client):

    response = client.get("/api/admin/version")

    assert response.status_code == status.HTTP_200_OK
    assert prefect.__version__
    assert prefect.__version__ == response.json()
