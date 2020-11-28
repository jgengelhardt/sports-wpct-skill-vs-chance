# import librarie
import requests
import json
from math import sqrt
from statistics import variance

# get franchise season results from the NHL API
league_request = requests.get('https://records.nhl.com/site/api/franchise-season-results')
league_json = league_request.json()
NHL_alltime = league_json['data']
print('Loaded NHL franchise season results from API')

def get_season(league,startyear):
    # get franchise records from a given season
    yearid = int(f"{startyear}{startyear+1}")
    season_teams = []
    for element in league:
        if element['seasonId'] == yearid:
            season_teams.append(element)
    # only include regular season games
    filtered_teams = []
    for team in season_teams:
        if team['gamesPlayed'] == season_teams[0]['gamesPlayed']:
            filtered_teams.append(team)
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
        return 'Error'

def skill_history(start, stop):
    output = []
    for i in range(start,stop+1):
        score = [i,var_skill(get_season(NHL_alltime,i))]
        if 'Error'  not in score:
            output += [score]
    return output

NHL_history = skill_history(1917,2021)
print(NHL_history)