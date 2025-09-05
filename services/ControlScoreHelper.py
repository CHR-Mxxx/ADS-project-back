from utils.GetSongInformation import get_song_information
from utils.ComputeScore import calculate_possible_scores
from os import path
import json
from enum import Enum


class Difficulty(Enum):
    EZ = "ez"
    HD = "hd"
    IN = "in"
    AT = "at"
    LEGACY = "legacy"


def controlScore(songId: str, score: int, difficulty: Difficulty):
    songInfo = get_song_information(songId)
    pos = calculate_possible_scores(
        total_notes=songInfo[difficulty.value]["combo"], target_score=score
    )
    print(pos)
    return pos
