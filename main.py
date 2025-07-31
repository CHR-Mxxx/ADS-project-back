from typing import Annotated

from fastapi import Depends, FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

from schemas.captchaEmail import CaptchaEmail

from services.user import send_email

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://192.168.31.152:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI Auth App!"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

@app.post("/captcha")
async def send_captcha(email:CaptchaEmail):
    send_email(email, background_tasks=BackgroundTasks())
    return {"message": "Captcha sent successfully to the provided email."}