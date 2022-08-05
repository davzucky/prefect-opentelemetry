"""
Defines the monitor protocol
"""
from typing import Protocol

from opentelemetry.trace import TracerProvider


class Monitor(Protocol):
    """
    Protocol that define a Monitor that allow to enable OpenTelemetry instrumentation

    Args:
        instrumentor: BaseIntrumentor

    """

    def monitor(self, tracer_provider: TracerProvider) -> None:
        """
        Enable the instrumentation of FastAPI

        Args:
            tracer_provider: Allow to initialize the TracerProvider to set default
                resources

        """
        pass
