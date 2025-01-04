from typing import Annotated, List, Literal, LiteralString, Optional, Union

import requests
from api.v1 import purchase
from core.config import purchase_settings
from db.pg import get_session
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from models.purchase import Purchase, Tariff, User
from sqlalchemy.orm import Session

app = FastAPI(
    title="purchase",
    docs_url="/api/v1/purchase/openapi",
    openapi_url="/api/v1/purchase/openapi.json",
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


app.include_router(purchase.router, prefix="/api/v1/purchase")
