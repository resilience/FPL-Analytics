import requests
import urllib, json
import csv
import os

import sys
from urllib.request import FancyURLopener

# player ID's selected for evaluation


playerIDArray =['','','','','']


for player in playerIDArray:

    # The difficulty bubble is the range (1-5) opponents of the same calibre as the selected players next opponents
    # The difficulty bubble thus showcases the average points expected for the next match, based on the historical data
    # of similar opponent strength and the points generated against them.

    opponenentRank =
    oP = opponentRank
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