
from fastapi import FastAPI, HTTPException, Depends
from models.purchase import Purchase, Tariff, User
from sqlalchemy.orm import Session
from db.pg import get_session
from core.config import purchase_settings
import requests
from typing import Annotated, List, Literal, LiteralString, Optional, Union
from fastapi.responses import ORJSONResponse


app = FastAPI(
    title="purchase",
    docs_url="/api/v1/purchase/openapi",
    openapi_url="/api/v1/purchase/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.post("/api/v1/purchases/")
def create_purchase(user_id: int, tariff_id: int, promocode: Optional[str] = None, db: Session = Depends(get_session)):
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    tariff = db.query(Tariff).filter_by(id=tariff_id).first()
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
    db.commit()

    # Обработка оплаты (эмуляция)
    payment_successful = process_payment(user_id, amount)

    if payment_successful:
        purchase.is_successful = True
        db.commit()
        # Сообщаем сервису промокодов об успешном применении промокода
        if promocode:
            try:
                response = requests.post(f"{purchase_settings.promocode_service_url}/apply/{promocode}")
                response.raise_for_status()
            except requests.HTTPError as e:
                # Логируем ошибку, но не прерываем выполнение
                pass
        # Предоставляем доступ к тарифу и т.д.
        # ...

        return {"detail": "Покупка успешно совершена", "amount": amount}

    else:
        # В случае неудачной оплаты
        purchase.failure_reason = "Ошибка оплаты"
        db.commit()
        # Отменяем применение промокода, если он был использован
        if promocode:
            try:
                response = requests.post(f"{purchase_settings.promocode_service_url}/revoke/{promocode}")
                response.raise_for_status()
            except requests.HTTPError as e:
                # Логируем ошибку
                pass
        raise HTTPException(status_code=400, detail="Ошибка оплаты")


def process_payment(user_id: int, amount: float) -> bool:
    # Интеграция с платежной системой
    # Здесь эмуляция успешной оплаты
    return True
