import random
import string

from core.logger import logger
from db.pg import get_session
from fastapi import APIRouter, Depends, HTTPException, status
from helpers.auth import get_current_user
from models.promocodes import Promocodes
from schemas.promocodes import PromocodeCreate, PromocodeOut
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


async def _generate_unique_promocode(
    db_session: AsyncSession,
) -> str:
    """
    Generate promode by provided parameters.
    """

    while True:
        # Генерируем случайную строку из 12 символов (буквы и цифры)
        code = "".join(random.choices(string.ascii_uppercase + string.digits, k=12))
        # Проверяем, существует ли такой промокод
        result = await db_session.execute(
            select(Promocodes).where(Promocodes.promocode == code)
        )
        existing_code = result.scalars().first()
        if not existing_code:
            return code


@router.post("/", response_model=PromocodeOut)
async def generate_promocode(
    promocode_data: PromocodeCreate,
    db: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user),
):
    code = await _generate_unique_promocode(db)
    logger.info(f"Generated promocode: {code}")

    new_promocode = Promocodes(
        promocode=code,
        discount_percent=promocode_data.discount_percent,
        discount_rubles=promocode_data.discount_rubles,
        start_date=promocode_data.start_date,
        end_date=promocode_data.end_date,
        usage_limit=promocode_data.usage_limit,
        used_count=0,
        is_active=promocode_data.is_active,
        is_one_time=promocode_data.is_one_time,
    )

    db.add(new_promocode)
    try:
        await db.commit()
        await db.refresh(new_promocode)
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Error creating promocode: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка при создании промокода")

    return new_promocode
