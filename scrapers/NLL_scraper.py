import csv
import os
import re
from bs4 import BeautifulSoup, Comment
from math import sqrt
from statistics import variance
from urllib.error import HTTPError
from urllib.request import Request, urlopen

def get_yearid_NLL():
    # get webpage containing list of ids
    url = f'https://www.nll.com/standings/'
    req = Request(url , headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    bs = BeautifulSoup(html, 'html.parser')
    # get ids
    options = bs.find('div',{'class':'filters standings'}).find_all('option') # get stats dropdown options
    seasons = list(filter(lambda x: 'Season' in x.get_text(), options)) # only keep regular season IDs
    season_ids = {}
    for season in seasons: # assign id to key and year to value
        season_ids[int(season.attrs['value'])] = int(re.findall("\d+", season.get_text())[0])
    return season_ids

def get_season_var_NLL(seasonid):
    try:     # check if the URL exists
        url = f'http://nll_stats.stats.pointstreak.com/standings.html?leagueid=230&seasonid={seasonid}&sortby=wpct'
        req = Request(url , headers={'User-Agent': 'Mozilla/5.0'})
        year_html = urlopen(req).read()
    except HTTPError as e:
        return 'Error'
    global year_bs
    year_bs = BeautifulSoup(year_html, 'html.parser')
    
    season_tables = year_bs.findAll('table',{'class':"tablelines"})
    if len(season_tables) == 0:
        return 'Error'
    # pull all win percentages into a list
    win_pct_raw = []
    for table in season_tables:
        win_pct_raw += (table.findAll('td',attrs={'class':'sortcell'}))
    win_pct = []
    for score in win_pct_raw:
        try:
            win_pct.append(float(score.get_text()))
        except:
            return 'Error'

    # find variance attributable to chance
    flips = []
    for table in season_tables:
        for row in table.find_all('tr')[2:]:
            wins = int(row.find_all('td')[1].get_text())
            losses = int(row.find_all('td')[2].get_text())
            flips.append(wins + losses)
    if len(flips) <= 0:
        return 'Error'
    flips = sum(flips)/len(flips) # mean number of games played (not ideal, but these tables sometimes include playoff games)
    # get observed variance minus variance attributable to chance
    var_diff = variance(win_pct)-(0.5*0.5/flips)
    if var_diff > 0:
        return round(sqrt(var_diff),3) #return standard deviation, not variance, for readability
    else:
        return 'Error'

def get_NLL_history():
    csvFile = open('./results/NLL_history.csv', 'w', newline='')
    season_ids = get_yearid_NLL()
    try:
        writer = csv.writer(csvFile)
        for id in season_ids:
            score = [season_ids[id], get_season_var_NLL(id)]
            if 'Error' not in score:
                print (f'Loaded NLL season {season_ids[id]}', end="\r", flush=True)
                writer.writerow(score)
    finally:
        csvFile.close()
        print('\nNLL .csv written', flush=True)

get_NLL_history()
