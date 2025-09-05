from pydantic import BaseModel
from services.ControlScoreHelper import Difficulty


class SongInfo(BaseModel):
    songId: str
    score: int
    difficulty: Difficulty
