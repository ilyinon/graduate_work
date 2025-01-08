import pytest
from httpx import AsyncClient
from app.main import app
from app.models.promocodes import Promocodes
from datetime import datetime, timedelta
from app.db.pg import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

@pytest.mark.asyncio
async def test_valid_promocode(initialized_test_db):
    async with get_session() as session:
        promocode = Promocodes(
            promocode="VALIDCODE",
            is_active=True,
            start_date=None,
            end_date=None,
            is_one_time=False,
            usage_limit=None,
            used_count=0,
            discount_percent=10,
            discount_rubles=None,
        )
        session.add(promocode)
        await session.commit()

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/VALIDCODE")

    assert response.status_code == 200
    assert response.json() == {
        "promocode": "VALIDCODE",
        "discount_percent": 10,
        "discount_rubles": None,
    }

