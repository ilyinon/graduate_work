from datetime import datetime

from core.logger import logger
from db.pg import get_session
from fastapi import APIRouter, Depends, HTTPException
from helpers.auth import get_current_user
from models.promocodes import Promocodes
from sqlalchemy import select
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/{promocode}")
async def validate_promocode(
    promocode: str,
    db: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user),
):
    """
    Validate promode thru many parameters like: existence, start and stop date,
    if it is one_time and already used, or just reached its limits.
    """
    logger.info(f"promocode from request: {promocode}")
    try:
        result = await db.execute(
            select(Promocodes).where(Promocodes.promocode == promocode)
        )
        promocode = result.scalars().first()
        logger.info(f"promocode from db: {promocode.promocode}")
    except:
        promocode = None

    if not promocode:
        logger.info(f"Promocode {promocode} is not exist")
        raise HTTPException(status_code=404, detail="Промокод не найден")
    if not promocode.is_active:
        logger.info(f"Promocode {promocode} is not active")
        raise HTTPException(status_code=400, detail="Промокод неактивен")
    if promocode.start_date and datetime.utcnow() < promocode.start_date:
        logger.info(f"Promocode {promocode} has start date in future")
        raise HTTPException(status_code=400, detail="Промокод еще не активен")
    if promocode.end_date and datetime.utcnow() > promocode.end_date:
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

    return {
        "promocode": promocode.promocode,
        "discount_percent": promocode.discount_percent,
        "discount_rubles": promocode.discount_rubles,
    }
