import datetime

from core.logger import logger
from fastapi import APIRouter, Depends, HTTPException
from models.promocodes import Promocodes
from sqlalchemy import select
from sqlalchemy.orm import Session


async def _validate_promocode(promocode, session):
    logger.info(f"Start to validate promocode: {promocode}")
    try:
        async with session() as db:
            result = await db.execute(
                select(Promocodes).where(Promocodes.promocode == promocode)
            )
            promocode = result.scalars().first()
        logger.info(f"promocode from db: {promocode.promocode}")
    except Exception as e:
        logger.error(f"the error to db: {e}")
        promocode = None

    if not promocode:
        logger.info(f"Promocode {promocode} is not exist")
        raise HTTPException(status_code=404, detail="Промокод не найден")
    if not promocode.is_active:
        logger.info(f"Promocode {promocode} is not active")
        raise HTTPException(status_code=400, detail="Промокод неактивен")
    if promocode.start_date.replace(
        tzinfo=datetime.timezone.utc
    ) and datetime.datetime.now(datetime.timezone.utc) < promocode.start_date.replace(
        tzinfo=datetime.timezone.utc
    ):
        logger.info(f"Promocode {promocode} has start date in future")
        raise HTTPException(status_code=400, detail="Промокод еще не активен")
    if promocode.end_date.replace(
        tzinfo=datetime.timezone.utc
    ) and datetime.datetime.now(datetime.timezone.utc) > promocode.end_date.replace(
        tzinfo=datetime.timezone.utc
    ):
        logger.info(f"Promocode {promocode} has expired date")
        raise HTTPException(status_code=400, detail="Срок действия промокода истек")
    if promocode.is_one_time and promocode.used_count >= 1:
        logger.info(f"Promocode {promocode} is onetime and has been used")
        raise HTTPException(status_code=400, detail="Промокод уже использован")
    if promocode.usage_limit and promocode.used_count >= promocode.usage_limit:
        logger.info(f"Promocode {promocode} reached limits of using")
        raise HTTPException(
            status_code=400, detail="Достигнут лимит использований промокода"
        )
    return promocode
