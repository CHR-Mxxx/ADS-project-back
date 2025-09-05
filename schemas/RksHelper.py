from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional


class RKSRequest(BaseModel):
    myBestSingleRks: float  # 这首歌推分前单曲rks
    songRks: float  # 这首歌的官方定数
    myBestAcc: int  # 这首歌的最高准确度
    b27Rks: float  # B27地板
    p3Rks: float  # P3地板
    wantRks: float  # 想要达到的总rks


class RKSResponse(BaseModel):
    canImprove: bool
    needAcc: Optional[float] = None
    occasion: Optional[str] = None
    message: Optional[str] = None
