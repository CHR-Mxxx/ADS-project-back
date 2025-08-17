from pydantic import BaseModel
from datetime import date, datetime, timedelta
from enum import Enum

from sqlalchemy import SmallInteger as tinyint


class UserCreate(BaseModel):
    id: int
    email: str
    username: str
    password: str
    phone: int | None
    gender: Enum
    birthday: date | None
    description: str | None
    created_at: datetime = datetime.now()
    expires_at: datetime = datetime.now() + timedelta(days=30)
    updated_at: datetime = datetime.now()
    # is_active: tinyint = (
    #     1  # 是否为激活状态，若不是激活状态则无法保持登录状态，需重新登录
    # )
    # is_superuser: tinyint = 0  # 是否为超级用户
    # is_available: tinyint = 1  # 若注销账户则此账户不可用。


class UserPublic(BaseModel):
    email: str
    username: str
    password: str
    phone: int | None
    gender: int | None
    birthday: date | None
    description: str | None


class UserRegister(BaseModel):
    user: UserPublic
    inputCaptcha: str
