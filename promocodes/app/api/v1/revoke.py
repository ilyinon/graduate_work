import random
from datetime import datetime, timedelta, timezone
from typing import Annotated, List, Literal, LiteralString, Optional, Union
from uuid import UUID

import requests
from core.config import promocodes_settings
from core.logger import logger
from db.pg import get_session
from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from models.promocodes import Promocodes
from sqlalchemy import select
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/{promocode}")
async def revoke_promocode(promocode: str, db: Session = Depends(get_session)):
    logger.info(f"promocode from request: {promocode}")
    result = await db.execute(
        select(Promocodes).where(Promocodes.promocode == promocode)
    )
    promocode = result.scalars().first()
    if not promocode:
        raise HTTPException(status_code=404, detail="Промокод не найден")
    if promocode.used_count > 0:
        promocode.used_count -= 1
        await db.commit()
    return {"detail": "Использование промокода отменено"}
