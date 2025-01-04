
from fastapi import FastAPI, HTTPException, Depends
from models.purchase import Purchase, Tariff, User
from sqlalchemy.orm import Session
from db.pg import get_session
from core.config import purchase_settings
import requests
from typing import Annotated, List, Literal, LiteralString, Optional, Union
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter, Depends, HTTPException, status
import random
from uuid import UUID
from sqlalchemy import select
from core.logger import logger


router = APIRouter()

@router.post("/")
async def create_purchase(user_id: UUID, tariff_id: UUID, promocode: Optional[str] = None, db: Session = Depends(get_session)):
    logger.info(f"Request to buy from - user_id: {user_id}, tariff_id: {tariff_id}, promocode: {promocode}")

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    logger.info(f"user: {user.id}")

    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    result = await db.execute(select(Tariff).where(Tariff.id == tariff_id))
    tariff = result.scalars().first()

    if not tariff:
        raise HTTPException(status_code=404, detail="Тариф не найден")

    amount = tariff.price

    promocode_data = None

    # Проверка и применение промокода
    if promocode:
        try:
            # Проверяем промокод через API сервиса промокодов
            response = requests.get(f"{purchase_settings.promocode_service_url}/validate/{promocode}")
            response.raise_for_status()
            promocode_data = response.json()
            discount_percent = promocode_data.get("discount_percent", 0)
            fixed_discount = promocode_data.get("fixed_discount", 0)
            if discount_percent:
                amount *= (1 - discount_percent / 100)
            if fixed_discount:
                amount -= fixed_discount
            amount = max(amount, 0)
        except requests.HTTPError as e:
            # Здесь можно добавить логирование причины отказа
            try:
                detail = e.response.json().get("detail", "Промокод не действует")
            except:
                detail = "Промокод не действует"
            raise HTTPException(status_code=400, detail=f"Ошибка промокода: {detail}")

    # Создаем запись о покупке

    purchase = Purchase(user_id=user_id, tariff_id=tariff_id, amount=amount, promocode_code=promocode)
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
                response = requests.post(f"{purchase_settings.promocode_service_url}/apply/{promocode}")
                response.raise_for_status()
            except requests.HTTPError as e:
                # Логируем ошибку, но не прерываем выполнение
                pass


        return {"detail": "Покупка успешно совершена", "amount": amount}

    else:
        purchase.failure_reason = "Ошибка оплаты"
        await db.commit()
        if promocode:
            try:
                response = requests.post(f"{purchase_settings.promocode_service_url}/revoke/{promocode}")
                response.raise_for_status()
            except requests.HTTPError as e:
                pass
        raise HTTPException(status_code=400, detail="Ошибка оплаты")


async def process_payment(user_id: int, amount: float) -> bool:
    """ Emulate payment. 90% is successfull"""
    chance = random.randint(1, 100)
    if chance <= 90:
        return True
    else:
        return False