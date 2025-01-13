from core.logger import logger
from db.pg import get_session
from fastapi import APIRouter, Depends, HTTPException, status
from helpers.auth import get_current_user
from models.promocodes import Promocodes
from sqlalchemy import select
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/{promocode}")
async def revoke_promocode(
    promocode: str,
    db: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user),
):
    """
    Revoke of using promocode by minus used_count.
    """
    logger.info(f"promocode from request: {promocode}")
    result = await db.execute(
        select(Promocodes).where(Promocodes.promocode == promocode)
    )
    promocode = result.scalars().first()
    if not promocode:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Промокод не найден"
        )
    if promocode.used_count > 0:
        promocode.used_count -= 1
        await db.commit()
    return {"detail": "Использование промокода отменено"}
