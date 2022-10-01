from typing import Type

import prefect.orion.api.server as orion_server
import pytest
from opentelemetry.instrumentation.asyncpg import AsyncPGInstrumentor
from opentelemetry.instrumentation.fastapi import (
    FastAPIInstrumentor,
    _InstrumentedFastAPI,
)
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

# from opentelemetry.instrumentation.sqlite3 import SQLite3Instrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider

from prefect_opentelemetry.monitors import (
    AsyncPGMonitor,
    FastAPIMonitor,
    SQLAlchemyMonitor,
)


@pytest.mark.parametrize(
    ["instrumentor", "monitor_type", "tracer_provider"],
    [
        (AsyncPGInstrumentor(), AsyncPGMonitor, None),
        (
            AsyncPGInstrumentor(),
            AsyncPGMonitor,
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
        # (SQLite3Instrumentor(), SQLLite3Monitor, None),
        # (
        #     SQLite3Instrumentor(),
        #     SQLLite3Monitor,
        #     TracerProvider(
        #         resource=Resource.create(
        #             {
        #                 "service.name": "Prefect",
        #             }
        #         )
        #     ),
        # ),
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


def test_prefect_fastapi_replaced():
    monitor = FastAPIMonitor()
    monitor.monitor(None)

    assert orion_server.FastAPI == _InstrumentedFastAPI
