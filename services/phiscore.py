def control_Score(songId: str, score: int):
    if songId[0] == "5":
        song_inChapter, song_chapterId = songId.split(".")
        print(song_inChapter, song_chapterId)
    else:
        song_Mchapter, song_MinChapter, song_chapterId = songId.split(".")
        print(song_Mchapter, song_MinChapter, song_chapterId)
