from fastapi import FastAPI
import time
from opentelemetry import trace 
from opentelemetry.sdk.trace import TracerProvider 

"""
Kullanım:
    # apt update
    # pip install opentelemetry-sdk
    # pip install opentelemetry-api
    # pip install opentelemetry-exporter-otlp
"""


provider = TracerProvider()
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

app = FastAPI()

@app.get("/")
def get_homepage():
    count = 1
    while count <= 3:
        with tracer.start_as_current_span(f"loop-count-{count}") as span:
            time.sleep(1)
    return {
        "status": "ok",
        "foo": "bar"
    }
