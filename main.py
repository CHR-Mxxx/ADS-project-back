from typing import Annotated

from fastapi import Depends, FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi import Body
from pydantic import BaseModel

from schemas.captchaEmail import CaptchaEmail
from schemas.user import UserCreate, UserPublic, UserRegister
from schemas.songinfo import SongInfo

from services.user import send_email, register_user
from services.mydb import get_db
from services.phiscore import control_Score

from sqlalchemy.orm import Session

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
async def send_captcha(email: CaptchaEmail):
    answer = send_email(email.email, background_tasks=BackgroundTasks())
    return {
        "status": answer["status"],
        "message": answer["message"],
    }


@app.post("/register")
async def register_account(userInfo: UserRegister, db: Session = Depends(get_db)):
    user = userInfo.user
    inputCaptcha = userInfo.inputCaptcha
    answer = register_user(db, user, inputCaptcha)
    return answer


@app.post("/phiscore")
async def controlScore(songinfo: SongInfo):
    print(songinfo)
    songId = songinfo.songId
    score = songinfo.score
    control_Score(songId, score)
    pass
