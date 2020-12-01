import csv
import json
import os
import requests
from math import sqrt
from statistics import variance

def get_season_var_NHL(league,startyear):
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
    # estimate the role skill plays in determining final win percentage variance within a given season
    if len(filtered_teams) >= 2:
        season_wpercentages = []
        for team in filtered_teams: # find the variance of win/loss records in a league
            season_wpercentages.append((team['wins']+(team['ties'] or 0)/2) / team['gamesPlayed'])
        # remove estimated variance attributable to chance
        var_diff = variance(season_wpercentages) - (.5*.5/filtered_teams[0]['gamesPlayed'])
        if var_diff > 0:
            return startyear, round(sqrt(var_diff),3), filtered_teams[0]['gamesPlayed']
        else:
            return startyear, 'Error'
    else:
        return startyear, 'Error'

def get_NHL_history():
    league_request = requests.get('https://records.nhl.com/site/api/franchise-season-results')
    league_json = league_request.json()
    NHL_alltime = league_json['data']
    print('Loaded NHL franchise season results from API')
    csvFile = open('./results/NHL_history.csv', 'w', newline='')
    try:
        writer = csv.writer(csvFile)
        for i in range(1917,2022):
            score = get_season_var_NHL(NHL_alltime,i)
            if 'Error' not in score:
                print (f'Loaded NHL season {i}', end="\r", flush=True)
                writer.writerow(score)
    finally:
        csvFile.close()
        print('\nNHL .csv written', flush=True)
        
# new_file_name = os.path.join(csv_folder, "results", f"{file.stem}-edited.csv")

get_NHL_history()
