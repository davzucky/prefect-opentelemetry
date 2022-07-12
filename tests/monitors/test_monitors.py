from typing import Type

import pytest
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.instrumentation.sqlite3 import SQLite3Instrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider

from prefect_opentelemetry.monitors import (
    FastAPIMonitor,
    SQLAlchemyMonitor,
    SQLLite3Monitor,
)


@pytest.mark.parametrize(
    ["instrumentor", "monitor_type", "tracer_provider"],
    [
        (SQLAlchemyInstrumentor(), SQLAlchemyMonitor, None),
        (
            SQLAlchemyInstrumentor(),
            SQLAlchemyMonitor,
            TracerProvider(
                resource=Resource.create(
                    {
                        "service.name": "Prefect",
                    }
                )
            ),
        ),
        (FastAPIInstrumentor(), FastAPIMonitor, None),
        (
            FastAPIInstrumentor(),
            FastAPIMonitor,
            TracerProvider(
                resource=Resource.create(
                    {
                        "service.name": "Prefect",
                    }
                )
            ),
        ),
        (SQLite3Instrumentor(), SQLLite3Monitor, None),
        (
            SQLite3Instrumentor(),
            SQLLite3Monitor,
            TracerProvider(
                resource=Resource.create(
                    {
                        "service.name": "Prefect",
                    }
                )
            ),
        ),
    ],
)
def test_call_call_intrument_with_provider(
    mocker,
    instrumentor: BaseInstrumentor,
    monitor_type: Type,
    tracer_provider: TracerProvider,
):
    spy = mocker.spy(instrumentor, "instrument")
    monitor = monitor_type(_instrumentor=instrumentor)

    monitor.monitor(tracer_provider=tracer_provider)

    assert spy.call_count == 1
    spy.assert_called_with(tracer_provider=tracer_provider)
