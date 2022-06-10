"""This is an example flows module"""
from prefect import flow

from prefect_opentelemetry.tasks import (
    goodbye_prefect_opentelemetry,
    hello_prefect_opentelemetry,
)


@flow
def hello_and_goodbye():
    """
    Sample flow that says hello and goodbye!
    """
    print(hello_prefect_opentelemetry)
    print(goodbye_prefect_opentelemetry)
