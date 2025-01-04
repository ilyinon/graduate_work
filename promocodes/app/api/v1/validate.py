from fastapi import FastAPI, HTTPException, Depends
from models.promocodes import Promocodes
from sqlalchemy.orm import Session
from db.pg import get_session
from core.config import promocodes_settings
import requests
from typing import Annotated, List, Literal, LiteralString, Optional, Union
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter, Depends, HTTPException, status
import random
from uuid import UUID
from sqlalchemy import select
from core.logger import logger
from datetime import datetime, timedelta, timezone

router = APIRouter()


@router.get("/{promocode}")
async def validate_promocode(promocode: str, db: Session = Depends(get_session)):
    logger.info(f"promocode from request: {promocode}")
    try:
        result = await db.execute(select(Promocodes).where(Promocodes.promocode == promocode))
        promocode = result.scalars().first()
        logger.info(f"promocode from db: {promocode.promocode}")
    except:
        promocode = None
    

    if not promocode:
        raise HTTPException(status_code=404, detail="Промокод не найден")
    if not promocode.is_active:
        raise HTTPException(status_code=400, detail="Промокод неактивен")
    if promocode.start_date and datetime.utcnow() < promocode.start_date:
        raise HTTPException(status_code=400, detail="Промокод еще не активен")
    if promocode.end_date and datetime.utcnow() > promocode.end_date:
        raise HTTPException(status_code=400, detail="Срок действия промокода истек")
    if promocode.is_one_time and promocode.used_count >= 1:
        raise HTTPException(status_code=400, detail="Промокод уже использован")
    if promocode.usage_limit and promocode.used_count >= promocode.usage_limit:
        raise HTTPException(status_code=400, detail="Достигнут лимит использований промокода")

    return {
        "code": promocode.promocode,
        "discount_percent": promocode.discount_percent,
        "discount_rubles": promocode.discount_rubles
    }