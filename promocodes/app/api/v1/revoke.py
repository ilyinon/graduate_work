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

@router.post("/{code}")
def revoke_promocode(code: str, db: Session = Depends(get_session)):
    promocode = db.query(Promocodes).filter_by(code=code).first()
    if not promocode:
        raise HTTPException(status_code=404, detail="Промокод не найден")
    if promocode.used_count > 0:
        promocode.used_count -= 1
        db.commit()
    return {"detail": "Использование промокода отменено"}