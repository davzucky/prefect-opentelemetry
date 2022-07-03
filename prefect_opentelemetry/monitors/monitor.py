from typing import Protocol
from fastapi import FastAPI
from opentelemetry.trace import TracerProvider

class Monitor(Protocol):

    def monitor(self, trace_provider: TracerProvider) -> None:
        pass