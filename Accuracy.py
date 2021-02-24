import weightkey
class Accuracy:
    league: str
    year: int
    resultRatio: float
    accuracyScore: float
    correctHomeGoal: int
    correctAwayGoal: int
    correctResult: int
    wrongHomeGoal: int
    wrongResult: int
    wrongAwayGoal: int
    totalMatch: int
    homeGoalRatio: float
    awayGoalRatio: float
    guessedDraw: int
    guessedHome: int
    guessedAway: int
    correctHome: int
    correctDraw: int
    correctAway: int
    wrongHome: int
    wrongDraw: int
    wrongAway: int
    homeRatio: float
    drawRatio: float
    awayRatio: float
    guessedHomeRatio: float
    guessedDrawRatio: float
    guessedAwayRatio: float
    key: weightkey.weightkey
    def __init__(self, league):
        self.league=league
        self.year=0
        self.resultRatio=0
        self.accuracyScore=0
        self.correctHomeGoal=0
        self.correctAwayGoal=0
        self.correctResult=0
        self.wrongHomeGoal=0
        self.wrongResult=0
        self.wrongAwayGoal=0
        self.totalMatch=0
        self.homeGoalRatio=0
        self.awayGoalRatio=0
        self.guessedDraw=0
        self.guessedHome=0
        self.guessedAway=0
        self.correctHome=0
        self.correctDraw=0
        self.correctAway=0
        self.wrongHome=0
        self.wrongDraw=0
        self.wrongAway=0
        self.homeRatio=0
        self.drawRatio=0
        self.awayRatio=0
        self.guessedHomeRatio=0
        self.guessedDrawRatio=0
        self.guessedAwayRatio=0
        self.key=weightkey.weightkey