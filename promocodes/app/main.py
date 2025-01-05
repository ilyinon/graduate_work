from typing import Annotated, List, Literal, LiteralString, Optional, Union

import requests
from api.v1 import apply, revoke, validate
from core.config import promocodes_settings
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from sqlalchemy.orm import Session

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
