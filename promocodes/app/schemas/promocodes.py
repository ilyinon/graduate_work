from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator


class PromocodeCreate(BaseModel):
    discount_percent: Optional[float] = Field(0.0, description="Скидка в процентах")
    discount_rubles: Optional[float] = Field(
        0.0, description="Фиксированная скидка в рублях"
    )
    start_date: Optional[datetime] = Field(
        None, description="Дата начала действия промокода"
    )
    end_date: Optional[datetime] = Field(
        None, description="Дата окончания действия промокода"
    )
    usage_limit: Optional[int] = Field(
        None, description="Максимальное количество использований"
    )
    is_active: bool = Field(True, description="Активен ли промокод")
    is_one_time: bool = Field(True, description="Одноразовый ли промокод")

    @model_validator(mode="after")
    def check_discounts(self):
        if self.discount_percent == 0.0 and self.discount_rubles == 0.0:
            raise ValueError("Необходимо указать скидку в процентах или рублях")
        return self

    model_config = ConfigDict(tz="utc")


class PromocodeOut(BaseModel):
    id: UUID
    promocode: str
    discount_percent: float
    discount_rubles: float
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    usage_limit: Optional[int]
    used_count: int
    is_active: bool
    is_one_time: bool

    class Config:
        orm_mode = True
