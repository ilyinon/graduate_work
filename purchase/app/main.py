import logging
from api.v1 import purchase
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

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

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@app.middleware("http")
async def log_request_data(request: Request, call_next):
    # Логируем метод и URL запроса
    logger.info(f"Запрос: {request.method} {request.url}")

    # Логируем заголовки
    headers = dict(request.headers)
    logger.info(f"Заголовки запроса: {headers}")

    # Логируем параметры запроса (query parameters)
    params = dict(request.query_params)
    logger.info(f"Параметры запроса: {params}")

    # Логируем тело запроса (если есть)
    body = await request.body()
    if body:
        logger.info(f"Тело запроса: {body.decode('utf-8')}")

    # Вызываем следующий обработчик
    response = await call_next(request)
    return response


app.include_router(purchase.router, prefix="/api/v1/purchase")
