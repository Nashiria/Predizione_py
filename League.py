# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = league_from_dict(json.loads(json_string))

from typing import Any, List, TypeVar, Callable, Type, cast
from Team import Team

T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class Match:
    home_team: str
    away_team: str
    home_score: int
    away_score: int
    result: str
    GoalCount: int
    League: str
    Year: int
    Division: int
    Country: str
    result: str
    machinePredict: str
    machineWinHome: float
    machineWinAway: float
    machineHomeRatio: float
    machineDrawRatio: float
    machineAwayRatio: float
    machineHomeScore: int
    machineAwayScore: int
    machineGoalCount: int
    CorrectResult: bool
    CorrectHomeScore: bool
    CorrectAwayScore: bool
    CorrectGoalCount: bool
    homeTeamGoalRatio: float
    awayTeamGoalRatio: float
    def __init__(self, home_team: str, away_team: str, home_score: int, away_score: int, result: str) -> None:
        self.home_team = home_team
        self.away_team = away_team
        self.home_score = home_score
        self.away_score = away_score
        self.result = result
        self.GoalCount = 0
        self.League = ""
        self.Year = 0
        self.Division = 0
        self.Country = ""
        self.machinePredict = ""
        self.machineWinHome = 0
        self.machineWinAway = 0
        self.machineHomeRatio = 0
        self.machineDrawRatio = 0
        self.machineAwayRatio = 0
        self.machineHomeScore = 0
        self.machineAwayScore = 0
        self.machineGoalCount = 0
        self.CorrectResult = False
        self.CorrectHomeScore = False
        self.CorrectAwayScore = False
        self.CorrectGoalCount = False
        self.homeTeamGoalRatio = 0
        self.awayTeamGoalRatio = 0

    @staticmethod
    def from_dict(obj: Any) -> 'Match':
        assert isinstance(obj, dict)
        home_team = from_str(obj.get("homeTeam"))
        away_team = from_str(obj.get("awayTeam"))
        home_score = from_int(obj.get("homeScore"))
        away_score = from_int(obj.get("awayScore"))
        result = from_str(obj.get("result"))
        return Match(home_team, away_team, home_score, away_score, result)

    def to_dict(self) -> dict:
        result: dict = {}
        result["homeTeam"] = from_str(self.home_team)
        result["awayTeam"] = from_str(self.away_team)
        result["homeScore"] = from_int(self.home_score)
        result["awayScore"] = from_int(self.away_score)
        result["result"] = from_str(self.result)
        return result


class League:
    teams: List[str]
    matches: List[Match]
    results: List[Match]
    leagueName: str
    year:int
    leaguesize:int
    totalmatch:int
    homewin:int
    draw:int
    awaywin:int
    homescored:int
    awayscored:int
    Teamlist:List[Team]
    def __init__(self, teams: List[str], matches: List[Match]) -> None:
        self.teams = teams
        self.matches = matches
        self.year = 0
        self.totalmatch = 0
        self.homewin = 0
        self.draw = 0
        self.awaywin = 0
        self.homescored = 0
        self.awayscored = 0
        self.Teamlist=[]
        self.results = []

    def getteamid(self,name):
        for team in self.Teamlist:
            if team.teamname==name:
                    return self.Teamlist.index(team)
            else:
                return -1
    def updatewresult(self,team1,team2,score1,score2):
        t1=self.getteamid(team1)
        t2=self.getteamid(team2)
        result=""
        if score1>score2:
            result="H"
        if score2>score1:
            result="A"
        else:
            result="D"
        self.Teamlist[t1].homeGoals += score1
        self.Teamlist[t1].homeConcede += score2
        self.Teamlist[t2].awayGoals += score2
        self.Teamlist[t2].awayConcede += score1
        self.Teamlist[t1].totalGoals += score1
        self.Teamlist[t1].totalMatch += 1
        self.Teamlist[t1].totalConcede += score2
        self.Teamlist[t2].totalGoals += score2
        self.Teamlist[t2].totalMatch += 1
        self.Teamlist[t2].totalConcede += score1
        self.Teamlist[t1].homeMatch += 1
        self.Teamlist[t2].awayMatch += 1
        if result == "H":
            self.Teamlist[t1].form += "W"
            self.Teamlist[t1].win += 1
            self.Teamlist[t1].homeWin += 1
            self.Teamlist[t1].homeForm += "W"
            self.Teamlist[t2].form += "L"
            self.Teamlist[t2].loses += 1
            self.Teamlist[t2].awayLoses += 1
            self.Teamlist[t2].awayForm += "L"
            self.Teamlist[t1].points+=3
        if result == "D":
            self.Teamlist[t1].form += "D"
            self.Teamlist[t1].draws += 1
            self.Teamlist[t1].homeDraws += 1
            self.Teamlist[t1].homeForm += "D"
            self.Teamlist[t2].form += "D"
            self.Teamlist[t2].draws += 1
            self.Teamlist[t2].awayDraws += 1
            self.Teamlist[t2].awayForm += "D"
            self.Teamlist[t1].points += 1
            self.Teamlist[t2].points += 1
        if result == "A":
            self.Teamlist[t1].form += "L"
            self.Teamlist[t1].loses += 1
            self.Teamlist[t1].homeLoses += 1
            self.Teamlist[t1].homeForm += "L"
            self.Teamlist[t2].form += "W"
            self.Teamlist[t2].win += 1
            self.Teamlist[t2].awayWin += 1
            self.Teamlist[t2].awayForm += "W"
            self.Teamlist[t2].points += 3
    @staticmethod
    def from_dict(obj: Any) -> 'League':
        assert isinstance(obj, dict)
        teams = from_list(from_str, obj.get("teams"))
        matches = from_list(Match.from_dict, obj.get("matches"))
        return League(teams, matches)
    def to_dict(self) -> dict:
        result: dict = {}
        result["teams"] = from_list(from_str, self.teams)
        result["matches"] = from_list(lambda x: to_class(Match, x), self.matches)
        return result


def league_from_dict(s: Any) -> League:
    return League.from_dict(s)


def league_to_dict(x: League) -> Any:
    return to_class(League, x)
