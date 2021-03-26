class weightkey:
    home: float
    draw: float
    away: float
    powerRank: float
    resultPerc: float
    pyEx: float
    pyExSide: float
    pattern1: float
    pattern3: float
    pattern5: float

    def __init__(self, home: float, draw: float, away: float, powerRank: float, resultPerc: float, pyEx: float,
                 pyExSide: float, pattern1: float, pattern3: float, pattern5: float) -> None:
        self.home = home
        self.draw = draw
        self.away = away
        self.powerRank = powerRank
        self.resultPerc = resultPerc
        self.pyEx = pyEx
        self.pyExSide = pyExSide
        self.pattern1 = pattern1
        self.pattern3 = pattern3
        self.pattern5 = pattern5
