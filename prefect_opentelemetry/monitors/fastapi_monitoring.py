from dataclasses import dataclass
from fastapi import FastAPI

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.trace import TracerProvider


@dataclass
class FastAPIMonitoring:
    app: FastAPI

    def monitor(self, tracer_provider: TracerProvider = None) -> None:
        FastAPIInstrumentor.instrument_app(
            app=self.app, tracer_provider=tracer_provider
        )
