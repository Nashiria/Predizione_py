# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = match_from_dict(json.loads(json_string))

from typing import Any, TypeVar, Type, cast

T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class Match:
    home_team: str
    away_team: str
    home_score: int
    away_score: int
    result: str

    def __init__(self, home_team: str, away_team: str, home_score: int, away_score: int, result: str) -> None:
        self.home_team = home_team
        self.away_team = away_team
        self.home_score = home_score
        self.away_score = away_score
        self.result = result

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


def match_from_dict(s: Any) -> Match:
    return Match.from_dict(s)


def match_to_dict(x: Match) -> Any:
    return to_class(Match, x)
