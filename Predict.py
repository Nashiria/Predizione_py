import math

import weightkey,Team,Match
from Odd import Odd
def predictmatch(m,k,t1,t2,l):
    decideRates(m,k,t1,t2,l)
    decideResult(m,k)
    decideScore(m,t1,t2)
    return m
def AddOdd(m,o,d):
    if(m.machineWinHome==None):
        m.machineWinHome=0
    if(m.machineWinAway==None):
        m.machineWinAway=0
    m.machineWinHome+=o.hw*d;m.machineWinAway+=o.aw*d
    return m
def PythagoreanExpectation(hometeam,awayteam):
    hometeamt = pow(hometeam.totalGoals, 1.22777) / ( pow(hometeam.totalGoals, 1.0723880529403687) +  pow(hometeam.totalConcede, 1.1272480487823486)) * 2.4999730587005615 * hometeam.totalMatch
    awayteamt = pow(awayteam.totalGoals, 1.22777) / ( pow(awayteam.totalGoals, 1.0723880529403687) + pow(awayteam.totalConcede, 1.1272480487823486)) * 2.4999730587005615 * awayteam.totalMatch
    total = hometeamt + awayteamt
    htr = hometeamt / total
    atr = awayteamt / total
    toReturn = Odd(0)
    toReturn.hw = htr
    toReturn.aw = atr
    return toReturn
def PythagoreanExpectationWithSides(hometeam,awayteam):
    hometeamt = pow(hometeam.homeGoals, 1.22777) / ( pow(hometeam.homeGoals, 1.0723880529403687) +  pow(hometeam.homeConcede, 1.1272480487823486)) * 2.4999730587005615 * hometeam.homeMatch
    awayteamt = pow(awayteam.awayGoals, 1.22777) / ( pow(awayteam.awayGoals, 1.0723880529403687) + pow(awayteam.awayConcede, 1.1272480487823486)) * 2.4999730587005615 * awayteam.awayMatch
    total = hometeamt + awayteamt
    htr = hometeamt / total
    atr = awayteamt / total
    toReturn = Odd(0)
    toReturn.hw = htr
    toReturn.aw = atr
    return toReturn
def calculateResultPerc(currentLeague,team1,team2):
    hometeam_HomeGoals = team1.homeGoals
    hometeam_HomeMatches = team1.homeMatch
    awayteam_AwayMatches = team2.awayMatch
    awayteam_AwayGoals = team2.awayGoals
    hometeam_HomeConceded = team1.homeConcede
    awayteam_AwayConceded = team2.awayConcede
    league_AwayConceded = currentLeague.homescored
    league_HomeConceded = currentLeague.awayscored
    league_HomeGoals = currentLeague.homescored
    league_AwayGoals = currentLeague.awayscored
    league_TotalMatch = currentLeague.totalmatch
    if (hometeam_HomeGoals == 0):
        hometeam_HomeGoals = 1
    if (hometeam_HomeMatches == 0):
        hometeam_HomeMatches = 1
    if (awayteam_AwayMatches == 0):
        awayteam_AwayMatches = 1
    if (awayteam_AwayGoals == 0):
        awayteam_AwayGoals = 1
    if (hometeam_HomeConceded == 0):
        hometeam_HomeConceded = 1
    if (awayteam_AwayConceded == 0):
        awayteam_AwayConceded = 1
    if (league_AwayConceded == 0):
        league_AwayConceded = 1
    if (league_HomeConceded == 0):
        league_HomeConceded = 1
    if (league_HomeGoals == 0):
        league_HomeGoals = 1
    if (league_AwayGoals == 0):
        league_AwayGoals = 1
    if (league_TotalMatch == 0):
        league_TotalMatch = 1
    hometeam_AttackStrenght = (hometeam_HomeGoals / hometeam_HomeMatches) * (league_HomeGoals / league_TotalMatch)
    awayteam_AttackStrenght = (awayteam_AwayGoals / awayteam_AwayMatches) * (league_AwayGoals / league_TotalMatch)
    hometeam_DefenseStrength = (hometeam_HomeConceded / hometeam_HomeMatches) * (league_HomeConceded / league_TotalMatch)
    awayteam_DefenseStrength = (awayteam_AwayConceded / awayteam_AwayMatches) * (league_AwayConceded / league_TotalMatch)
    if (awayteam_AwayConceded == 0):
        awayteam_DefenseStrength = 2.0
    if (hometeam_HomeConceded == 0):
        hometeam_DefenseStrength = 2.0
    hometeam_PossibleGoals = hometeam_AttackStrenght / awayteam_DefenseStrength * (league_HomeGoals / league_TotalMatch)
    awayteam_PossibleGoals = awayteam_AttackStrenght / hometeam_DefenseStrength * (league_AwayGoals / league_TotalMatch)
    toReturn = Odd(0)
    toReturn.hw = round(10000.0 * awayteam_PossibleGoals / (hometeam_PossibleGoals + awayteam_PossibleGoals) / 10000.0)
    toReturn.aw = round(10000.0 * awayteam_PossibleGoals / (hometeam_PossibleGoals + awayteam_PossibleGoals) / 10000.0)
    return toReturn
def fillodds(m):
      m.machineWinAway=1-m.machineWinHome
      machineDrawRatio=abs(m.machineWinHome-m.machineWinAway)
      while(machineDrawRatio>0.4):
          machineDrawRatio/=2
      left=1-machineDrawRatio
      m.machineHomeRatio=left*m.machineWinHome/(m.machineWinHome+m.machineWinAway)
      m.machineAwayRatio=left*m.machineWinAway/(m.machineWinHome+m.machineWinAway)
def PowerRank(hometeam, awayteam):
    probofelo1win = 1.0 / pow(10.0, (awayteam.elo - hometeam.elo) / 400.0) / 2.0
    probofelo2win = 1.0 / pow(10.0, (hometeam.elo - awayteam.elo) / 400.0) / 2.0
    draw = abs((probofelo1win - probofelo2win))
    formula = (2.0 * pow(draw, 2.0) / 75.0 - 47.0 * draw / 30.0 + 33.0) / 100.0
    total = probofelo1win + probofelo2win
    probofelo1win /= total
    probofelo2win /= total
    if (probofelo1win < 0.0) :
      probofelo1win = -probofelo1win
      probofelo2win += 2.0 * probofelo1win
    if (probofelo2win < 0.0) :
      probofelo2win = -probofelo2win
      probofelo1win += probofelo2win
    currentOdd=Odd(0)
    currentOdd.hw = probofelo1win
    currentOdd.aw = probofelo2win
    return currentOdd
def decideRates(m,k,t1,t2,l):
    m.machineAwayRatio = 0
    m.machineHomeRatio = 0
    m.machineDrawRatio = 0
    if (t1.totalMatch > 0 and t2.totalMatch > 0):
        if (t1.totalGoals > 0 and t2.totalGoals > 0 and t1.totalConcede > 0 and t2.totalConcede > 0):
            if (t1.homeGoals > 0 and t2.homeConcede > 0 and t1.awayConcede > 0 and t2.awayGoals > 0):
                m = AddOdd(m, PythagoreanExpectationWithSides(t1, t2), k.pyExSide)
                m = AddOdd(m, PythagoreanExpectation(t1, t2), k.pyEx)
                m = AddOdd(m, calculateResultPerc(l, t1, t2),k.resultPerc)
    m = AddOdd(m, PowerRank(t1, t2), k.powerRank)
    m = fillodds(m)
    return m
def decideResult(m,k):
    hProb=m.machineHomeRatio*k.home
    dProb=m.machineDrawRatio*k.draw
    aProb=m.machineAwayRatio*k.away
    total=hProb+dProb+aProb
    hProb=hProb/total
    dProb=dProb/total
    aProb=aProb/total
    if(hProb>dProb and hProb>aProb):
        m.machinePredict="H"
    elif(dProb>hProb and dProb>aProb):
        m.machinePredict="D"
    elif(aProb>dProb and aProb>hProb):
        m.machinePredict="A"
    return m
def poisson(mean):
    return math.ceil(mean)
def decideScore(m, t1, t2):
    team1 = t1
    team2 = t2
    hometeam_HomeGoals = team1.totalGoals
    hometeam_HomeMatches = team1.totalMatch
    awayteam_AwayMatches = team2.totalMatch
    awayteam_AwayGoals = team2.totalGoals
    hometeam_HomeConceded = team1.totalConcede
    awayteam_AwayConceded = team2.totalConcede
    if (hometeam_HomeGoals == 0):
        hometeam_HomeGoals = 1
    if (hometeam_HomeMatches == 0):
        hometeam_HomeMatches = 1
    if (awayteam_AwayMatches == 0):
        awayteam_AwayMatches = 1
    if (awayteam_AwayGoals == 0):
        awayteam_AwayGoals = 1
    if (hometeam_HomeConceded == 0):
        hometeam_HomeConceded = 1
    if (awayteam_AwayConceded == 0):
        awayteam_AwayConceded = 1
    hometeam_AttackStrenght = (hometeam_HomeGoals / hometeam_HomeMatches)
    awayteam_AttackStrenght = (awayteam_AwayGoals / awayteam_AwayMatches)
    hometeam_DefenseStrength = (hometeam_HomeConceded / hometeam_HomeMatches)
    awayteam_DefenseStrength = (awayteam_AwayConceded / awayteam_AwayMatches)
    if (awayteam_AwayConceded == 0):
        awayteam_DefenseStrength = 2
    if (hometeam_HomeConceded == 0):
        hometeam_DefenseStrength = 2
    hometeam_PossibleGoals = (hometeam_AttackStrenght / awayteam_DefenseStrength)
    awayteam_PossibleGoals = (awayteam_AttackStrenght / hometeam_DefenseStrength)
    expectedGoals1 = 0
    expectedGoals2 = 0
    m.homeTeamGoalRatio = hometeam_PossibleGoals
    m.awayTeamGoalRatio = awayteam_PossibleGoals
    trys = 50
    if (((m.result == "F") and (m.machinePredict == "H")) or (m.result == "H")):
        while (expectedGoals1 <= expectedGoals2):
            expectedGoals2 = poisson(awayteam_PossibleGoals)
            expectedGoals1 = poisson(hometeam_PossibleGoals)
            trys -= 1
            if (trys < 0):
                expectedGoals2 = poisson(hometeam_PossibleGoals)
                expectedGoals1 = expectedGoals2 + 1
    if (((m.result == "F") and (m.machinePredict == "D")) or (m.result == "D")):
        expectedGoals1 = poisson((hometeam_PossibleGoals + awayteam_PossibleGoals) / 2)
        expectedGoals2 = expectedGoals1
    if (((m.result == "F") and (m.machinePredict == "A")) or (m.result == "A")):
        while (expectedGoals1 >= expectedGoals2):
            expectedGoals2 = poisson(awayteam_PossibleGoals)
            expectedGoals1 = poisson(hometeam_PossibleGoals)
            trys -= 1
            if (trys < 0):
                expectedGoals1 = poisson(hometeam_PossibleGoals)
                expectedGoals2 = expectedGoals1 + 1
    m.machineHomeScore = expectedGoals1
    m.machineAwayScore = expectedGoals2
    m.machineGoalCount = m.machineHomeScore + m.machineAwayScore
    if (m.result != "F"):
        m.GoalCount = m.home_score + m.away_score
    m.CorrectGoalCount = (m.machineGoalCount == m.GoalCount)
    m.CorrectResult = (m.result == m.machinePredict)
    m.CorrectHomeScore = (m.home_score == m.machineHomeScore)
    m.CorrectAwayScore = (m.away_score == m.machineAwayScore)
    return m
