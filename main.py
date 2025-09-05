from typing import Annotated


from fastapi.responses import JSONResponse
from fastapi import Depends, FastAPI, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi import Body
from pydantic import BaseModel

from schemas.captchaEmail import CaptchaEmail
from schemas.user import UserCreate, UserPublic, UserRegister
from schemas.songinfo import SongInfo
from schemas.RksHelper import RKSRequest, RKSResponse

from services.user import send_email, register_user
from services.MyDb import get_db
from services.TapTapLogin import share, get_account_info, register_user

from utils.RankingScoreHelper import RankingScoreHelper, turnToRks
from services.ControlScoreHelper import controlScore

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


# 假设 share 模块中的内容已经适配到 FastAPI
# 这里需要根据实际情况调整 share 模块的实现


@app.post("/taplogin")
async def tap_login(request: Request):
    device_id = (await request.body()).decode()
    url = "https://www.taptap.com/oauth2/v1/device/code"
    payload = f"client_id=rAK3FfdieFob2Nn8Am&response_type=device_code&scope=basic_info&version=1.2.0&platform=unity&info=%7b%22device_id%22%3a%22{device_id}%22%7d"

    # 需要适配 share.client 到异步请求，比如使用 httpx
    response = await share.client.post(url, headers=share.tap_headers, data=payload)
    json_response = response.json()

    return JSONResponse(content=json_response["data"])


@app.post("/token/{device_code}")
async def get_token(device_code: str, request: Request):
    device_id = (await request.body()).decode()
    url = "https://www.taptap.cn/oauth2/v1/token"
    payload = f"grant_type=device_token&client_id=rAK3FfdieFob2Nn8Am&secret_type=hmac-sha-1&code={device_code}&version=1.0&platform=unity&info=%7b%22device_id%22%3a%22{device_id}%22%7d"

    # 需要适配 share.client 到异步请求
    response = await share.client.post(url, headers=share.tap_headers, data=payload)
    json_response = response.json()

    if not json_response["success"]:
        return JSONResponse(content=json_response["data"])

    token = json_response["data"]
    token_info = await get_account_info(token)  # 需要异步化
    user_info = await register_user(token, token_info)  # 需要异步化

    return JSONResponse(content=user_info)


@app.post("/phiscore")
async def compute_score(songinfo: SongInfo):
    print(songinfo)
    songId = songinfo.songId
    score = songinfo.score
    difficulty = songinfo.difficulty
    ans = controlScore(songId, int(score), difficulty)
    return ans


@app.post("/rkshelper")
async def rks_helper(request: RKSRequest):
    rks_helper = RankingScoreHelper(
        myBestSingleRks=request.myBestSingleRks,
        songRks=request.songRks,
        myBestAcc=request.myBestAcc,
        b27Rks=request.b27Rks,
        p3Rks=request.p3Rks,
        wantRks=request.wantRks,
    )
    result = rks_helper.improveSingleRks(
        bestRks=turnToRks(acc=request.myBestAcc, realRks=request.songRks)
    )
    return RKSResponse(**result)
