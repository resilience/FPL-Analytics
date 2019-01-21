import requests
import urllib, json
import csv
import os

import sys
from urllib.request import FancyURLopener


mz = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
apple = ' AppleWebKit/537.36 (KHTML, like Gecko) '
chrome = 'Chrome/66.0.3359.181 Safari/537.36'


class MyOpener(FancyURLopener):version = mz+apple+chrome
myopener = MyOpener()



# player ID's selected for evaluation
playerIDArray =['','','','','']


for player in playerIDArray:

    apiPlayerURL = 'https://fantasy.premierleague.com/drf/element-summary/'
    param = player

    try:
        this = apiPlayerURL + param

    except ValueError as vE:
        print('Value Error on ' + param)
        continue

    try:
         apiPlayerSearch = myopener.open(this.strip()).read()

    except ValueError as vE:
        print('Value Error on ' + param)
        continue



    # The difficulty bubble is the range (1-5) opponents of the same calibre as the selected players next opponents
    # The difficulty bubble thus showcases the average points expected for the next match, based on the historical data
    # of similar opponent strength and the points generated against them.

    opponenentRank =
    oR = opponentRank
    difficultyBubbleFixtures = [ oR-2, oR-1 ,oR ,oR +1, oR +2]
    difficultyBubbleGWs =


    nextFixtureAverage = difficultyBubblePoints / difficultyBubbleFixtures
    tenWeekRollingAverage = lastTenGameData / 10

    # Explosivity is calculated as 1% for each fixture in the difficulty bubble
    # that has a chance of exploding ( gaining more than 10 points )
    # Chance for exploding is calculated by comparing the explosions that have occured
    # against the calibre of fixtures playing.
    # for instance if Liverpool is the top team, and the player selected has exploded against liverpool
    # the player gains 1% for each team in his difficulty bubble that is weaker than Liverpool

    explosivity


