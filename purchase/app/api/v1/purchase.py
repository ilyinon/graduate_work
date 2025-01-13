import random
from decimal import Decimal
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

import httpx
import requests
from core.config import purchase_settings
from core.logger import logger
from db.pg import get_session
from helpers.auth import check_from_auth, take_user_id
from models.purchase import Purchase, Tariff, User

get_token = HTTPBearer(auto_error=False)

router = APIRouter()


class PurchaseRequest(BaseModel):
    tariff_id: UUID = Field(..., example="8656a8f3-2713-4efc-bf63-79bd60df8417")
    promocode: Optional[str] = Field(None, example="DISCOUNT_10P")


@router.get("/tariff")
async def get_tariffs(
    db: Session = Depends(get_session), credentials: str = Depends(get_token)
):
    if not await check_from_auth(credentials):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Доступ запрещён"
        )

    result = await db.execute(select(Tariff))
    tariffs = result.scalars().all()
    tariffs_to_return = []
    for tariff in tariffs:
        new_tariff = {
            "id": tariff.id,
            "name": tariff.name,
            "description": tariff.description,
            "price": tariff.price,
        }
        tariffs_to_return.append(new_tariff)
    return {"detail": "Список тарифов", "tariffs": tariffs_to_return}


@router.post("/checkout")
async def create_checkout(
    request: PurchaseRequest,
    db: Session = Depends(get_session),
    credentials: str = Depends(get_token),
):
    logger.info(f"credentials: {credentials}")
    if not await check_from_auth(credentials):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Доступ запрещён"
        )

    logger.info(f"request: {request}")

    if request.promocode:
        promocode = request.promocode
    else:
        promocode = None
    tariff_id = request.tariff_id

    result = await db.execute(select(Tariff).where(Tariff.id == tariff_id))
    tariff = result.scalars().first()

    if not tariff:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Тариф не найден"
        )

    amount = tariff.price

    promocode_data = None
    if promocode:
        promocode_data = await check_promocode(promocode)

        if promocode_data:
            amount = await calculate_amount(promocode_data, amount)
            return {"detail": "Промокод успешно применён", "amount": amount}

    return {"detail": "Стоимость подписки", "amount": amount}


@router.post("/payment")
async def create_purchase(
    request: PurchaseRequest,
    db: Session = Depends(get_session),
    credentials: str = Depends(get_token),
):
    logger.info(f"request: {request}")
    if not await check_from_auth(credentials):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Доступ запрещён"
        )

    user_id = await take_user_id(credentials.credentials)
    promocode = request.promocode
    tariff_id = request.tariff_id

    headers = {"Authorization": f"Bearer {purchase_settings.promocode_service_token}"}

    logger.info(f"user_id: {user_id}")

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    logger.info(f"user: {user.id}")

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден"
        )
    result = await db.execute(select(Tariff).where(Tariff.id == tariff_id))
    tariff = result.scalars().first()

    if not tariff:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Тариф не найден"
        )

    amount = tariff.price

    promocode_data = None

    if promocode:
        try:
            promocode_data = await check_promocode(promocode)
        except Exception as e:
            logger.info(f"failed to apply promocode: {e}")

    amount = await calculate_amount(promocode_data, amount)

    # Создаем запись о покупке

    purchase = Purchase(
        user_id=user_id, tariff_id=tariff_id, amount=amount, promocode_code=promocode
    )
    db.add(purchase)
    await db.commit()
    await db.refresh(purchase)
    logger.info(f"purchase: {purchase.id}")

    # Обработка оплаты (эмуляция)
    payment_result = await process_payment(user_id, amount)

    if payment_result:
        purchase.is_successful = True
        await db.commit()
        if promocode:
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{purchase_settings.promocode_service_url}/apply/{promocode}",
                        headers=headers,
                    )
                    response.raise_for_status()
            except Exception as e:
                logger.info(f"the error to use promocode: {e}")

        return {"detail": "Покупка успешно совершена", "amount": amount}

    else:
        purchase.failure_reason = "Ошибка оплаты"
        await db.commit()
        if promocode:
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{purchase_settings.promocode_service_url}/revoke/{promocode}",
                        headers=headers,
                    )
                    response.raise_for_status()

            except requests.HTTPError:
                pass
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Ошибка оплаты"
        )


async def check_promocode(promocode: str) -> float:
    headers = {"Authorization": f"Bearer {purchase_settings.promocode_service_token}"}

    if promocode:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{purchase_settings.promocode_service_url}/validate/{promocode}",
                    headers=headers,
                )
                response.raise_for_status()
            promocode_data = response.json()
            return promocode_data

        except requests.HTTPError as e:
            try:
                detail = e.response.json().get("detail", "Промокод не действует")
            except:
                detail = "Промокод не действует"
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ошибка промокода: {detail}",
            )
        except Exception as e:
            logger.error(f"promocode service doesn't response: {e}")
        return None


async def calculate_amount(promocode_data, amount) -> Decimal:
    if promocode_data:
        discount_percent = promocode_data.get("discount_percent", 0)
        fixed_discount = promocode_data.get("discount_rubles", 0)
        if discount_percent != 0:
            amount *= 1 - discount_percent / 100
            logger.info(
                f"discount_percent: promocode {promocode_data['promocode']}, {discount_percent}, amount {amount}"
            )
        if fixed_discount != 0:
            amount -= fixed_discount
            logger.info(
                f"fixed_discount: promocode {promocode_data['promocode']}, {fixed_discount}, amount {amount}"
            )
        amount = Decimal(max(round(amount), 0))
    return amount


async def process_payment(user_id: int, amount: float) -> bool:
    """Emulate payment. 90% is successfull"""
    chance = random.randint(1, 100)
    if chance <= 90:
        return True
    else:
        return False
