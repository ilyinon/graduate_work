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


@router.post("/{promocode}")
async def apply_promocode(promocode: str, db: Session = Depends(get_session)):
    logger.info(f"promocode from request: {promocode}")
    result = await db.execute(select(Promocodes).where(Promocodes.promocode == promocode))
    promocode = result.scalars().first()
    if not promocode:
        raise HTTPException(status_code=404, detail="Промокод не найден")
    promocode.used_count += 1
    await db.commit()
    return {"detail": "Промокод успешно применен"}