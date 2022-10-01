"""
Defines the Orion FastAPI app on which we enable opentelemetry
"""
import sys
from typing import Callable

import prefect
from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import (
    PROCESS_RUNTIME_NAME,
    PROCESS_RUNTIME_VERSION,
    SERVICE_NAME,
    SERVICE_VERSION,
    Resource,
)
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, SpanExporter
from prefect.orion.api.server import create_app

from .monitors import Monitor, MultiMonitors
from .monitors.multi_monitors import get_default_prefect_server_monitors

fastapi_factory_creator = Callable[[], FastAPI]


def default_trace_provider(
    exporter: SpanExporter = OTLPSpanExporter(),
) -> TracerProvider:
    """
    Get the deafult trace provider
    """
    provider = TracerProvider(
        resource=Resource.create(
            {
                SERVICE_NAME: "Prefect_Server",
                SERVICE_VERSION: prefect.__version__,
                PROCESS_RUNTIME_NAME: sys.implementation.name,
                PROCESS_RUNTIME_VERSION: sys.implementation.version,
            },
        ),
    )
    processor = BatchSpanProcessor(exporter)
    provider.add_span_processor(processor)

    return provider


def create_app_with_OTLP(
    fastapi_factory: fastapi_factory_creator = create_app,
    tracer_provider: TracerProvider = None,
    monitor: Monitor = None,
) -> FastAPI:
    """
    Create an FastAPI app with opentelemtry enable that includes the Orion API and UI

    Args:
        fastapi_factory: Callable that return the base fastapi app.
        trace_provider: TracerProvider to use to initialize the intrumentation.
        monitor: Monitor used to instrument the application
    """
    tracer_provider = tracer_provider or default_trace_provider()
    monitor = monitor or MultiMonitors(monitors=get_default_prefect_server_monitors())

    trace.set_tracer_provider(tracer_provider)
    monitor.monitor(tracer_provider=tracer_provider)

    app = fastapi_factory()
    # FastAPIInstrumentor.instrument_app(app)
    return app
