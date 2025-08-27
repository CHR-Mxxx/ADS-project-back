import json
from enum import Enum

SongRelative1 = {
    "1": "main_chapter",
    "2": "branch_chapter",
    "3": "external_chapter",
    "4": "premium_chapter",
    "5": "single_collection",
}

SongRelative2 = {
    "1.1": "chapter_legacy",
    "1.2": "chapter_5",
    "1.3": "chapter_6",
    "1.4": "chapter_7",
    "1.5": "chapter_8",
    "2.1": "chapter_1",
    "2.2": "chapter_2",
    "2.3": "chapter_3",
    "2.4": "chapter_4",
    "3.1": "camellia",
    "4.1": "Rising Sun Traxx",
    "4.2": "Hyun",
    "4.3": "GOOD",
    "4.4": "WAVEAT",
    "4.5": "Muse Dash",
    "4.6": "KALPA",
    "4.7": "Lanota",
    "4.8": "JMT",
    "4.9": "CMSYL",
    "4.10": "OverRapid",
    "4.11": "Rotaeno",
    "4.12": "CHUNITHM",
    "4.13": "Paradigm:Reboot",
    "4.14": "SHINOBI SLASH",
    "4.15": "TAKUMI³",
    "4.16": "JZDS",
    "4.17": "EGTS",
    "4.18": "Immaculée Sekai",
    "4.19": "オンゲキ",
}


def control_Score(songId: str, score: int):
    if songId[0] == "5":
        song_inChapter, song_chapterId = songId.split(".")
        print(song_inChapter, song_chapterId)
        song_inChapterName = SongRelative1[song_inChapter]
        # with open("/ADS-project-back/assets/song_information.json", "r") as f:
        #     songData = json.load(f)
        #     song = songData[song_inChapterName][song_chapterId]
        #     print(song["name"])
    else:
        song_Mchapter, song_MinChapter, song_chapterId = songId.split(".")
        song_inChapter = f"{song_Mchapter}.{song_MinChapter}"
        print(song_inChapter, song_chapterId)
        song_MChapterName = SongRelative1[song_Mchapter]
        song_inChapterName = SongRelative2[song_inChapter]
        # with open("../assets/song_information.json", "r") as f:
        #     songData = json.load(f)
        #     song = songData[song_MChapterName][song_inChapterName][song_chapterId]
        #     print(song["name"])
