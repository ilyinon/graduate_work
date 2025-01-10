from db.pg import get_session
from fastapi import APIRouter, Depends, HTTPException
from helpers.auth import get_current_user
from helpers.validate import _validate_promocode
from models.users import User
# from models.promocodes import Promocodes, UserPromocodes
from schemas.promocodes import ApplyPromocodeRequest, ApplyPromocodeResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

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

    # Есть ли пользователь
    result = await db.execute(select(User).where(User.id == request.user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    # Проверка наличия и активности промокода
    promocode = await _validate_promocode(promocode)

    # Применение промокода к аккаунту пользователя
    user_promocode = UserPromocodes(user_id=user.id, promocode_id=promocode.id)
    db.add(user_promocode)

    # Увеличение счетчика использования промокода
    promocode.used_count += 1

    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Ошибка при применении промокода")

    return ApplyPromocodeResponse(
        success=True,
        message="Промокод успешно применен к аккаунту пользователя",
        promocode=promocode,
    )
