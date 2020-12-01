from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError
from statistics import variance
from math import sqrt

def get_season_var_NBA(year):
    try:     # check if the URL exists; else print('No season played')
        year_html = urlopen(f'https://www.basketball-reference.com/leagues/NBA_{year}.html')
    except HTTPError as e:
        return 'Error'
    year_bs = BeautifulSoup(year_html, 'html.parser')
    season_tables = year_bs.findAll('table')
    # pull all win percentages into a list
    win_pct_raw = []
    for table in season_tables:
        win_pct_raw += (table.findAll('td',attrs={'data-stat':'win_loss_pct'}))
    win_pct = []
    for score in win_pct_raw:
        try:
            win_pct.append(float(score.get_text()))
        except:
            return 'Error'
    # find variance attributable to chance
    flips = []
    for table in season_tables:
        for row in table.findAll('tr'):
            flips.append(int(table.find('td',{'data-stat':'wins'}).get_text())+int(table.find('td',{'data-stat':'losses'}).get_text()))
    flips = sum(flips)/len(flips) # mean number of games played (not ideal, but these tables include playoff games)
    # get observed variance minus variance attributable to chance
    var_diff = variance(win_pct)-(0.5*0.5/flips)
    if var_diff > 0:
        return round(sqrt(var_diff),3) #return standard deviation, not variance, for readability
    else:
        return 'Error'

def NBA_skill_history(start,stop):
    history = []
    for season in range(start,stop+1):
        score = [season, get_season_var_NBA(season)]
        if 'Error'  not in score:
            history += [score]
    return history

NBA_history = NBA_skill_history(1940,2022)
