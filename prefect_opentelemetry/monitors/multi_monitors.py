"""
Define a monitor that allow can manage multiple monitors
"""
from dataclasses import dataclass
from typing import List

from opentelemetry.trace import TracerProvider
from prefect.orion.utilities.database import get_dialect
from prefect.settings import PREFECT_ORION_DATABASE_CONNECTION_URL

from .monitor import Monitor
from .otlp_monitors import AsyncPGMonitor, FastAPIMonitor, SQLAlchemyMonitor


def get_default_prefect_server_monitors() -> List[Monitor]:
    """
    Gets the default list of monitors that we support

    Args:
        monitors: List of the monitor we want to group

    """
    monitors = [FastAPIMonitor(), SQLAlchemyMonitor()]

    # TODO: Disable as this is not working with OTLP
    connection_url = PREFECT_ORION_DATABASE_CONNECTION_URL.value()
    dialect = get_dialect(connection_url)

    if dialect.name == "postgresql":
        monitors.append(AsyncPGMonitor())
    # elif dialect.name == "sqlite":
    # monitors.append(SQLLite3Monitor())

    return monitors


@dataclass
class MultiMonitors:
    """
    Monitor that allow to aggregate multiple monitor together

    Args:
        monitors: List of the monitor we want to group

    """

    monitors: List[Monitor]

    def monitor(self, tracer_provider: TracerProvider = None) -> None:
        """
        Call monitor on all the monitors

        Args:
            tracer_provider: Allow to initialize the TracerProvider to set default
                resources

        """
        for monitor in self.monitors:
            monitor.monitor(tracer_provider=tracer_provider)
