import tkinter as tk
import tkinter.filedialog
import pandas as pd
import datetime
import os
# BigQuery Configuration."""

from google.cloud import bigquery

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'G:\Hunt Systems\FPL-Analytics\mykey.json'
gcp_credentials = os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'G:\Hunt Systems\FPL-Analytics\mykey.json'
print(gcp_credentials)

client = bigquery.Client(project='fpl-production')
dataset_id = 'fpl-production:fantasy_data'
table = client.get_table('fantasy_data.players')


root = tk.Tk()
root.withdraw()
# Output file names

dt = str(datetime.datetime.today().strftime(" %B %d %Y "))
storage = "" + dt + " storage "
outputName = 'dispositions_dataset'

def playerHistory():
    dir = '/FPL-Analytics/Fantasy-Premier-League-master/Fantasy-Premier-League-master/data'
    file_path = tk.filedialog.askopenfilename(initialdir=dir, title="Select file", filetypes=[("ALL Files", "*.*")])
    storage = " storage "
    # -------- PARSE CSV INTO JSON ---------------

    with open(file_path, encoding='latin-1',errors='surrogateescape') as input, \
            open(storage + '.csv', 'w', encoding='latin-1', errors='surrogateescape') as output:
        non_blank = (line for line in input if line.strip())
        output.writelines(non_blank)
    df = pd.read_csv(storage + ".csv", delimiter=",", encoding='latin-1')

    k = 0
    # ----------- Loops through each line -----------------------------------------
    #

    with open(storage + '.csv', encoding='utf-8-sig') as f:
        rows_to_insert = []

        for line in f:
            line = line.replace('\n', '')
            k = k + 1
            row = line
            sep = ","

            try:
                    playerID = row.split(sep, 1)[0]
                    data = row.split(sep, 1)[1]
                    print(playerID)

                    first_name = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]
                    print(first_name)
                    last_name = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]
                    print(last_name)
                    player_role = data.split(sep, 1)[0]
                    data = data.split(sep, 1)[1]
                    print(player_role)
                    player_teamID = data.split(sep, 1)[0]
                    print(player_teamID)

                    timestamp = '2020-09-11T09:00:00Z'
            except NameError as nE:
                print('name error', nE)

            schema = [

                    bigquery.SchemaField('playerID', 'INTEGER', mode='REQUIRED'),
                    bigquery.SchemaField('timestamp', 'TIMESTAMP', mode='REQUIRED'),
                    bigquery.SchemaField('first_name', 'STRING', mode='REQUIRED'),
                    bigquery.SchemaField('last_name', 'STRING', mode='REQUIRED'),
                    bigquery.SchemaField('player_role', 'INTEGER', mode='REQUIRED'),
                    bigquery.SchemaField('player_teamID', 'INTEGER', mode='REQUIRED')
                ]

            job_config = bigquery.LoadJobConfig()
            job_config.schema = schema

            try:
                        row = dict({
                            "playerID": playerID,
                            "timestamp": timestamp,
                            "first_name": first_name,
                            "last_name": last_name,
                            "player_role": player_role,
                            "player_teamID":  player_teamID
                        })

                        dict_copt = row.copy()
                        rows_to_insert.append(dict_copt)

                        print(row)

            except IndexError as error:
                    print(error)
        errors = client.insert_rows(
            table, rows_to_insert, selected_fields=schema
        )
        for error in errors:
            print(error)
        if not errors:
            print('New Rows have been added')


playerHistory()

