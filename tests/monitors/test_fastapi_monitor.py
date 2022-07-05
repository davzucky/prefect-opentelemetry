import pytest
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider

from prefect_opentelemetry.monitors import fastapi_monitoring


@pytest.mark.parametrize(
    "tracer_provider",
    [
        (None),
        (
            TracerProvider(
                resource=Resource.create(
                    {
                        "service.name": "Prefect",
                    }
                )
            )
        ),
    ],
)
def test_call_fast_api_instrumentor_once_with_app(
    mocker, tracer_provider: TracerProvider
):
    instrumentor = FastAPIInstrumentor()
    spy = mocker.spy(instrumentor, "instrument")

    monitor = fastapi_monitoring.FastAPIMonitor(instrumentor=instrumentor)
    monitor.monitor(tracer_provider=tracer_provider)

    assert spy.call_count == 1
    spy.assert_called_with(tracer_provider=tracer_provider)
