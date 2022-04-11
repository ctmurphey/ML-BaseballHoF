'''A collection of stats generating functions meant to clarify code in the notebooks. Using the '''

import numpy as np
import pandas as pd
from scipy import stats

players = pd.read_csv('baseballdatabank-2022.2/core/People.csv') #basic player info, may want to trim down in future
batting = pd.read_csv('baseballdatabank-2022.2/core/Batting.csv') # regular season batting
pitching = pd.read_csv('baseballdatabank-2022.2/core/Pitching.csv')
fielding = pd.read_csv('baseballdatabank-2022.2/core/Fielding.csv')
FG_weights = pd.read_csv('FanGraphs-Leaderboard.csv')

players_ids = players['playerID']





def verify_player(playerID):
    '''Verifies that that player is in the database
    by checking their unique playerID against it.'''
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
        WHIP = 3*(BB+H)/IPouts (Walks + hits per inning pitched)
        PARAMS: playerID: the playerID of the relevant player.'''

    verify_player(playerID)
    verify_pitcher(playerID)

    # WH = int(pitching.loc[pitching['playerID']==playerID, ["H", "BB"]].sum().sum())
    WH = sum([int(count_pitching_stat(playerID, s)) for s in ["H", "BB"]])
    IPouts = int(count_pitching_stat(playerID, "IPouts"))

    return 3*WH/IPouts





### Intermediate Stats:
### These stats are similar to the basic ones, but incorporate something
### else into the mix that pertains to the league as a whole. These stats
### include ERA+, OPS+, FIP, wOBA

def ERAplus(playerID):
    '''Calculates the career ERA+ of the playerID
        ERA+ = 100*ERA(league)/ERA(player)
        PARAMS: playerID: playerID of relevant player'''

    verify_player(playerID)
    verify_pitcher(playerID)

    ERA_p = ERA(playerID)
    ### This may be slightly off as it doesn't account for players starting/ending mid season
    ###Should be close enough approximation though

    ### Have to do some fun data type manipulation to get the correct years
    date_start = players.loc[players['playerID']==playerID, ['debut']]
    year_start = int(np.array(date_start.values)[0][0][0:4])

    date_end = players.loc[players['playerID']==playerID, ['finalGame']]
    year_end = int(np.array(date_end.values)[0][0][0:4])

    ra_l   = int(pitching.loc[(pitching['yearID']>=year_start) & (pitching['yearID']<=year_end), ['ER']].sum().values)
    outs_l = int(pitching.loc[(pitching['yearID']>=year_start) & (pitching['yearID']<=year_end), ['IPouts']].sum().values)


    ERA_l = 27*ra_l/outs_l

    return 100*ERA_l/ERA_p


def OPSplus(playerID):
    '''Calculates the career OPS+ of the playerID
        OPS+ = 100*OPS(player)/OPS(league)
        OPS = OBP + SLG (on-base plus slugging)
        PARAMS: playerID: playerID of relevant player'''

    verify_player(playerID)
    verify_batter(playerID)

    OBP_b = OBP(playerID)
    SLG_b = SLG(playerID)

    OPS_b = OBP(playerID) + SLG(playerID)
    ### This may be slightly off as it doesn't account for players starting/ending mid season
    ###Should be close enough approximation though, assuming the player played multiple seasons

    ### Have to do some fun data type manipulation to get the correct years
    date_start = players.loc[players['playerID']==playerID, ['debut']]
    year_start = int(np.array(date_start.values)[0][0][0:4])

    date_end = players.loc[players['playerID']==playerID, ['finalGame']]
    year_end = int(np.array(date_end.values)[0][0][0:4])


    H_l   = int(batting.loc[(batting['yearID']>=year_start) & (batting['yearID']<=year_end), ['H']].sum().values)
    BB_l  = int(batting.loc[(batting['yearID']>=year_start) & (batting['yearID']<=year_end), ['BB']].sum().values)
    HBP_l = int(batting.loc[(batting['yearID']>=year_start) & (batting['yearID']<=year_end), ['HBP']].sum().values)
    DBL_l = int(batting.loc[(batting['yearID']>=year_start) & (batting['yearID']<=year_end), ['2B']].sum().values)
    TPL_l = int(batting.loc[(batting['yearID']>=year_start) & (batting['yearID']<=year_end), ['3B']].sum().values)
    HR_l  = int(batting.loc[(batting['yearID']>=year_start) & (batting['yearID']<=year_end), ['HR']].sum().values)
    AB_l  = int(batting.loc[(batting['yearID']>=year_start) & (batting['yearID']<=year_end), ['AB']].sum().values)
    SH_l  = int(batting.loc[(batting['yearID']>=year_start) & (batting['yearID']<=year_end), ['SH']].sum().values)
    SF_l  = int(batting.loc[(batting['yearID']>=year_start) & (batting['yearID']<=year_end), ['SF']].sum().values)
    SGL_l = H_l - DBL_l - TPL_l - HR_l

    RB_l = H_l + BB_l + HBP_l
    PA_l = AB_l + BB_l + HBP_l + SH_l + SF_l

    SLG_l = (SGL_l + 2*DBL_l + 3*TPL_l + 4*HR_l)/AB_l
    OBP_l = RB_l / PA_l   

    OPS_l = OBP_l + SLG_l

    return 100*(OBP_b/OBP_l + SLG_b/SLG_l -1)




def wOBA(playerID):

    verify_player(playerID)
    verify_batter(playerID)



    return



def FIP(playerID):

    verify_player(playerID)
    verify_pitcher(playerID)


    return


### Advanced Stats:
### These stats are significantly more complicated than the intermediate
### ones and may even draw upon and weight them. They have the ironic
### tendancy to be some of the most used yet least understood stats when
### comparing different players. They include fWAR and bWAR (yes they're
### different, same stat created by different stat companies (Fangraphs and BBRef)).