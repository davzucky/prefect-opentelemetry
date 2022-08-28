from dataclasses import dataclass

import pytest
from opentelemetry.trace import TracerProvider

from prefect_opentelemetry.monitors import (  # AsyncPGMonitor,; SQLLite3Monitor,
    MultiMonitors,
)

# from prefect.settings import PREFECT_ORION_DATABASE_CONNECTION_URL, temporary_settings

# from prefect_opentelemetry.monitors.multi_monitors import (
#     get_default_prefect_server_monitors,
# )


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
    monitor.monitor(tracer_provider=None)

    assert len(child_monitors) == len([m for m in child_monitors if m.nb_call == 1])


# @pytest.mark.xfail(reason="Disable postgres OTLP")
# def test_default_monitors_contain_asynpg():
#     db_con_str = (
#         "postgresql+asyncpg://postgres:yourTopSecretPassword@localhost:5432/orion"
#     )
#     with temporary_settings({PREFECT_ORION_DATABASE_CONNECTION_URL: db_con_str}):
#         monitors = get_default_prefect_server_monitors()
#         assert len(monitors) == 3
#         assert (
#             len(
#              [monitor for monitor in monitors if isinstance(monitor, AsyncPGMonitor)]
#             )
#             == 1
#         )


# @pytest.mark.xfail(reason="Disable sqllite OTLP")
# def test_default_monitors_contain_sqllite():
#     db_con_str = "sqlite+aiosqlite:////full/path/to/a/location/orion.db"

#     with temporary_settings({PREFECT_ORION_DATABASE_CONNECTION_URL: db_con_str}):
#         monitors = get_default_prefect_server_monitors()
#         assert len(monitors) == 3
#         assert (
#             len(
#                 [
#                     monitor
#                     for monitor in monitors
#                     if isinstance(monitor, SQLLite3Monitor)
#                 ]
#             )
#             == 1
#         )
