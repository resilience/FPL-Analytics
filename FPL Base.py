import requests
import urllib, json
import csv
import os
import numpy as np
import sys
from unidecode import unidecode
from urllib.request import FancyURLopener


mz = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
apple = ' AppleWebKit/537.36 (KHTML, like Gecko) '
chrome = 'Chrome/66.0.3359.181 Safari/537.36'


class MyOpener(FancyURLopener):version = mz+apple+chrome
myopener = MyOpener()



# player ID's selected for evaluation
#playerIDArray =['372']
playerIDArray =['253','372','122','23','270','246','275','302','172']

# ______________________________RANKING__________________________________


# https://fantasy.premierleague.com/drf/fixtures/ page shows match id's going up to 224+
# can use this to
# find each matches participants using "team_a":11,"team_h":14  and scores using "team_h_score":2,"team_a_score":1
#
# Highest score wins the match
# Teams receive three points for a win and one point for a draw
# Rank Team accordingly

# Using the ranking we can then find out the teams in the current difficulty bubble

apiFixturesURL = 'https://fantasy.premierleague.com/drf/fixtures/'
apiFixturesSearch = myopener.open(apiFixturesURL.strip()).read()
fplFixturesData = json.loads(apiFixturesSearch.decode('utf-8'))
fixtures = list(range(0, 233))

teamMatrix = np.zeros((20, 3))
teamMatrix[:,0] = np.arange(1, 21)

for fixture in fixtures:
        try:
            id = fplFixturesData[fixture].get('id')
            print('match id: ',id)
            scoreA = fplFixturesData[fixture].get('team_a_score')
            scoreH = fplFixturesData[fixture].get('team_h_score')
            teamA = fplFixturesData[fixture].get('team_a')
            teamH = fplFixturesData[fixture].get('team_h')
            print("Away Team: ", teamA, ", score: ", scoreA)
            print("Home Team: ", teamH, ", score: ", scoreH)

            if scoreA > scoreH:
                teamMatrix[teamA-1,1] = teamMatrix[teamA-1,1]+3
                print("team ", teamA," wins")
                print("printing matrix: teamMatrix ", teamMatrix)
                print("printing matrix: teamMatrix[teamA][0] ", teamMatrix[teamA][0])
                print("printing matrix: teamMatrix[teamA][1] ", teamMatrix[teamA][1])

            elif scoreA < scoreH:
                teamMatrix[teamH-1, 1] = teamMatrix[teamH-1, 1] + 3
                print("team ", teamH," wins")
                print("printing matrix: teamMatrix ", teamMatrix)
                print("printing matrix: teamMatrix[teamA][0] ", teamMatrix[teamH][0])
                print("printing matrix: teamMatrix[teamA][1] ", teamMatrix[teamH][1])
            elif scoreA == scoreH:
                print("teams draw")
                teamMatrix[teamA-1, 1] = teamMatrix[teamA-1, 1] + 1
                teamMatrix[teamH-1, 1] = teamMatrix[teamH-1, 1] + 1
                print("team A teamMatrix[teamA] ",teamMatrix[teamA])
                print("team H teamMatrix[teamH] ", teamMatrix[teamH])

        except (IndexError, TypeError) as iE:

            continue
print("All matches swept")

# ____________________ SORT RANKING___________________
teamMatrix = teamMatrix[teamMatrix[:, 1].argsort()[::-1]]
print(teamMatrix)


# ________________________________PLAYER ANALYSIS_______________________________

for player in playerIDArray:

    apiPlayerURL = 'https://fantasy.premierleague.com/drf/element-summary/'
    param = player

    apiSummaryURL = 'https://fantasy.premierleague.com/drf/bootstrap-static'

    apiTeamURL = 'https://fantasy.premierleague.com/drf/bootstrap'
    try:
        this = apiPlayerURL + param

    except ValueError as vE:
        print('Value Error on ' + param)
        continue

    try:
        apiPlayerSearch = myopener.open(this.strip()).read()
        apiSummarySearch = myopener.open(apiSummaryURL.strip()).read()


    except ValueError as vE:
        print('Value Error on ' + param)
        continue

    fplPlayerData = json.loads(apiPlayerSearch.decode('utf-8'))
    fplSummaryData = json.loads(apiSummarySearch.decode('utf-8'))

    #print(fplSummaryData)
    gameweeks = list(range(0, 37))
    try:
        rounds = list()
        points = list()
        for gameweek in gameweeks:
            round = fplPlayerData['history'][gameweek].get('round')
            rounds.append(round)
            point = fplPlayerData['history'][gameweek].get('total_points')
            points.append(point)

            print("round: ", round, " points: ", point)

    except IndexError as iE:

        print()
    rollingAverage = sum(points[-10:])/10
    print("rolling average ( 10 weeks ) ",rollingAverage)
    playerTeam = fplPlayerData['fixtures'][0].get('opponent_name')
    nextOpponent = fplPlayerData['fixtures'][0].get('opponent_name')
    opponentHome = fplPlayerData['fixtures'][0].get('is_home')

    if opponentHome == True:
        opponentID = fplPlayerData['fixtures'][0].get('team_a')
    elif opponentHome == False:

        opponentID = fplPlayerData['fixtures'][0].get('team_h')

    print('nextOpponent: ',nextOpponent)
    print('opponent playing Home? ',opponentHome)
    print('next opponent ID: ', opponentID)


    # ________________________ DIFFICULTY BUBBLE___________________________

    # The difficulty bubble is the range (1-5) opponents of the same calibre as the selected players next opponents
    # The difficulty bubble thus showcases the average points expected for the next match, based on the historical data
    # of similar opponent strength and the points generated against them.

    teamMatrix[:, 2] = np.arange(1, 21)
    teamMatrix = teamMatrix[teamMatrix[:, 0].argsort()]
    team = fplSummaryData['elements'][int(player)].get('team')
    print('Team: ', team)

    print(teamMatrix)

    # not sure why, the below is not returning the right values, change 0 to 1 or 2 and test

    oR = teamMatrix[opponentID - 1][2]
    print('Opponent Rank: ', oR)

    difficultyRank = [oR-2, oR-1, oR, oR+1, oR+2]
    print(difficultyRank)
    difficultyBubble = [opponentID]







    # ________________________ EXPLOSIVENESS _____________________

    # Explosiveness is calculated as 1% for each fixture in the difficulty bubble
    # that has a chance of exploding ( gaining more than 10 points )
    # Chance for exploding is calculated by comparing the explosions that have occurred
    # against the calibre of fixtures playing.
    # for instance if Liverpool is the top team, and the player selected has exploded against liverpool
    # the player gains 1% for each team in his difficulty bubble that is weaker than Liverpool

    # _________________________CSV OUTPUT________________________

    # Store data as 'n collection in CSV for viewing in excel or upload to site

'''
    opponenentRank =
    oR = opponentRank
    difficultyBubbleFixtures = [ oR-2, oR-1 ,oR ,oR +1, oR +2]
    difficultyBubbleGWs =


    nextFixtureAverage = difficultyBubblePoints / difficultyBubbleFixtures

'''
