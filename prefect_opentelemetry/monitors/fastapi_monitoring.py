"""
Defines FastAPI monitor
"""
from dataclasses import dataclass, field

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from opentelemetry.trace import TracerProvider


@dataclass
class FastAPIMonitor:
    """
    A monitor class that allow to enable FastAPI instrumentation

    Args:
        instrumentor: BaseIntrumentor

    """

    instrumentor: BaseInstrumentor = field(
        default_factory=lambda: FastAPIInstrumentor()
    )

    def monitor(self, tracer_provider: TracerProvider = None) -> None:
        """
        Enable the instrumentation of FastAPI

        Args:
            tracer_provider: Allow to initialize the TracerProvider to set default
                resources

        """

        self.instrumentor.instrument(tracer_provider=tracer_provider)
