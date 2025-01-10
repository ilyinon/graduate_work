from core.logger import logger
from db.pg import get_session, get_session_local
from fastapi import APIRouter, Depends, HTTPException
from helpers.auth import get_current_user
from helpers.validate import _validate_promocode
from models.promocodes import UserPromocodes
from models.users import User
from schemas.promocodes import ApplyPromocodeRequest, ApplyPromocodeResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

router = APIRouter()


@router.post("/", response_model=ApplyPromocodeResponse)
async def assign_promocode_to_user(
    request: ApplyPromocodeRequest,
    db: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user),
):
    """
    Assign promocode to user by admin.
    """

    logger.info(f"request {request}")
    try:
        result = await db.execute(select(User).where(User.email == request.user_email))
        user = result.scalar_one_or_none()
        logger.info(f"user: {user}")
        if user is None:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
    except Exception as e:
        logger.error(f"Expection to fetch data: {e}")
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    promocode = await _validate_promocode(request.promocode, get_session_local)

    result = await db.execute(
        select(UserPromocodes)
        .where(UserPromocodes.user_id == user.id)
        .where(UserPromocodes.promocode_id == promocode.id)
    )
    user_promocode = result.scalars().first()
    if user_promocode:
        raise HTTPException(
            status_code=400, detail="Пользователь уже использовал этот промокод"
        )

    user_promocode = UserPromocodes(user_id=user.id, promocode_id=promocode.id)
    db.add(user_promocode)

    promocode.used_count += 1

    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Ошибка при применении промокода")

    return ApplyPromocodeResponse(
        success=True, message="Промокод успешно применен к аккаунту пользователя"
    )
