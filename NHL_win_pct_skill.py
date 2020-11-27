# import librarie
import requests
import json
from math import sqrt
from statistics import variance

# get franchise season results from the NHL API
league_request = requests.get('https://records.nhl.com/site/api/franchise-season-results')
league_json = league_request.json()
NHL_alltime = league_json['data']
print('Loaded NHL franchise season results')

def get_season(league,startyear):
    # get franchise records from a given season
    yearid = int(f"{startyear}{startyear+1}")
    season_teams = []
    for element in league:
        if element['seasonId'] == yearid:
            season_teams.append(element)
    print(f'Found {len(season_teams)} entries with seasonId {yearid}')
    # only include regular season games
    filtered_teams = []
    for team in season_teams:
        if team['gamesPlayed'] == season_teams[0]['gamesPlayed']:
            filtered_teams.append(team)
    print(f'Removed {len(season_teams)-len(filtered_teams)} entries, leaving {len(filtered_teams)} from the regular season')
    return filtered_teams

def var_skill(season_teams):
	# estimate the role skill plays in determining final win percentage variance within a given season
    if len(season_teams) >= 2:
        season_wpercentages = []
        for team in season_teams: # find the variance of win/loss records in a league
            season_wpercentages.append((team['wins']+(team['ties'] or 0)/2) / team['gamesPlayed'])
        # remove estimated variance attributable to chance
        var_diff = variance(season_wpercentages) - (.5*.5/season_teams[0]['gamesPlayed'])
        if var_diff > 0:
            return round(sqrt(var_diff),3)
        else:
            return 'Error'
    else:
        print('Not enough season participation')

def skill_history(start, stop):
    output = {'year': 'skill stdev'}
    for i in range(start,stop+1):
        output[i] = var_skill(get_season(NHL_alltime,i))
    return output

# ask the user what they want to see
first_year = input('What year do you want to start with?'
last_year = input('What recent year do you want to end on?')
print skill_history(first_year, last_year)