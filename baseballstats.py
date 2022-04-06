'''A collection of stats generating functions meant to clarify code in the notebooks. Using the '''

import numpy as np
import pandas as pd
from scipy import stats

players = pd.read_csv('baseballdatabank-2022.2/core/People.csv') #basic player info, may want to trim down in future
batting = pd.read_csv('baseballdatabank-2022.2/core/Batting.csv') # regular season batting
pitching = pd.read_csv('baseballdatabank-2022.2/core/Pitching.csv')

players_ids = players['playerID']





def verify_player(playerID):
    '''Verifies that that player is in the database
    by checking their unique playerID against it'''
    if playerID in players_ids.values:
        pass
    else:
        raise Exception(f"IDError: playerID {playerID} not found in database")

def verify_batter(playerID):
    '''Verifies that the playerID recorded at lease one AB at some point'''

    if playerID in batting['playerID'].values:
        pass
    else:
        raise Exception(f"IDError: playerID {playerID} not found among batters")

def verify_pitcher(playerID):
    '''Verifies that the playerID pitched at some point'''

    if playerID in pitching['playerID'].values:
        pass
    else:
        raise Exception(f"IDError: playerID {playerID} not found among pitchers")






def count_batting_stat(playerID, stat):
    '''Allows the searching of the total number of a stat a player has,
        (hits, walks, strikeouts, etc.).
        PARAMS: playerID: the playerID of the relevant player
                stat: the stat that we want to be tallied'''
    verify_player(playerID)
    verify_batter(playerID)

    if stat == "K": #adding this because I know I'll make this mistake in the future
        stat = "SO"

    return batting.loc[batting['playerID']==playerID, [stat]].sum().values

def count_pitching_stat(playerID, stat):
    '''Allows the searching of the total number of a stat a player has,
        (strikeouts, wins, saves, etc.).
        PARAMS: playerID: the playerID of the relevant player
                stat: the stat that we want to be tallied'''
    verify_player(playerID)
    verify_pitcher(playerID)

    if stat == "K": #adding this because I know I'll make this mistake in the future
        stat = "SO"

    return pitching.loc[pitching['playerID']==playerID, [stat]].sum().values






###BASIC STATS
###These are the typical run-of-the-mill stats that don't require league
###comparisons, they include AVG,OBP, SLG, ERA, and WHIP


def AVG(playerID):
    '''Calculates the career batting average of the playerID.
    AVG = H/AB (hits per at-bat)
    PARAMS: playerID: the playerID of the relevant player.'''

    verify_player(playerID)
    verify_batter(playerID)

    # hits = int(batting.loc[batting['playerID']==playerID, ["H"]].sum().values)
    hits = int(count_batting_stat(playerID, "H"))
    # atbats = int(batting.loc[batting['playerID']==playerID, ["AB"]].sum().values)
    atbats = int(count_batting_stat(playerID, "AB"))


    return hits/atbats



def OBP(playerID):
    '''Calculates the career on-base percentage of the playerID
        OBP = (H+BB+HBP)/(AB+BB+SH+SF+HBP) (times reached base per plate appearence)
        PARAMS: playerID: the playerID of the relevant player.'''

    verify_player(playerID)
    verify_batter(playerID)


    # reached_base = batting.loc[batting['playerID']==playerID, ["H", "BB", "HBP"]].sum().sum()
    reached_base = sum([int(count_batting_stat(playerID, s)) for s in ["H", "BB", "HBP"]])
    # plate_appearance = batting.loc[batting['playerID']==playerID, ["AB", "BB", "SH", "HBP", "SF"]].sum().sum()
    plate_appearance = sum([int(count_batting_stat(playerID, s)) for s in ["AB", "BB", "SH", "HBP", "SF"]])

    return reached_base/plate_appearance


def SLG(playerID):
    '''Calculates the slugging percentage of the playerID
        SLG = (1B*1+2B*2+3B*3+HR*4)/AB (total bases on hits per at-bat
        PARAMS: playerID: the playerID of the relevant player.'''

    verify_player(playerID)
    verify_batter(playerID)


    hits     = int(count_batting_stat(playerID, "H"))

    doubles  = int(count_batting_stat(playerID, "2B"))
    triples  = int(count_batting_stat(playerID, "3B"))
    homeruns = int(count_batting_stat(playerID, "HR"))

    singles  = hits - doubles - triples - homeruns #since they're not directly logged here
    atbats   = int(count_batting_stat(playerID, "AB"))


    return (singles + 2*doubles + 3*triples + 4*homeruns)/atbats






def ERA(playerID):
    '''Calculates the Earned Run Average of the playerID
        ERA = (ER/IPOuts)*27 (Earned runs per 27 outs pitched)
        PARAMS: playerID: the playerID of the relevant player.'''

    verify_player(playerID)
    verify_pitcher(playerID)


    ER = int(count_pitching_stat(playerID, "ER"))
    IPouts = int(count_pitching_stat(playerID, "IPouts"))

    return 27*ER / IPouts


def WHIP(playerID):
    '''Calculates the WHIP of the playerID
        WHIP = 3*(BB+H)/IPouts (Walks + hits per inning pitched
        PARAMS: playerID: the playerID of the relevant player.'''

    verify_player(playerID)
    verify_pitcher(playerID)

    # WH = int(pitching.loc[pitching['playerID']==playerID, ["H", "BB"]].sum().sum())
    WH = sum([int(count_pitching_stat(playerID, s)) for s in ["H", "BB"]])
    IPouts = int(pitching.loc[pitching['playerID']==playerID, ['IPouts']].sum().values)
    IPouts = int(count_pitching_stat(playerID, "IPouts"))

    return 3*WH/IPouts


