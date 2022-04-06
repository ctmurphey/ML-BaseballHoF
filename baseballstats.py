'''A collection of stats generating functions meant to clarify code in the notebooks. Using the '''

import numpy as np
import pandas as pd
from scipy import stats

players = pd.read_csv('baseballdatabank-2022.2/core/People.csv') #basic player info, may want to trim down in future
batting = pd.read_csv('baseballdatabank-2022.2/core/Batting.csv') # regular season batting
# players['playerID'] = str(players['playerID'])
players_ids = players['playerID'].astype(pd.StringDtype())


def verify_player(playerID):
    '''Verifies that that player is in the database
    by checking their unique playerID against it'''
    if playerID in players_ids.values:
        pass
    else:
        raise Exception("IDError: playerID not found in database")
        

def AVG(playerID):
    '''Fetches the batting average using the data in the csv files provided.
    PARAMS:
    playerID: the playerID of the relevant player.'''

    verify_player(playerID)

    print("Found them!")

    

