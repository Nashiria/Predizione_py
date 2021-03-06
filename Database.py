import League
import Predict
import json
import random
import weightkey

from Accuracy import Accuracy
from Team import Team

guessafterpercentageofmatches = 10
with open('soccer_2001-2020 2 .json', 'r') as outfile:
    f = outfile.read()
    database = json.loads(f)


def simLeague(l, k):
    for team in l.teams:
        t = Team(team)
        l.Teamlist.append(t)
    for match in l.matches:
        team1id = 0
        team2id = 0
        for team in l.Teamlist:
            if team.teamname == match.home_team:
                team1id = l.Teamlist.index(team)
            if team.teamname == match.away_team:
                team2id = l.Teamlist.index(team)
        if (l.matches.index(match) > len(l.matches) / guessafterpercentageofmatches):
            match = Predict.predictmatch(match, k, l.Teamlist[team1id], l.Teamlist[team2id], l)
        l.updatewresult(team1id, team2id, match.home_score, match.away_score)
        # t1=l.Teamlist[team1id]
        # t2=l.Teamlist[team2id]
        # print(t1.teamname,t1.form,t1.totalGoals,t1.totalConcede)
        l.totalmatch += 1
        if match.result == "H":
            l.homewin += 1
        if match.result == "D":
            l.draw += 1
        if match.result == "A":
            l.awaywin += 1
        l.homescored += match.home_score
        l.awayscored += match.away_score
        l.results.append(match)
    return l


def leagueimport(year, league):
    l = League.league_from_dict(database[year][league])
    l.leagueName = league
    l.season = year

    return l


def getRandom(min, max):
    random.randint(min, max)


def FixKeyAcc(acc):
    crKey = acc.key
    hk = acc.guessedHomeRatio
    dk = acc.guessedDrawRatio
    ak = acc.guessedAwayRatio
    if (hk > dk + 0.1):
        crKey.draw += (acc.guessedHomeRatio - acc.guessedDrawRatio) * 30.0

    if (hk > ak + 0.1):
        crKey.away += (acc.guessedHomeRatio - acc.guessedAwayRatio) * 30.0

    if (ak > dk + 0.1):
        crKey.draw += (acc.guessedAwayRatio - acc.guessedDrawRatio) * 30.0

    if (ak > hk + 0.1):
        crKey.home += (acc.guessedAwayRatio - acc.guessedHomeRatio) * 30.0
    if (dk > ak + 0.1):
        crKey.away += (acc.guessedDrawRatio - acc.guessedAwayRatio) * 30.0
    if (dk > hk + 0.1):
        crKey.home += (acc.guessedDrawRatio - acc.guessedHomeRatio) * 30.0
    acc.key = crKey
    return crKey


def randomKey():
    toReturn = keytrans(
        "Home:228.81533101045298 Draw:216.0526315789474 Away:223.94736842105263 powerRank:0.0 resultPerc:-3.0 pyEx:-2.0 pyExSide:-9.0 pattern1:0.0 pattern3:0.0 pattern5:0.0")
    toReturn.home = 100.0
    toReturn.draw = 100.0
    toReturn.away = 100.0
    toReturn.powerRank = random.randint(-1000, 1000) / 100
    toReturn.resultPerc = random.randint(-1000, 1000) / 100
    toReturn.pyEx = random.randint(-1000, 1000) / 100
    toReturn.pyExSide = random.randint(-1000, 1000) / 100
    toReturn.pattern1 = 0.0
    toReturn.pattern3 = 0.0
    toReturn.pattern5 = 0.0
    return toReturn


def perc(currD):
    return (int(currD * 100.0) / 100.0)


def PrintkeyAccuracy(curAccuracy):
    print("Accuracy Ratios: Total:%" +
          str(perc(curAccuracy.resultRatio * 100.0)) + " H:%" +
          str(perc(curAccuracy.homeRatio * 100.0)) + " D:%" +
          str(perc(curAccuracy.drawRatio * 100.0)) + " A:%" +
          str(perc(curAccuracy.awayRatio * 100.0)) + " H:" +
          str(perc(curAccuracy.key.home)) + " D:" +
          str(perc(curAccuracy.key.draw)) + " A:" +
          str(perc(curAccuracy.key.away)))


def findBetterKey(l, k):
    acc = Accuracy(l.leagueName)
    alltries = 0
    lasth = 0.0
    lastd = 0.0
    lasta = 0.0
    count = 0
    currentkeytry = 0
    maxacc = acc
    reqres = 0.58
    reqh = 0.1
    reqd = 0.1
    reqa = 0.1
    maxleague = l
    CurrentLeague = l
    if (CurrentLeague.leagueName == "Premier League"):
        reqres = 0.40
    if (CurrentLeague.leagueName == "Mahalle"):
        reqres = 0.51
    if (CurrentLeague.leagueName == "Eredivisie"):
        reqres = 0.52
    if (CurrentLeague.leagueName == "Ligue 1"):
        reqres = 0.52
    if (CurrentLeague.leagueName == "Bundesliga"):
        reqres = 0.52
    if (CurrentLeague.leagueName == "Superlig"):
        reqres = 0.52
    if (CurrentLeague.leagueName == "La Liga"):
        reqres = 0.52
    if (CurrentLeague.leagueName == "Serie A"):
        reqres = 0.52
    if (CurrentLeague.leagueName == "Liga NOS"):
        reqres = 0.52
    if (CurrentLeague.leagueName == "NBA"):
        reqres = 0.50
        reqh = 0.5
        reqa = 0.5
        reqd = 0
    lig = CurrentLeague.leagueName
    trycount = 0
    rats = []
    didntchange = 0
    lastmax = 0
    maxleague = 0
    while ((
                   acc.resultRatio < reqres + 0.001 or acc.homeRatio < reqh or acc.drawRatio < reqd or acc.awayRatio < reqa) and trycount < 10000):
        trycount += 1
        ++alltries
        ++currentkeytry
        ++count
        CurrentLeague = leagueimport("2019", "Premier League")
        CurrentLeague = simLeague(CurrentLeague, k)
        acc = giveacc(CurrentLeague, k)
        if lastmax == 0:
            lastmax = acc

        if acc.resultRatio > lastmax.resultRatio:
            lastmax = acc
            maxleague = CurrentLeague
            PrintkeyAccuracy(lastmax)
        condition = ((acc.resultRatio < reqres or acc.homeRatio < reqh or acc.drawRatio < reqd) or acc.awayRatio < reqa)
        if acc.correctAway in rats and acc.correctDraw in rats and acc.correctAway in rats:
            didntchange += 1
        if rats == []:
            rats = [acc.correctAway, acc.correctDraw, acc.correctAway]
        if didntchange > 10:
            k = randomKey()
            count = 0
            currentkeytry = 0
            rats = []
            didntchange = 0
        if (condition):
            --count
            k = FixKeyAcc(acc)
            rats = [acc.correctAway, acc.correctDraw, acc.correctAway]

        if (lig == "NBA"):
            acc.drawRatio = 1
            acc.guessedDrawRatio = 1
        if (acc.homeRatio > reqh and acc.awayRatio > reqa and acc.drawRatio > reqd and acc.resultRatio > reqres):
            print("")
            PrintkeyAccuracy(acc)
            print("Home:" + str(acc.key.home) + " Draw:" + str(acc.key.draw)
                  + " Away:" + str(acc.key.away) + " powerRank:" + str(acc.key.powerRank)
                  + " resultPerc:" + str(acc.key.resultPerc) + " pyEx:" + str(acc.key.pyEx)
                  + " pyExSide:" + str(acc.key.pyExSide) + " pattern1:" + str(acc.key.pattern1)
                  + " pattern3:" + str(acc.key.pattern3) + " pattern5:" + str(acc.key.pattern5))
            maxacc = acc
            if (acc.resultRatio > reqres):
                break
        acc = maxacc
        if (lig == "NBA"):
            acc.drawRatio = 1
            acc.guessedDrawRatio = 1
        # print("Home:" + str(acc.key.home) + " Draw:" + str(acc.key.draw)+ " Away:" + str(acc.key.away) + " powerRank:" + str(acc.key.powerRank)+ " resultPerc:" + str(acc.key.resultPerc) + " pyEx:" + str(acc.key.pyEx)+ " pyExSide:" + str(acc.key.pyExSide) + " pattern1:" + str(acc.key.pattern1)+ " pattern3:" + str(acc.key.pattern3) + " pattern5:" + str(acc.key.pattern5))
        Templist = []
        teamcount = len(CurrentLeague.Teamlist)
        while (len(Templist) != teamcount):
            indexofmaxteam = 0
            valueofmaxteam = 0
            for team in CurrentLeague.Teamlist:
                team.points = 3 * team.win + team.draws
                valueofcurrentteam = 1000 * (team.points) + (team.totalGoals - team.totalConcede)
                if (valueofcurrentteam > valueofmaxteam):
                    valueofmaxteam = valueofcurrentteam
                    indexofmaxteam = CurrentLeague.Teamlist.index(team)
            Templist.append(CurrentLeague.Teamlist[indexofmaxteam])
            CurrentLeague.Teamlist.remove(CurrentLeague.Teamlist[indexofmaxteam])
        CurrentLeague.Teams = Templist
    print("")
    PrintkeyAccuracy(lastmax)
    print("Home:" + str(lastmax.key.home) + " Draw:" + str(lastmax.key.draw)
          + " Away:" + str(lastmax.key.away) + " powerRank:" + str(lastmax.key.powerRank)
          + " resultPerc:" + str(lastmax.key.resultPerc) + " pyEx:" + str(lastmax.key.pyEx)
          + " pyExSide:" + str(lastmax.key.pyExSide) + " pattern1:" + str(lastmax.key.pattern1)
          + " pattern3:" + str(lastmax.key.pattern3) + " pattern5:" + str(lastmax.key.pattern5))
    print("")
    printleague(maxleague)


def printleague(l):
    teams = l.Teamlist
    points = []
    for team in teams:
        team.leaguePoints = team.win * 3 + team.draws
        points.append(team.win * 3000 + team.draws * 1000 + (team.totalGoals - team.totalConcede))
    points2 = points.copy()
    points2.sort()
    points2.reverse()
    for point in points2:
        team = teams[points.index(point)]
        print(team.teamname, team.win, team.draws, team.loses, team.leaguePoints)

    pass


def keytrans(text):
    newk = weightkey.weightkey
    text = text.replace("Home:", "").replace("Draw:", "").replace("Away:", "").replace("powerRank:", "").replace(
        "resultPerc:", "").replace("pyEx:", "").replace("pyExSide:", "").replace("pattern1:", "").replace("pattern3:",
                                                                                                          "").replace(
        "pattern5:", "")
    text = text.split(" ")
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


def giveacc(l, k):
    currentAccuracy = Accuracy(l.leagueName)
    for curr in l.results:
        if (l.results.index(curr) > len(l.results) / guessafterpercentageofmatches):
            currentAccuracy.totalMatch += 1
            if (curr.machinePredict == "D"):
                currentAccuracy.guessedDraw += 1
            if (curr.machinePredict == "H"):
                currentAccuracy.guessedHome += 1
            if (curr.machinePredict == "A"):
                currentAccuracy.guessedAway += 1
            if (curr.CorrectAwayScore):
                currentAccuracy.correctAwayGoal += 1
            else:
                currentAccuracy.wrongAwayGoal += 1
            if (curr.CorrectHomeScore):
                currentAccuracy.correctHomeGoal += 1
            else:
                currentAccuracy.wrongHomeGoal += 1
            if (curr.CorrectResult):
                if (curr.result == "D"):
                    currentAccuracy.correctDraw += 1
                if (curr.result == "H"):
                    currentAccuracy.correctHome += 1
                if (curr.result == "A"):
                    currentAccuracy.correctAway += 1
                currentAccuracy.correctResult += 1
            else:
                currentAccuracy.wrongResult += 1
                if (curr.result == "D"):
                    currentAccuracy.wrongDraw += 1
                if (curr.result == "H"):
                    currentAccuracy.wrongHome += 1
                if (curr.result == "A"):
                    currentAccuracy.wrongAway += 1
    currentAccuracy.homeGoalRatio = currentAccuracy.correctHomeGoal / currentAccuracy.totalMatch
    currentAccuracy.awayGoalRatio = currentAccuracy.correctAwayGoal / currentAccuracy.totalMatch
    currentAccuracy.resultRatio = currentAccuracy.correctResult / currentAccuracy.totalMatch
    currentAccuracy.homeRatio = currentAccuracy.correctHome / (currentAccuracy.correctHome + currentAccuracy.wrongHome);
    currentAccuracy.drawRatio = currentAccuracy.correctDraw / (currentAccuracy.correctDraw + currentAccuracy.wrongDraw);
    currentAccuracy.awayRatio = currentAccuracy.correctAway / (currentAccuracy.correctAway + currentAccuracy.wrongAway);
    currentAccuracy.guessedAwayRatio = currentAccuracy.guessedAway / currentAccuracy.totalMatch
    currentAccuracy.guessedDrawRatio = currentAccuracy.guessedDraw / currentAccuracy.totalMatch
    currentAccuracy.guessedHomeRatio = currentAccuracy.guessedHome / currentAccuracy.totalMatch
    currentAccuracy.accuracyScore = 0.7 * currentAccuracy.resultRatio + currentAccuracy.awayGoalRatio * 0.1 + currentAccuracy.homeGoalRatio * 0.2
    currentAccuracy.key = k
    currentAccuracy.Season = l.season
    currentAccuracy.league = l.leagueName
    return currentAccuracy


l = leagueimport("2020", "Premier League")
k = keytrans(
    "Home:228.81533101045298 Draw:216.0526315789474 Away:223.94736842105263 powerRank:0.0 resultPerc:-3.0 pyEx:-2.0 pyExSide:-9.0 pattern1:0.0 pattern3:0.0 pattern5:0.0")
findBetterKey(l, k)
