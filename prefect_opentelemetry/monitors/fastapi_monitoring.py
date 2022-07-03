from dataclasses import dataclass, field
from fastapi import FastAPI

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.trace import TracerProvider
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor


@dataclass
class FastAPIMonitoring:
    instrumentor: BaseInstrumentor = field(default_factory= lambda: FastAPIInstrumentor())

    def monitor(self, tracer_provider: TracerProvider = None) -> None:
        self.instrumentor.instrument(
            tracer_provider=tracer_provider
        )
