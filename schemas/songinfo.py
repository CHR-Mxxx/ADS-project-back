from pydantic import BaseModel


class SongInfo(BaseModel):
    songId: str
    score: int
