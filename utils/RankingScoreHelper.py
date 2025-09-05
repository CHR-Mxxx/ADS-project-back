import math
from utils.floatUp import floatUp


def turnToAcc(myBestSingleRks: float, realRks: float):
    return 5500 + 4500 * math.sqrt(myBestSingleRks / realRks)


def turnToRks(acc: int, realRks: float):
    if acc > 7000:
        return realRks * ((acc - 5500) / 4500) ** 2
    else:
        return 0


class RankingScoreHelper:
    def __init__(
        self,
        myBestSingleRks: float,  # 这首歌推分前单曲rks
        songRks: float,  # 这首歌的官方定数
        myBestAcc: int,  # 这首歌的最高准确度
        b27Rks: float,  # B27地板
        p3Rks: float,  # P3地板
        wantRks: float,  # 想要达到的总rks
    ):
        self.myBestSingleRks = myBestSingleRks
        self.songRks = songRks
        self.myBestAcc = myBestAcc
        self.b27Rks = b27Rks
        self.p3Rks = p3Rks
        self.wantRks = wantRks

    def improveB27Rks(self, finalAcc: int):
        # 此函数用于计算提升B27所需要的单曲最少需要达到的提升rks
        if self.wantRks > 16.91:
            return 0  # 想当音游王？做梦去吧你
        wantRksUp = self.wantRks - self.myBestSingleRks
        deltaRks = wantRksUp * 30
        if self.myBestSingleRks >= self.b27Rks:
            return deltaRks  # 已经过b27地板了，继续加油往前推！！！
        else:
            return (
                turnToRks(finalAcc, self.songRks) - self.b27Rks
            )  # 还没过b27地板，计算推歌之后能比b27地板高多少

    def improveP3Rks(self):
        # 此函数用于计算提升P3所需要的单曲可以提升多少rks
        if self.songRks <= self.p3Rks:
            return 0  # 过不了p3地板
        print("songRks:", self.songRks)
        print("p3:", self.p3Rks)
        return self.songRks - self.p3Rks  # 过了p3地板，计算能提升多少rks

    def improveSingleRks(self, bestRks: float):  # 需要提升的单曲rks
        if (
            self.songRks <= self.b27Rks and self.songRks >= self.p3Rks
        ):  # 无法提升b27但能提升p3，即ap floor太低
            upRks = (self.songRks - self.p3Rks) / 30
            finalRks = self.myBestSingleRks + upRks
            if floatUp(finalRks) >= floatUp(self.wantRks):
                return {
                    "canImprove": True,
                    "needAcc": 1.0000,
                    "occasion": "ap",
                }
        for acc in range(round(self.myBestAcc), 10000):
            wantSingleRks = bestRks + self.improveB27Rks(acc)  # 需要达到的单曲rks
            finalRks = turnToRks(acc, self.songRks)  # 计算当前准确度下的单曲rks
            if floatUp(finalRks) >= floatUp(wantSingleRks):
                return {
                    "canImprove": True,
                    "needAcc": round(acc) / 10000,
                    "occasion": "b27",
                }  # 到这里考虑未ap时提升rks的情况
        acc = 10000
        finalRks = (
            bestRks + self.improveP3Rks() + self.improveB27Rks(10000)
        )  # 计算满分时的单曲rks
        print(bestRks)
        print("finalRks:", finalRks)
        print(self.improveP3Rks(), self.improveB27Rks(10000))
        print(
            "floatUp(finalRks):",
            floatUp(finalRks),
            "floatUp(self.wantRks):",
            floatUp(self.wantRks),
        )
        if floatUp(finalRks) >= floatUp(self.wantRks):
            print(finalRks)
            return {"canImprove": True, "needAcc": 1.0000, "occasion": "ap+b27"}
        # 考虑ap时提升rks的情况
        return {
            "canImprove": False,
            "needAcc": None,
            "occasion": None,
        }  # 沉默-_-微笑都没法救你


RKSHELPER_TEST = RankingScoreHelper(
    myBestSingleRks=16.26,
    songRks=16.3,
    myBestAcc=9876,
    b27Rks=15.73,
    p3Rks=15.81,
    wantRks=16.27,
)
print(RKSHELPER_TEST.improveSingleRks(bestRks=turnToRks(acc=9876, realRks=16.3)))
