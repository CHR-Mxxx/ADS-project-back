from pydantic import BaseModel, EmailStr
from typing import List


class CaptchaEmail(BaseModel):
    email: str
