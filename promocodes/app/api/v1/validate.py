from datetime import datetime

from core.logger import logger
from db.pg import get_session_local
from fastapi import APIRouter, Depends, HTTPException
from helpers.auth import get_current_user
from helpers.validate import _validate_promocode
from models.promocodes import Promocodes
from sqlalchemy import select
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/{promocode}")
async def validate_promocode(
    promocode: str,
    current_user: dict = Depends(get_current_user),
):
    """
    Validate promode thru many parameters like: existence, start and stop date,
    if it is one_time and already used, or just reached its limits.
    """
    logger.info(f"promocode from request: {promocode}")

    promocode = await _validate_promocode(promocode, get_session_local)

    return {
        "promocode": promocode.promocode,
        "discount_percent": promocode.discount_percent,
        "discount_rubles": promocode.discount_rubles,
    }
