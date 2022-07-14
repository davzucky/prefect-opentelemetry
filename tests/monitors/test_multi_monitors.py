from dataclasses import dataclass

import pytest
from opentelemetry.trace import TracerProvider

from prefect_opentelemetry.monitors import MultiMonitors


@dataclass
class FakeMonitor:
    name: str
    nb_call: int = 0

    def monitor(self, tracer_provider: TracerProvider = None) -> None:
        self.nb_call += 1


def test_can_initialize_with_empty_list():
    monitor = MultiMonitors(monitors=[])
    assert len(monitor.monitors) == 0


@pytest.mark.parametrize("nb_monitors", [(0), (1), (5), (10)])
def test_call_monitor_in_list(nb_monitors: int):
    child_monitors = [FakeMonitor(name=f"Monitor_{i}") for i in range(nb_monitors)]

    monitor = MultiMonitors(monitors=child_monitors)
    monitor.monitor(None)

    assert len(child_monitors) == len([m for m in child_monitors if m.nb_call == 1])
