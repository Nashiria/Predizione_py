import Match,json,League,Predict,weightkey
from Team import Team

with open('soccer_2001-2020 2 .json', 'r') as outfile:
    f=outfile.read()
    database=json.loads(f)
def simLeague(l,k):
    for team in l.teams:
        t=Team(team)
        l.Teamlist.append(t)

    for match in l.matches:
        team1id=0
        team2id=0

        for team in l.Teamlist:
            if team.teamname == match.home_team:
                team1id=l.Teamlist.index(team)
            if team.teamname == match.away_team:
                team2id = l.Teamlist.index(team)
        match=Predict.predictmatch(match,k,l.Teamlist[team1id],l.Teamlist[team2id],l)
        l.updatewresult(match.home_team,match.away_team,match.home_score,match.away_score)
        l.totalmatch+=1
        if match.result == "H":
            l.homewin += 1
        if match.result=="D":
            l.draw+=1
        if match.result=="A":
            l.awaywin+=1
        l.homescored+=match.home_score
        l.awayscored+=match.away_score
        l.results.append(match)

    print(type(l))
    return l
def leagueimport(year,league):
    l=League.league_from_dict(database[year][league])
    l.leagueName=league
    l.season=year

    return l

def keytrans(text):
    newk=weightkey.weightkey
    text=text.replace("Home:","").replace("Draw:","").replace("Away:","").replace("powerRank:","").replace("resultPerc:","").replace("pyEx:","").replace("pyExSide:","").replace("pattern1:","").replace("pattern3:","").replace("pattern5:","")
    text=text.split(" ")
    newk.home = float(text[0])
    newk.draw = float(text[1])
    newk.away = float(text[2])
    newk.powerRank = float(text[3])
    newk.resultPerc = float(text[4])
    newk.pyEx = float(text[5])
    newk.pyExSide = float(text[6])
    newk.pattern1 = float(text[7])
    newk.pattern3 = float(text[8])
    newk.pattern5 = float(text[9])
    return newk

l=leagueimport("2020","Premier League")
k=keytrans("Home:228.81533101045298 Draw:216.0526315789474 Away:223.94736842105263 powerRank:0.0 resultPerc:-3.0 pyEx:-2.0 pyExSide:-9.0 pattern1:0.0 pattern3:0.0 pattern5:0.0")

l=simLeague(l,k)

correct=0
wrong=0
for match in l.results:
    print(match.result,match.machinePredict,match.machineHomeRatio,match.machineDrawRatio,match.machineAwayRatio)
    if match.result==match.machinePredict:
        correct+=1
    else:
        wrong+=1
print(correct/(correct+wrong))