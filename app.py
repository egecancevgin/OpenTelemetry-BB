from fastapi import FastAPI
import time

app = FastAPI()

"""
# apt update
# apt install python3-pip
# pip install -r requirements.txt
# opentelemetry-bootstrap -a requirements
# opentelemetry-instrument --service_name my_first.api uvicorn app:app
"""

@app.get("/")
def get_homepage():
    count = 1
    while count <= 3:
        print("Loop count {count}")
        count += 1
        time.sleep(1)

    return {
        "status": "ok",
        "foo": "bar"
    }
