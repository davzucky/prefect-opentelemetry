"""
Defines SQLAlchemy monitor
"""
from dataclasses import dataclass, field

from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.trace import TracerProvider


@dataclass
class SQLAlchemyMonitoring:
    """
    A monitor class that allow to enable SQLAlchemy instrumentation

    Args:
        instrumentor: BaseIntrumentor

    """

    instrumentor: BaseInstrumentor = field(
        default_factory=lambda: SQLAlchemyInstrumentor()
    )

    def monitor(self, tracer_provider: TracerProvider = None) -> None:
        """
        Enable the instrumentation of FastAPI

        Args:
            tracer_provider: Allow to initialize the TracerProvider to set default
                resources

        """
        self.instrumentor.instrument(tracer_provider=tracer_provider)
