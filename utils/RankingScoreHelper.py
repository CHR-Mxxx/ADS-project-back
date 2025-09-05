import math
from floatUp import floatUp


def turnToAcc(myRks: float, realRks: float):
    return 5500 + 4500 * math.sqrt(myRks / realRks)


def turnToRks(acc: int, realRks: float):
    return realRks * ((acc - 5500) / 4500) ** 2


class RankingScoreHelper:
    def __init__(
        self,
        myRks: float,
        songRks: float,
        bestAcc: float,
        b27Rks: float,
        p3Rks: float,
        wantRks: float,
    ):
        self.myRks = myRks
        self.songRks = songRks
        self.bestAcc = round(bestAcc * 10000)
        self.b27Rks = b27Rks
        self.p3Rks = p3Rks
        self.wantRks = wantRks

    def improveB27Rks(self, finalAcc: float):
        # 此函数用于计算提升B27所需要的单曲最少需要达到的提升rks
        if self.wantRks > 16.89:
            return 0
        self.wantRksUp = self.wantRks - self.myRks
        deltaRks = self.wantRksUp * 30
        if self.myRks >= self.b27Rks:
            return deltaRks
        else:
            return turnToRks(finalAcc, self.songRks) - self.b27Rks

    def improveP3Rks(self):
        # 此函数用于计算提升P3所需要的单曲可以提升多少rks
        if self.songRks <= self.p3Rks:
            return 0
        return self.songRks - self.p3Rks

    def improveSingleRks(self, bestRks: float):  # 需要提升的单曲rks
        if (
            self.songRks <= self.b27Rks and self.songRks >= self.p3Rks
        ):  # 无法提升b27但能提升p3，即ap floor太低
            upRks = (self.songRks - self.p3Rks) / 30
            finalRks = self.myRks + upRks
            if floatUp(finalRks) >= floatUp(self.wantRks):
                return {
                    "canImprove": True,
                    "needAcc": 1.0000,
                }
        for acc in range(round(self.bestAcc * 10000), 9999):
            wantSingleRks = bestRks + self.improveB27Rks(acc)
            finalRks = turnToRks(acc, self.songRks)
            if floatUp(finalRks) >= floatUp(wantSingleRks):
                return {
                    "canImprove": True,
                    "needAcc": round(acc) / 10000,
                }  # 到这里考虑未ap时提升rks的情况
        if acc == 10000:
            finalRks = bestRks + self.improveP3Rks() + self.improveB27Rks(10000)
            if floatUp(finalRks) >= floatUp(self.wantRks):
                return {"canImprove": True, "needAcc": 1.0000}
            # 考虑ap时提升rks的情况
        return {
            "canImprove": False,
        }


RKSHELPER_TEST = RankingScoreHelper(
    myRks=16.26, songRks=16.5, bestAcc=0.9803, b27Rks=15.73, p3Rks=15.88, wantRks=16.30
)
print(RKSHELPER_TEST.improveSingleRks(bestRks=turnToRks(bestAcc=0.9803, realRks=16.5)))
