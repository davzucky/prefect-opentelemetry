"""
Defines generic monitor that implement standard opentelemetry instrumentor
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

import fastapi
import prefect.orion.api.server as orion_server
from opentelemetry.instrumentation.asyncpg import AsyncPGInstrumentor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

# from opentelemetry.instrumentation.sqlite3 import SQLite3Instrumentor
from opentelemetry.trace import TracerProvider


class BaseOTLPMonitor(ABC):
    """
    Base monitor that can work with any generic OTLP instrumentor

    Args:
        instrumentor: BaseIntrumentor

    """

    @property
    @abstractmethod
    def instrumentor(self) -> BaseInstrumentor:
        """
        Property that return the baseInstrumentor

        Returns:
            Returns the BaseInstrumentor

        """
        ...

    def _monitor(self, tracer_provider: TracerProvider) -> None:
        """
        Allow to run other custom action to enable the monitoring

        Args:
            tracer_provider: Allow to initialize the TracerProvider to set default
                resources
        """
        ...

    def monitor(self, tracer_provider: TracerProvider) -> None:
        """
        Enable the instrumentation of FastAPI

        Args:
            tracer_provider: Allow to initialize the TracerProvider to set default
                resources
        """

        self.instrumentor.instrument(tracer_provider=tracer_provider)
        self._monitor(tracer_provider=tracer_provider)


@dataclass
class AsyncPGMonitor(BaseOTLPMonitor):
    """
    A monitor class that allow to enable AsyncPG instrumentation

    Args:
        _instrumentor: AsyncPGInstrumentor that can be replace for testing

    """

    _instrumentor: BaseInstrumentor = field(
        default_factory=lambda: AsyncPGInstrumentor()
    )

    @property
    def instrumentor(self) -> BaseInstrumentor:
        """
        Gets the base intrumentor
        """
        return self._instrumentor

    def _monitor(self, tracer_provider: TracerProvider) -> None:
        """
        Allow to run other custom action to enable the monitoring

        Args:
            tracer_provider: Allow to initialize the TracerProvider to set default
                resources
        """
        self.instrumentor.capture_parameters = True


@dataclass
class FastAPIMonitor(BaseOTLPMonitor):
    """
    A monitor class that allow to enable FastAPI instrumentation

    Args:
        _instrumentor: FastAPIInstrumentor that can be replace for testing

    """

    _instrumentor: BaseInstrumentor = field(
        default_factory=lambda: FastAPIInstrumentor()
    )

    @property
    def instrumentor(self) -> BaseInstrumentor:
        """
        Gets the base intrumentor
        """
        return self._instrumentor

    def _monitor(self, tracer_provider: TracerProvider) -> None:
        """
        replaced orin server fastapo with the instrumented instance
        """
        if orion_server.FastAPI != fastapi.FastAPI:
            orion_server.FastAPI = fastapi.FastAPI


# @dataclass
# class SQLLite3Monitor(BaseOTLPMonitor):
#     """
#     A monitor class that allow to enable SQLLite instrumentation

#     Args:
#         _instrumentor: SQLite3Instrumentor that can be replace for testing

#     """

#     _instrumentor: BaseInstrumentor = field(
#         default_factory=lambda: SQLite3Instrumentor()
#     )

#     @property
#     def instrumentor(self) -> BaseInstrumentor:
#         """
#         Gets the base intrumentor
#         """
#         return self._instrumentor


@dataclass
class SQLAlchemyMonitor(BaseOTLPMonitor):
    """
    A monitor class that allow to enable SQLAlchemy instrumentation

    Args:
        _instrumentor: SQLAlchemyInstrumentor that can be replace for testing

    """

    _instrumentor: BaseInstrumentor = field(
        default_factory=lambda: SQLAlchemyInstrumentor()
    )

    @property
    def instrumentor(self) -> BaseInstrumentor:
        """
        Gets the base intrumentor
        """
        return self._instrumentor
