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
from google.cloud import bigquery

# BigQuery Configuration."""
from os import environ
# Google BigQuery config
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'G:\Hunt Systems\FPL-Analytics\mykey.json'
gcp_credentials = os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'G:\Hunt Systems\FPL-Analytics\mykey.json'
print(gcp_credentials)

client = bigquery.Client(project='fpl-production')
dataset_id = 'fpl-production:fantasy_data'
table = client.get_table('fantasy_data.performances')

root = tk.Tk()
root.withdraw()
# Output file names

dt = str(datetime.datetime.today().strftime(" %B %d %Y "))
storage = "" + dt + " storage "
outputName = 'dispositions_dataset'

#                   Goalbox Functions :
#                   Upload Historical Player Data
#                   Upload



# ----------- Inserts new csv data into the cloud ( alternatively use google cloud sql import csv ) ------------
# ----------- This method is more reliable but slower depending on region of connection origin.

def playerHistory():
    dir = '/FPL-Analytics/Fantasy-Premier-League-master/Fantasy-Premier-League-master/data'
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
                    assists = row.split(sep, 1)[0]
                    data = row.split(sep, 1)[1]
                    bonus = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    bps = data.split(sep, 1)[0]

                    print('bps: ', bps)
                    data = data.split(sep, 1)[1]

                    clean_sheets = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    creativity = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]
                    element = int(data.split(sep, 1)[0])
                    print('player_code, ', element)
                    data = data.split(sep, 1)[1]

                    fixture = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    goals_conceded = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]
                    print('data: ', data)
                    goals_scored = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    ict_index = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    influence = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    kickoff_time = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    minutes = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    opponent_team = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    own_goals = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]
                    print('data: ', data)
                    penalties_missed = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    penalties_saved = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    red_cards = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    gameweek = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    saves = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    selected = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]
                    print('data: ', data)

                    team_a_scored = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    team_h_scored = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    threat = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

                    total_points = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]

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

                    yellow_cards = data.split(sep, 1)[0]



                except NameError as nE:
                    print('name error', nE)

                values = (
                    historical_year,
                    element,
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
                    rows_to_insert = [(
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
                             )]
                    errors = client.insert_rows(
                        table, rows_to_insert, row_ids=[None] * len(rows_to_insert)
                    )
                    if not errors:
                                print('New Rows have been added')
                except NameError as error:
                    print(error)

playerHistory()



