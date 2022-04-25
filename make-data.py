import pandas as pd
import baseballstats as bbs
from datetime import date

'''Makes the csv files of the pandas dataframes for pitchers and hitters.'''

#Step 1: sort out the people still eligible
    #Rules for eligibility: (source: https://baseballhall.org/hall-of-famers/rules/bbwaa-rules-for-election)
    #   -Retired for at least 5 years
    #   -Retired for no more than 15
    #   -Played for at least 10 seasons

    #Therefore, to find all of the players who were at one point eligible
    #but not anymore, we just need those who played for at least 10 seasons
    #but retired more than 15 years ago.

current_year = int(str(date.today())[:4])

# print(len(bbs.players_ids))

# just take the first few until we're ready to run on the whole set
all_players = pd.DataFrame({'playerID': list(bbs.players_ids)})

all_players['Seasons'] = [bbs.count_seasons(pid) for pid in all_players['playerID']]

eligible = pd.DataFrame(all_players.loc[all_players['Seasons'] >= 10])
eligible['Last_season'] = [bbs.last_season(pid) for pid in eligible['playerID']]

past_eligible = eligible.loc[current_year - eligible['Last_season'] >= 15].reset_index()
del past_eligible['index'] #leftover from cutting out players

#finish up the mutual stats for both pitchers and hitters
past_eligible['HoF']      = [bbs.HoF_inductee(pid) for pid in past_eligible['playerID']]
past_eligible['Awards']   = [bbs.award_count(pid) for pid in past_eligible['playerID']]
past_eligible['WS_titles']= [bbs.WS_titles(pid) for pid in past_eligible['playerID']]
past_eligible['allstars'] = [bbs.allstar_count(pid) for pid in past_eligible['playerID']]
past_eligible['appearances'] = [int(sum(bbs.count_appearances(pid).values)) for pid in past_eligible['playerID']]

# Seperating hitters and pitchers with a boolean mask of whether or not half their appearances were as a pitcher
is_batter = [(bbs.count_appearances(pid).values[0] < past_eligible.loc[past_eligible['playerID']==pid, ['appearances']].values / 2)
 for pid in past_eligible['playerID']]

is_batter = [i[0][0] for i in is_batter]


battingdata = pd.DataFrame(past_eligible.loc[is_batter])
pitchingdata = pd.DataFrame(past_eligible.loc[[~i for i in is_batter]])


# Now that the pitchers and batters are seperated, time to add the other stats to each

# lets start with pitching

counting_stats_p = ['SO', 'W', 'L', 'G', 'SV', 'H', 'ER', 'HR', 'BB']
for stat in counting_stats_p:
    pitchingdata[stat] = [int(bbs.count_pitching_stat(pid, stat)) for pid in pitchingdata['playerID']]

pitchingdata['ERA']  = [bbs.ERA(pid) for pid in pitchingdata['playerID']]
pitchingdata['WHIP'] = [bbs.WHIP(pid) for pid in pitchingdata['playerID']]
pitchingdata['ERA+'] = [bbs.ERAplus(pid) for pid in pitchingdata['playerID']]
pitchingdata['FIP']  = [bbs.FIP(pid) for pid in pitchingdata['playerID']]


# Now lets move on to batting
counting_stats_b = ['G', 'R', 'H', 'HR', 'RBI', 'SB', 'BB']
for stat in counting_stats_b:
    battingdata[stat] = [int(bbs.count_batting_stat(pid, stat)) for pid in battingdata['playerID']]

battingdata['AVG']  = [bbs.AVG(pid) for pid in battingdata['playerID']]
battingdata['OBP']  = [bbs.OBP(pid) for pid in battingdata['playerID']]
battingdata['SLG']  = [bbs.AVG(pid) for pid in battingdata['playerID']]
battingdata['OPS+'] = [bbs.OPSplus(pid) for pid in battingdata['playerID']]
battingdata['wOBA'] = [bbs.wOBA(pid) for pid in battingdata['playerID']]

# print(battingdata)
# print(pitchingdata)
battingdata = battingdata.reset_index()
pitchingdata = pitchingdata.reset_index()

del battingdata['index']
del pitchingdata['index']
#now all that's left is to save to csv files

battingdata.to_csv('battingdata.csv')
pitchingdata.to_csv('pitchingdata.csv')