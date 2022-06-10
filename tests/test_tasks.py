from prefect import flow

from prefect_opentelemetry.tasks import (
    goodbye_prefect_opentelemetry,
    hello_prefect_opentelemetry,
)


def test_hello_prefect_opentelemetry():
    @flow
    def test_flow():
        return hello_prefect_opentelemetry()

    flow_state = test_flow()
    task_state = flow_state.result()
    assert task_state.result() == "Hello, prefect-opentelemetry!"


def goodbye_hello_prefect_opentelemetry():
    @flow
    def test_flow():
        return goodbye_prefect_opentelemetry()

    flow_state = test_flow()
    task_state = flow_state.result()
    assert task_state.result() == "Goodbye, prefect-opentelemetry!"
