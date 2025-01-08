import sentry_sdk
from api.v1 import apply, generate, revoke, validate
from core.config import promocodes_settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

if promocodes_settings.sentry_enable:
    sentry_sdk.init(
        dsn=promocodes_settings.sentry_dsn,
        traces_sample_rate=promocodes_settings.sentry_traces_sample_rate,
        _experiments={
            "continuous_profiling_auto_start": True,
        },
    )

app = FastAPI(
    title="promocodes",
    docs_url="/api/v1/promocodes/openapi",
    openapi_url="/api/v1/promocodes/openapi.json",
    default_response_class=ORJSONResponse,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "null",
        "http://localhost",
        "http://localhost:8000",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


app.include_router(apply.router, prefix="/api/v1/promocodes/apply")
app.include_router(revoke.router, prefix="/api/v1/promocodes/revoke")
app.include_router(validate.router, prefix="/api/v1/promocodes/validate")
app.include_router(generate.router, prefix="/api/v1/promocodes/generate")
