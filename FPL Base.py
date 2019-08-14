import requests
import urllib, json
import csv
import os
import numpy as np
import sys
from unidecode import unidecode
from urllib.request import FancyURLopener
import pymysql
import socket
import sqlite3

socket.getaddrinfo('127.0.0.1', 8080)

conn = pymysql.connect(host='127.0.0.1', user='root', password='hyvemobilepassword', db='fpldb')
c = conn.cursor()

mz = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
apple = ' AppleWebKit/537.36 (KHTML, like Gecko) '
chrome = 'Chrome/66.0.3359.181 Safari/537.36'


class MyOpener(FancyURLopener):version = mz+apple+chrome
myopener = MyOpener()

# params = (player, firstName, secondName, playerRole, playerPrice, rollingAverage, totalpoints, team, cost, nextOpponent, '', '', '', )

c.execute("""CREATE TABLE IF NOT EXISTS playersCurrentStats (
            playerCode integer PRIMARY KEY NOT NULL,
            productFirstName VARCHAR(255) NOT NULL,
            productSecondName VARCHAR(255) NOT NULL,
            playerRole VARCHAR(255) NOT NULL,
            projectedScore real,
            rollingAverage real,
            totalPoints real,
            playerTeam VARCHAR(255) NOT NULL,
            playerPrice real,
            nextOpponent VARCHAR(255) NOT NULL,
            opRank integer,
            opID1 integer,
            opID2 integer,
            opID3 integer,
            opID4 integer,
            opID5 integer,
            playerExplosivity real,
            playerTotalGoals INT NOT NULL,
            playerTotalAssists INT NOT NULL
            )""")

c.execute("""CREATE TABLE IF NOT EXISTS pointsList (
             pointsID integer PRIMARY KEY NOT NULL,
             playerCode INT NOT NULL,
             goalAmount INT NOT NULL,
             assistAmount INT NOT NULL,
             bonusPointAmount INT NOT NULL,
             gameWeek INT NOT NULL,
             yellowCard INT NOT NULL,
             redCard INT NOT NULL,
             minutePlayed INT NOT NULL )""")


c.execute("""CREATE TABLE IF NOT EXISTS players (
             playerCode INT PRIMARY KEY NOT NULL,
             productFirstName VARCHAR(255) NOT NULL,
             productSecondName VARCHAR(255) NOT NULL,
             playerRole VARCHAR(255) NOT NULL,
             totalPoints real )""")

c.execute("""CREATE TABLE IF NOT EXISTS performances (
             performanceID INT PRIMARY KEY NOT NULL,
             playerCode INT NOT NULL,
             gameweek VARCHAR(255) NOT NULL,
             date_year INT NOT NULL,
             goals_scored real,
             assists real,
             clean_sheets real,
             goals_conceded real,
             own_goals real,
             penalties_saved real,
             penalties_missed real,
             yellow_cards real,
             red_cards real,
             saves real,
             bonus real,
             bps real,
             influence float,
             creativity float,
             threat float,
             ict_index float,
             total_points real,
             in_dreamteam VARCHAR(255) NOT NULL
             )""")



# player ID's selected for evaluation
#playerIDArray =[122,118,115,150,391]
playerIDArray = range(1, 526)






# ______________________________RANKING__________________________________


# https://fantasy.premierleague.com/drf/fixtures/ page shows match id's going up to 224+
# can use this to
# find each matches participants using "team_a":11,"team_h":14  and scores using "team_h_score":2,"team_a_score":1
#
# Highest score wins the match
# Teams receive three points for a win and one point for a draw
# Rank Team accordingly

# Using the ranking we can then find out the teams in the current difficulty bubble

def scanMatches():

    gameweeks = range(1, 37)
    performances = range(0, 526)
    for gameweek in gameweeks:
        try:

            print('Gameweek: ',gameweek)
            apiEvents = 'https://fantasy.premierleague.com/api/event/' + str(gameweek) + '/live/'
            print(apiEvents)
            apiEventSearch = myopener.open(apiEvents.strip()).read()
            apiEventsData = json.loads(apiEventSearch.decode('utf-8'))

            print(apiEventsData)
            for performanceID in performances:
                date_year = 2019
                print('performance ID: ', performanceID)

                playerCode = apiEventsData['elements'][performanceID].get('id')
                print('playerCode ', playerCode)
                goals_scored = apiEventsData['elements'][performanceID]['stats'].get('goals_scored')
                assists = apiEventsData['elements'][performanceID]['stats'].get('assists')
                clean_sheets = apiEventsData['elements'][performanceID]['stats'].get('clean_sheets')
                goals_conceded = apiEventsData['elements'][performanceID]['stats'].get('goals_conceded')
                own_goals = apiEventsData['elements'][performanceID]['stats'].get('own_goals')
                penalties_saved = apiEventsData['elements'][performanceID]['stats'].get('penalties_saved')
                penalties_missed = apiEventsData['elements'][performanceID]['stats'].get('penalties_missed')
                yellow_cards = apiEventsData['elements'][performanceID]['stats'].get('yellow_cards')
                red_cards = apiEventsData['elements'][performanceID]['stats'].get('red_cards')
                saves = apiEventsData['elements'][performanceID]['stats'].get('saves')
                bonus = apiEventsData['elements'][performanceID]['stats'].get('bonus')
                bps = apiEventsData['elements'][performanceID]['stats'].get('bps')
                influence = apiEventsData['elements'][performanceID]['stats'].get('influence')
                creativity = apiEventsData['elements'][performanceID]['stats'].get('creativity')
                threat = apiEventsData['elements'][performanceID]['stats'].get('threat')
                ict_index = apiEventsData['elements'][performanceID]['stats'].get('ict_index')
                total_points = apiEventsData['elements'][performanceID]['stats'].get('total_points')
                in_dreamteam = apiEventsData['elements'][performanceID]['stats'].get('in_dreamteam')

                values = (performanceID, playerCode, gameweek, date_year, goals_scored, assists, clean_sheets, goals_conceded, own_goals, penalties_saved, penalties_missed,yellow_cards,red_cards,saves,bonus,bps,influence,creativity,threat,ict_index,total_points,in_dreamteam)

                insertSql = """insert into performances( performanceID, playerCode, gameweek, date_year, goals_scored, assists, clean_sheets, goals_conceded, own_goals, penalties_saved, penalties_missed,yellow_cards,red_cards,saves,bonus,bps,influence,creativity,threat,ict_index,total_points,in_dreamteam ) 
                                          values (%s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

                c.execute(insertSql, values)
                conn.commit()
        except pymysql.err.IntegrityError as duplicate:
            print('already done this gameweek')


        except IndexError as iE:
            print('Index Error ', iE)
            break



scanMatches()

def scanPlayers():
    apiFixturesURL = 'https://fantasy.premierleague.com/drf/fixtures/'
    apiFixturesSearch = myopener.open(apiFixturesURL.strip()).read()
    fplFixturesData = json.loads(apiFixturesSearch.decode('utf-8'))
    fixtures = list(range(0, 233))

    teamMatrix = np.zeros((20, 4))
    teamMatrix[:, 0] = np.arange(1, 21)

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
                 #   print("printing matrix: teamMatrix ", teamMatrix)
                 #   print("printing matrix: teamMatrix[teamA][0] ", teamMatrix[teamA][0])
                 #   print("printing matrix: teamMatrix[teamA][1] ", teamMatrix[teamA][1])

                elif scoreA < scoreH:
                    teamMatrix[teamH-1, 1] = teamMatrix[teamH-1, 1] + 3
                    print("team ", teamH," wins")
                   # print("printing matrix: teamMatrix ", teamMatrix)
                  # print("printing matrix: teamMatrix[teamA][0] ", teamMatrix[teamH][0])
                   # print("printing matrix: teamMatrix[teamA][1] ", teamMatrix[teamH][1])
                elif scoreA == scoreH:
                    print("teams draw")
                    teamMatrix[teamA-1, 1] = teamMatrix[teamA-1, 1] + 1
                    teamMatrix[teamH-1, 1] = teamMatrix[teamH-1, 1] + 1
                   # print("team A teamMatrix[teamA] ",teamMatrix[teamA])
                    #print("team H teamMatrix[teamH] ", teamMatrix[teamH])

            except (IndexError, TypeError) as iE:

                continue
    print("All matches swept")

    # ____________________ SORT RANKING___________________
    teamMatrix = teamMatrix[teamMatrix[:, 1].argsort()[::-1]]
    teamMatrix[:, 2] = np.arange(1, 21)
    print(teamMatrix)


    # ________________________________PLAYER ANALYSIS_______________________________
    k = 0
    for player in playerIDArray:

        apiPlayerURL = 'https://fantasy.premierleague.com/api/element-summary/'
        param = player

        apiSummaryURL = 'https://fantasy.premierleague.com/api/bootstrap-static'

        apiTeamURL = 'https://fantasy.premierleague.com/api/bootstrap'
        try:
            this = apiPlayerURL + str(param)

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

        playerData = fplSummaryData['elements']

        for i in playerData:

            if i['id'] == player:
                team = i['team_code']
                firstName = i['first_name']
                secondName = i['second_name']
                cost = i['now_cost']/10
                totalPoints = i['total_points']
                playerRole = i['element_type']
                totalGoals = i['goals_scored']
                totalAssists = i['assists']


                break


        print('player :', int(player))
        print(firstName, ' ',secondName)
        print('Players Team: ', team)
        print('cost :', cost)
        print('Total Points :', totalPoints)

        print('nextOpponent: ',nextOpponent)
        print('next opponent ID: ', opponentID)
        print('opponent playing Home? ', opponentHome)


        # ________________________ DIFFICULTY BUBBLE___________________________
        # 2.

        # The difficulty bubble is the range (1-5) opponents of the same calibre as the selected players next opponents
        # The difficulty bubble thus showcases the average points expected for the next match, based on the historical data
        # of similar opponent strength and the points generated against them.

        teamMatrix = teamMatrix[teamMatrix[:, 0].argsort()]


       # print('Players Team: ', team)

        print(teamMatrix)

        # not sure why, the below is not returning the right values, change 0 to 1 or 2 and test

        oR = teamMatrix[opponentID - 1][2]
        print('Opponent Rank: ', oR)

        # ______________________________ RANK WEIGHTING ___________________________
        # 2. 1

        # TO DO
        # Points should be allocated differently depending on the distance from the first ranking
        # Thus weaker teams should way less towards the difficulty, and stronger teams should way more.

        if 3 <= oR <= 18:
            o1 = int(oR - 2)
            o2 = int(oR - 1)
            o3 = int(oR)
            o4 = int(oR + 1)
            o5 = int(oR + 2)

        elif oR == 2:
            o1 = int(oR + 3)
            o2 = int(oR - 1)
            o3 = int(oR)
            o4 = int(oR + 1)
            o5 = int(oR + 2)

        elif oR == 1:
            o1 = int(oR + 3)
            o2 = int(oR + 4)
            o3 = int(oR)
            o4 = int(oR + 1)
            o5 = int(oR + 2)

        elif oR == 19:
            o1 = int(oR - 2)
            o2 = int(oR - 1)
            o3 = int(oR)
            o4 = int(oR + 1)
            o5 = int(oR - 3)

        elif oR == 20:
            o1 = int(oR - 2)
            o2 = int(oR - 1)
            o3 = int(oR)
            o4 = int(oR - 3)
            o5 = int(oR - 4)

        # Finding how deep the rank is we're looking for

        def column(matrix, i):
            return [row[i] for row in matrix]
        print('column 3 values: ')
        rankList = column(teamMatrix, 2)
        print('rank list: ', rankList)
        item1Depth = rankList.index(o1)
        item2Depth = rankList.index(o2)
        item3Depth = rankList.index(o3)
        item4Depth = rankList.index(o4)
        item5Depth = rankList.index(o5)

        print('item 1 depth: ', item1Depth)

        opID1 = teamMatrix[item1Depth][0]
        opID2 = teamMatrix[item2Depth][0]
        opID3 = teamMatrix[item3Depth][0]
        opID4 = teamMatrix[item4Depth][0]
        opID5 = teamMatrix[item5Depth][0]

        print('opponent 1: team ', opID1)
        print('opponent 2: team ', opID2)
        print('opponent 3: team ', opID3)
        print('opponent 4: team ', opID4)
        print('opponent 5: team ', opID5)

        difficultyBubble = [opID1, opID2, opID3, opID4, opID5]
        scores = 0

        counter = 0
        for opId in difficultyBubble:
            gameweeks = list(range(37, -1, -1))

            for gameweek in gameweeks:
                    try:
                        score = fplPlayerData['history'][gameweek].get('total_points')
                        if fplPlayerData['history'][gameweek].get('opponent_team') == opId and counter < 5:
                            counter = counter + 1
                            print(secondName, 'scored ', score, ' against team ', opId)
                            scores = scores + score

                            if score > 8:
                                print()


                    except IndexError as iE:

                        continue
                    #playerExplosivity real, playerTotalGoals, playerTotalAssists

        print('Projected average score: ', scores/5)
        params = (player, firstName, secondName, playerRole, scores/5, rollingAverage, totalPoints, team, cost, nextOpponent,oR,opID1,opID2,opID3,opID4, opID5,'', totalGoals, totalAssists )
        try:
            c.execute("INSERT INTO players VALUES (?, ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", params)
            conn.commit()
        except sqlite3.IntegrityError as uniqueError:
            print('player already exists')
            # c.execute("UPDATE players SET rollingAverage, totalPoints, cost, nextOpponent, explosivity, totalGoals, totalAssists


    # ________________________________________________________________________________________
    # ________________________________________________________________________________________
    # ________________________________________________________________________________________
        # TO DO
        #   1. List all players in order of
        #     - 10 week rolling average
        #     - 5 week rolling average
        #     - relative power
        #     - number of explosions ( number of scores above
        #       ( if 1 - 3 usually, it has to be higher than 6
        #     - estimate performance against next team
        #     - reliability
        #          - how well have they done against those calibre in the last 5 weeks
        #          - how many goals they have scored recently
        #          - how many assists have they scored recently
        #          - how consistent their scores have been recently
        #
        #   2. return top 6 players based on each player type
        #   3. Explosion logic
        #       - probability to explode
        #       - describe the players explosion tendencies
        #           if against anyone, weaker or stronger teams and the reliability of this classification
        #       - describe their explosion strength
        #           determined by their recent frequency, overall frequency, and explosion size
        #       - weigh different explosion classes against each other. so best in class gets points
        #       - include pricing in the array so i can list by price or find by price range
        #
        #   4. Compare arrays of teams by showcasing the range of their low and high score probabilities
        #   5.
    # ________________________________________________________________________________________
    # ________________________________________________________________________________________
    # ________________________________________________________________________________________

        # ________________________ EXPLOSIVENESS _____________showPlayer  ________

        # Explosiveness is calculated as 1% for each fixture in the difficulty bubble
        # that has a chance of exploding ( gaining more than 10 points )
        # Chance for exploding is calculated by comparing the explosions that have occurred
        # against the calibre of fixtures playing.
        # for instance if Liverpool is the top team, and the player selected has exploded against liverpool
        # the player gains 1% for each team in his difficulty bubble that is weaker than Liverpool


        gameweeks = list(range(37, -1, -1))

        for gameweek in gameweeks:

            try:
                round = fplPlayerData['history'][gameweek].get('round')
                point = fplPlayerData['history'][gameweek].get('total_points')

                if point > 8:

                    victim = fplPlayerData['history'][gameweek].get('opponent_team')
                    explPoint = point

                else:
                    # points = points + point
                    print()

            except IndexError as iE:
                 continue

    conn.commit()
        # _________________________CSV OUTPUT________________________

        # Store data as 'n collection in CSV for viewing in excel or upload to site


#scanPlayers()


def showPlayer():
    x = input("Player code? ")
    c.execute('SELECT * from players WHERE playerCode = '+str(x)+';')
    res = c.fetchone()
    print(res)

#showPlayer()

def showTop():
    go = 1
    y = input("what role? ")
    many = input("Top how many?")
    price = input("Price?")
    if y == 'exit':
        go = 0

    # Don't incorporate heavily skewed data?
    else:
        c.execute('SELECT * from players WHERE playerPrice < '+str(price)+' AND playerRole = '+str(y)+' ORDER BY projectedScore DESC;')
        ps = c.fetchmany(int(many))
        print("PROJECTED SCORE RANKING: ", ps)

        c.execute('SELECT * from players WHERE playerPrice < '+str(price)+' AND playerRole = ' + str(y) + ' ORDER BY rollingAverage DESC;')
        res = c.fetchmany(int(many))
        print("ROLLING AVERAGE RANKING: ", res)

        c.execute('SELECT * from players WHERE playerPrice < '+str(price)+' AND playerRole = '+str(y)+' ORDER BY totalPoints / playerPrice DESC;')
        performance = c.fetchmany(int(many))
        print("PRICE PERFORMANCE RANKING: ", performance)

        c.execute('SELECT * from players WHERE playerPrice < '+str(price)+' AND playerRole = ' + str(y) + ' ORDER BY (totalPoints/37*3) + (rollingAverage*2) + (projectedScore/2)  DESC;')
        mixed = c.fetchmany(int(many))
        print("MIXED RANKING: ", mixed)


        c.execute('SELECT * from players WHERE playerRole = '+str(y)+' ORDER BY totalPoints / playerPrice DESC;')
        performance = c.fetchmany(int(many))
        print("PRICE PERFORMANCE RANKING: ", performance)

        c.execute('SELECT * from players WHERE playerRole = ' + str(y) + ' ORDER BY (totalPoints/37*3) + (rollingAverage*2) + (projectedScore/2)  DESC;')
        mixed = c.fetchmany(int(many))
        print("MIXED RANKING: ", mixed)
        while go == 1:
            showTop()
def pickMethod():
    r = input("What would you like to do: Press 1 to search a player. Press 2 to show top in role.")
    if r == 1:
      showPlayer()
    elif r == 2:
      showTop()
# pickMethod()


