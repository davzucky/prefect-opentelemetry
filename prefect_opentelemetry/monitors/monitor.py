from typing import Protocol
from fastapi import FastAPI
from opentelemetry.trace import TracerProvider
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor

class Monitor(Protocol):

    @property
    def instrumentor(self) -> BaseInstrumentor:
        pass

    def monitor(self, trace_provider: TracerProvider) -> None:
        pass