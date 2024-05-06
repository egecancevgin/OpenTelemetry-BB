from flask import Flask
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource


""" Kullanım:
    # docker pull jaegertracing/all-in-one:latest
    # docker run -d --name jaeger \
        -e COLLECTOR_ZIPKIN_HOST_PORT=:9411 \
        -p 5775:5775/udp \
        -p 6831:6831/udp \
        -p 6832:6832/udp \
        -p 5778:5778 \
        -p 16686:16686 \
        -p 14268:14268 \
        -p 14250:14250 \
        -p 9411:9411 \
        jaegertracing/all-in-one:1.22
    # apt update
    # apt install python3-pip
    # pip install flask
    # pip install opentelemetry-sdk
    # pip install opentelemetry-instrumentation-flask
    # pip install opentelemetry-exporter-proto
    # pip install opentelemetry-exporter-otlp-proto-http
    # pip install opentelemetry-exporter-otlp
"""

resource = Resource(attributes={
    "service.name": "bb"
})

app = Flask(__name__)

trace.set_tracer_provider(TracerProvider(resource=resource))
#tracer = trace.get_tracer(__name__)


#trace.set_tracer_provider(TracerProvider())

otlp_exporter = OTLPSpanExporter(endpoint="http://localhost:4317")

span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

FlaskInstrumentor().instrument_app(app)

@app.route("/")
def hello():
    tracer = trace.get_tracer(__name__) 
    with tracer.start_as_current_span("hello"):
        return "Hello, World!"


if __name__ == "__main__":
    app.run(debug=True)
