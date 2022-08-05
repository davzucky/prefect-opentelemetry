import prefect
import pytest
from fastapi import status
from fastapi.testclient import TestClient
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
from prefect.orion.api.server import create_app

from prefect_opentelemetry.server import create_app_with_OTLP, default_trace_provider


@pytest.fixture(scope="module")
def prefect_ephemeral_app():
    def get_app():
        return create_app(ephemeral=True)

    return get_app


@pytest.fixture(scope="module")
def in_memory_exporter():
    return InMemorySpanExporter()


@pytest.fixture(scope="module")
def in_memory_tracer_provider(in_memory_exporter):
    return default_trace_provider(exporter=in_memory_exporter)


@pytest.fixture(scope="module")
def client(prefect_ephemeral_app, in_memory_tracer_provider):
    app = create_app_with_OTLP(
        fastapi_factory=prefect_ephemeral_app, tracer_provider=in_memory_tracer_provider
    )
    with TestClient(app) as test_client:
        yield test_client


def test_call_version_check_spans(
    client: TestClient,
    in_memory_tracer_provider: TracerProvider,
    in_memory_exporter: InMemorySpanExporter,
):
    in_memory_tracer_provider.force_flush(10)
    spans = in_memory_exporter.get_finished_spans()

    in_memory_exporter.clear()
    response = client.get("/api/admin/version")

    in_memory_tracer_provider.force_flush(10)
    spans = in_memory_exporter.get_finished_spans()

    assert response.status_code == status.HTTP_200_OK
    assert prefect.__version__
    assert prefect.__version__ == response.json()
    assert len(spans) == 6


def test_call_create_flows(
    client: TestClient,
    in_memory_tracer_provider: TracerProvider,
    in_memory_exporter: InMemorySpanExporter,
):
    in_memory_tracer_provider.force_flush(10)
    in_memory_exporter.clear()

    flow_data = {"name": "my-flow"}
    response = client.post(
        "/api/flows/", json=flow_data, headers={"traceID": "1234", "spanID": "1234"}
    )

    in_memory_tracer_provider.force_flush(10)
    spans_after = in_memory_exporter.get_finished_spans()

    assert response.json()["name"] == "my-flow"
    assert response.status_code == status.HTTP_201_CREATED
    assert len(spans_after) == 13
