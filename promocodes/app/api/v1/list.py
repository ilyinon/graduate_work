from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.logger import logger
from db.pg import get_session
from helpers.auth import get_current_user
from models.promocodes import Promocodes
from schemas.promocodes import PromocodeOut

router = APIRouter()


@router.get("/", response_model=List[PromocodeOut])
async def get_promocodes_list(
    db: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1),
):
    """
    Get list promocodes from DB and show it by request with pagination.
    """
    try:
        result = await db.execute(select(Promocodes).offset(skip).limit(limit))
        promocodes = result.scalars().all()
        return promocodes
    except SQLAlchemyError as e:
        logger.info(f"error to get promocodes: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при получении списка промокодов",
        )
