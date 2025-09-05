from utils.RankingScoreHelper import RankingScoreHelper, turnToRks
from utils.GetSongInformation import get_song_information
from os import path
from json import loads


def RksHelper(
    myBestSingleRks: float,
    songRks: float,
    myBestAcc: int,
    b27Rks: float,
    p3Rks: float,
    wantRks: float,
):
    rks_helper = RankingScoreHelper(
        myBestSingleRks=myBestSingleRks,
        songRks=songRks,
        myBestAcc=myBestAcc,
        b27Rks=b27Rks,
        p3Rks=p3Rks,
        wantRks=wantRks,
    )
    answer = rks_helper.improveSingleRks(
        bestRks=turnToRks(acc=myBestAcc, realRks=songRks)
    )
    return answer
