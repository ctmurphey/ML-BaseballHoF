'''A collection of stats generating functions meant to clarify code in the notebooks. Using the '''

import numpy as np
import pandas as pd
from scipy import stats

players = pd.read_csv('baseballdatabank-2022.2/core/People.csv') #basic player info, may want to trim down in future
batting = pd.read_csv('baseballdatabank-2022.2/core/Batting.csv') # regular season batting
pitching = pd.read_csv('baseballdatabank-2022.2/core/Pitching.csv')

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
    '''Calculates the career batting average of the playerID.
    AVG = H/AB (hits per at-bat)
    PARAMS: playerID: the playerID of the relevant player.'''

    verify_player(playerID)

    hits = int(batting.loc[batting['playerID']==playerID, ["H"]].sum().values)
    atbats = int(batting.loc[batting['playerID']==playerID, ["AB"]].sum().values)


    return hits/atbats



def OBP(playerID):
    '''Calculates the career on-base percentage of the playerID
        OBP = (H+BB+HBP)/(AB+BB+SH+SF+HBP) (times reached base per plate appearence)
        PARAMS: playerID: the playerID of the relevant player.'''

    verify_player(playerID)

    reached_base = batting.loc[batting['playerID']==playerID, ["H", "BB", "HBP"]].sum().sum()
    plate_appearance = batting.loc[batting['playerID']==playerID, ["AB", "BB", "SH", "HBP", "SF"]].sum().sum()

    return reached_base/plate_appearance


def SLG(playerID):
    '''Calculates the slugging percentage of the playerID
        SLG = (1B*1+2B*2+3B*3+HR*4)/AB (total bases on hits per at-bat
        PARAMS: playerID: the playerID of the relevant player.'''

    verify_player(playerID)

    hits     = int(batting.loc[batting['playerID']==playerID, ["H"]].sum().values)

    doubles  = int(batting.loc[batting['playerID']==playerID, ["2B"]].sum().values)
    triples  = int(batting.loc[batting['playerID']==playerID, ["3B"]].sum().values)
    homeruns = int(batting.loc[batting['playerID']==playerID, ["HR"]].sum().values)

    singles  = hits - doubles - triples - homeruns #since they're not directly logged here
    atbats   = int(batting.loc[batting['playerID']==playerID, ["AB"]].sum().values)


    return (singles + 2*doubles + 3*triples + 4*homeruns)/atbats



def ERA(playerID):
    '''Calculates the Earned Run Average of the playerID
        ERA = (ER/IPOuts)*27 (Earned runs per 27 outs pitched)
        PARAMS: playerID: the playerID of the relevant player.'''

    verify_player(playerID)

    ER = int(pitching.loc[pitching['playerID']==playerID, ['ER']].sum().values)
    IPouts = int(pitching.loc[pitching['playerID']==playerID, ['IPouts']].sum().values)

    return 27*ER / IPouts


def WHIP(playerID):
    '''Calculates the WHIP of the playerID
        WHIP = 3*(BB+H)/IPouts (Walks + hits per inning pitched
        PARAMS: playerID: the playerID of the relevant player.'''

    WH = int(pitching.loc[pitching['playerID']==playerID, ["H", "BB"]].sum().sum())
    IPouts = int(pitching.loc[pitching['playerID']==playerID, ['IPouts']].sum().values)

    return 3*WH/IPouts


def count_pitching_stat(playerID, stat):
    '''Allows the searching of the total number of a stat a player has,
        (strikeouts, wins, saves, etc.).
        PARAMS: playerID: the playerID of the relevant player
                stat: the stat that we want to be tallied'''

    if stat == "K": #adding this because I know I'll make this mistake in the future
        stat = "SO"

    return pitching.loc[pitching['playerID']==playerID, [stat]].sum().values

