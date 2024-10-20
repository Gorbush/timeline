
from contextlib import contextmanager
import logging
import os
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider, Tracer, Span
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry.sdk.resources import Resource

tracer: Tracer = None
otel_context = None
otel_attributes = {}

logger = logging.getLogger(__name__)

class DummyTracer:
    @contextmanager
    def start_as_current_span(self, name: str, *, context=None, attributes=None):
        logger.info(f"[dummy-telemetry] {name}")
        yield self
        
       
    def set_attribute(self, name: str, value: str):
        logger.debug(f"[dummy-telemetry] set_attribute: {name} = {value}")

    def add_event(self, name: str)  -> None :
        logger.debug(f"[dummy-telemetry] add_event: {name} ")

    def set_status(self, code: int) -> None :
        logger.debug(f"[dummy-telemetry] set_status: {code} ")


def init_tracer(service_name: str, disable_otel: bool = False):
    # Initialize tracing
    global tracer, otel_context
    if tracer is None:
        if os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT") and not disable_otel:
            otel_attributes["service.name"] = service_name
            otel_attributes["service_name"] = service_name
            otel_resource = Resource(attributes={
                "service.name": service_name
            })
            tracer_provider = TracerProvider(resource=otel_resource)
            tracer_processor = BatchSpanProcessor(OTLPSpanExporter())
            tracer_provider.add_span_processor(tracer_processor)
            trace.set_tracer_provider(tracer_provider)
            tracer = trace.get_tracer(__name__)

            prop = TraceContextTextMapPropagator()
            carrier = {}
            if "TRACEPARENT" in os.environ:
                carrier[TraceContextTextMapPropagator._TRACEPARENT_HEADER_NAME] = os.environ["TRACEPARENT"]

            if carrier:
                otel_context = prop.extract(carrier=carrier)
            else:
                otel_context = None
        else:
            otel_context = None
            tracer = DummyTracer()
    return tracer, otel_context

tracer, otel_context = init_tracer("timeline")

def root_span(span_name: str) -> Span:
    logger.debug(f"root span [{span_name}]")
    return tracer.start_as_current_span(span_name, attributes=otel_attributes, context=otel_context)


def sub_span(span_name: str, local_otel_context=None) -> Span:
    logger.debug(f"span [{span_name}]")
    return tracer.start_as_current_span(span_name, attributes=otel_attributes, context=local_otel_context)
        
