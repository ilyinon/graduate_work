from core.logger import logger
from db.pg import get_session, get_session_local
from fastapi import APIRouter, Depends, HTTPException, status
from helpers.auth import get_current_user
from helpers.validate import _validate_promocode
from models.promocodes import Promocodes
from sqlalchemy import select
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/{promocode}")
async def apply_promocode(
    promocode: str,
    db: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user),
):
    """
    Apply promocode to use by adding one to used_count.
    """

    logger.info(f"promocode from request: {promocode}")
    await _validate_promocode(promocode, get_session_local)
    result = await db.execute(
        select(Promocodes).where(Promocodes.promocode == promocode)
    )
    promocode = result.scalars().first()
    if not promocode:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Промокод не найден")
    promocode.used_count += 1
    await db.commit()
    return {"detail": "Промокод успешно применен"}
