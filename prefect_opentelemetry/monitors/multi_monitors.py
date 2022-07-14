"""
Define a monitor that allow can manage multiple monitors
"""
from dataclasses import dataclass
from typing import List

from opentelemetry.trace import TracerProvider

from .monitor import Monitor


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
            monitor.monitor(tracer_provider)
