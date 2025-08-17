from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum, Date
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta
from sqlalchemy.dialects.mysql import INTEGER

Base = declarative_base()


class GenderEnum(Enum):
    male = "2"
    female = "1"
    unknown = "0"


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, nullable=False, primary_key=True, index=True)
    email = Column(String(64), nullable=False, unique=True, index=True)
    username = Column(String(64), nullable=False, index=True)
    password = Column(String(640), nullable=False)
    phone = Column(INTEGER(unsigned=True), nullable=True)
    gender = Column(Integer, nullable=False)
    birthday = Column(Date, nullable=True)
    description = Column(String(1024), nullable=True)
    created_at = Column(Date, default=datetime.now)
    updated_at = Column(Date, default=datetime.now, onupdate=datetime.now)
    expires_at = Column(Date, default=lambda: datetime.now() + timedelta(days=30))
    is_active = Column(
        Boolean, default=True
    )  # 是否为激活状态，若不是激活状态则无法保持登录状态，需重新登录
    is_superuser = Column(Boolean, default=False)  # 是否为超级用户
    is_available = Column(Boolean, default=True)  # 若注销账户则此账户不可用。
