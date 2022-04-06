'''A collection of stats generating functions meant to clarify code in the notebooks. Using the '''

import numpy as np
import pandas as pd
from scipy import stats

players = pd.read_csv('baseballdatabank-2022.2/core/People.csv') #basic player info, may want to trim down in future
batting = pd.read_csv('baseballdatabank-2022.2/core/Batting.csv') # regular season batting

players_ids = players['playerID']
# batting = batting.set_index(['playerID', 'yearID'])

def verify_player(playerID):
    '''Verifies that that player is in the database
    by checking their unique playerID against it'''
    if playerID in players_ids.values:
        pass
    else:
        raise Exception(f"IDError: playerID {playerID} not found in database")
        

def AVG(playerID):
    '''Fetches the career batting average of the playerID.
    AVG = H/AB (hits per at-bat)
    PARAMS:
    playerID: the playerID of the relevant player.'''

    verify_player(playerID)

    # print("Found them!")

    # hits = batting[['playerID', 'yearID', 'H']].set_index(['playerID', 'yearID']).groupby(level='playerID').sum()[playerID]
    # atbats = batting.sum(level="AB")[playerID]
    hits = int(batting.loc[batting['playerID']==playerID, ["H"]].sum().values)
    atbats = int(batting.loc[batting['playerID']==playerID, ["AB"]].sum().values)


    return hits/atbats


    print('Found the data!')

    # return hits

