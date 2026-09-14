import os

import sentry_sdk
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

sentry_dsn = os.getenv("SENTRY_DSN")
if sentry_dsn:
    sentry_sdk.init(
        dsn=sentry_dsn,
        traces_sample_rate=1.0,
    )
app = FastAPI()


@app.get("/ping", response_class=PlainTextResponse)
def ping():
    return "pong"