import tkinter as tk
import tkinter.filedialog
import sys
import pandas as pd
import csv
import time
import json
import requests
from datetime import date
import datetime
import pytz
import iso8601
import os
import pymysql
import socket

socket.getaddrinfo('127.0.0.1', 8080)

conn = pymysql.connect(host='127.0.0.1', user='root', password='hyvemobilepassword', db='fpldb')
c = conn.cursor()

root = tk.Tk()
root.withdraw()
# Output file names

dt = str(datetime.datetime.today().strftime(" %B %d %Y "))
storage = "" + dt + " storage "
outputName = 'dispositions_dataset'

#                   Goalbox Functions :
#                   Upload Historical Player Data
#                   Upload

c.execute("""CREATE TABLE IF NOT EXISTS playerdata (
            historical_year VARCHAR(255) NOT NULL,
            player_code INT NOT NULL,
            first_name  VARCHAR(255) NOT NULL,
            second_name  VARCHAR(255) NOT NULL,
            assists INT NOT NULL,
            bonus INT NOT NULL,
            bps INT NOT NULL,
            clean_sheets INT NOT NULL,
            creativity float NOT NULL,
            fixture INT NOT NULL,
            goals_conceded INT NOT NULL,
            goals_scored INT NOT NULL,
            ict_index float NOT NULL,
            influence float NOT NULL,
            kickoff_time VARCHAR(255) NOT NULL,
            minutes INT NOT NULL,
            opponent_team INT NOT NULL,
            own_goals INT NOT NULL,
            penalties_missed INT NOT NULL,
            penalties_saved INT NOT NULL,
            red_cards INT NOT NULL,
            gameweek INT NOT NULL,
            saves INT NOT NULL,
            selected INT NOT NULL,
            team_a_scored INT NOT NULL,
            team_h_scored INT NOT NULL,
            threat float NOT NULL,
            total_points INT NOT NULL,
            transfers_balance INT NOT NULL,
            transfers_in INT NOT NULL,
            transfers_out INT NOT NULL,
            price float NOT NULL,
            was_home VARCHAR(255) NOT NULL,
            yellow_cards INT NOT NULL

            )""")


# ----------- Inserts new csv data into the cloud ( alternatively use google cloud sql import csv ) ------------
# ----------- This method is more reliable but slower depending on region of connection origin.

def playerHistory():
    dir = 'G:/Hunt Systems/FPL-Analytics/Fantasy-Premier-League-master/Fantasy-Premier-League-master/data'
    file_path = tk.filedialog.askopenfilename(initialdir=dir, title="Select file", filetypes=[("ALL Files", "*.*")])
    storage = " storage "
    # -------- PARSE CSV INTO JSON ---------------

    with open(file_path, encoding='utf8', errors='surrogateescape') as input, open(storage + '.csv', 'w',
                                                                                   encoding='utf8') as output:
        non_blank = (line for line in input if line.strip())
        output.writelines(non_blank)
    df = pd.read_csv(storage + ".csv", delimiter=",")

    k = 0
    # ----------- Loops through each line -----------------------------------------
    #
    historical_year = '2018-19'

    with open(storage + '.csv', encoding='utf8') as f:
        for line in f:
            line = line.replace('\n', '')
            k = k + 1
            if k == 1:
                print('headers: ', line)

            else:

                row = line
                sep = ","
                try:
                    foldersep = '_'
                    path = os.path.dirname(file_path)
                    print(historical_year)
                    print('path: ', path)
                    fullname = os.path.basename(path)
                    print('fullname: ', fullname)
                    first_name = fullname.split(foldersep, 1)[0]
                    print('first_name: ', first_name)
                    second_name_and_code = fullname.split(foldersep, 1)[1]
                    second_name = second_name_and_code.split(foldersep, 1)[0]
                    player_code = second_name_and_code.split(foldersep, 1)[1]
                    assists = row.split(sep, 1)[0]
                    data = row.split(sep, 1)[1]

                    c1 = row.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    c2 = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    c3 = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    bonus = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]
                    print('bonus ', bonus)

                    bps = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    clean_sheets = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    c4 = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    c5 = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    creativity = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]
                    print('creativity ', creativity)

                    c6 = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    c7 = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    element = int(data.split(sep, 1)[0])
                    print('player_code, ', element)
                    data = data.split(sep, 1)[1]

                    c8 = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    c9 = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    fixture = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    c10 = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    goals_conceded = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]
                    print('data: ', data)
                    goals_scored = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    ict_index = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    c11 = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    influence = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    c12 = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    kickoff_time = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    c24 = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    c13 = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    c14 = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    minutes = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    c15 = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    c16 = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    opponent_team = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    own_goals = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]
                    print('data: ', data)

                    c23 = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    penalties_missed = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    penalties_saved = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    c17 = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    red_cards = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    gameweek = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    saves = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    selected = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]
                    print('selected: ', selected)

                    c18 = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    c19 = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    c20 = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    team_a_scored = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    team_h_scored = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    threat = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    total_points = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]
                    print('total_points ', total_points)

                    transfers_balance = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    transfers_in = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    transfers_out = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    price = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    was_home = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    c21 = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    yellow_cards = data.split(sep, 1)[0]



                except NameError as nE:
                    print('name error', nE)
                except pymysql.err.InternalError as iE:
                    print('internal error', iE)

                values = (
                    historical_year,
                    player_code,
                    first_name,
                    second_name,
                    int(assists),
                    int(bonus),
                    int(bps),
                    int(clean_sheets),
                    float(creativity),
                    int(fixture),
                    int(goals_conceded),
                    int(goals_scored),
                    float(ict_index),
                    float(influence),
                    kickoff_time,
                    int(minutes),
                    int(opponent_team),
                    int(own_goals),
                    int(penalties_missed),
                    int(penalties_saved),
                    int(red_cards),
                    int(gameweek),
                    int(saves),
                    int(selected),
                    int(team_a_scored),
                    int(team_h_scored),
                    float(threat),
                    int(total_points),
                    int(transfers_balance),
                    int(transfers_in),
                    int(transfers_out),
                    float(price),
                    was_home,
                    int(yellow_cards)

                )
                time.sleep(0.1)

                # 35 items in insertSql

                try:
                    insertSql = """insert into playerdata( 
                    historical_year,
                    player_code,
                    first_name,
                    second_name,
                    assists,
                    bonus,
                    bps,
                    clean_sheets,
                    creativity,
                    fixture,
                    goals_conceded,
                    goals_scored,
                    ict_index,
                    influence,
                    kickoff_time,
                    minutes,
                    opponent_team,
                    own_goals,
                    penalties_missed,
                    penalties_saved,
                    red_cards,
                    gameweek,
                    saves,
                    selected,
                    team_a_scored,
                    team_h_scored,
                    threat,
                    total_points,
                    transfers_balance,
                    transfers_in,
                    transfers_out,
                    price,
                    was_home,
                    yellow_cards
                    )
                    values (
                    %s, 
                    %s, 
                    %s, 
                    %s, 
                    %s, 
                    %s, 
                    %s, 
                    %s, 
                    %s, 
                    %s,
                    %s,
                    %s, 
                    %s, 
                    %s, 
                    %s, 
                    %s, 
                    %s, 
                    %s, 
                    %s, 
                    %s, 
                    %s, 
                    %s,
                    %s,
                    %s,
                    %s, 
                    %s, 
                    %s, 
                    %s, 
                    %s, 
                    %s, 
                    %s, 
                    %s, 
                    %s,
                    %s
                    )"""
                    c.execute(insertSql, values)
                    conn.commit()
                except pymysql.err.InternalError as iE:
                    print('internal error', iE)
                    time.sleep(10)
                    for value in values:
                        print(value, ' ', type(value))


playerHistory()



