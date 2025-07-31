from pydantic import BaseModel


class CaptchaEmail(BaseModel):
    email: str
