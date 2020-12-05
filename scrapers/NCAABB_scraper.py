import csv
import os
from bs4 import BeautifulSoup, Comment
from urllib.request import urlopen
from urllib.error import HTTPError
from statistics import variance
from math import sqrt

def get_season_var_NCAABB(year):
    try:     # check if the URL exists; else print('No season played')
        year_html = urlopen(f'https://www.sports-reference.com/cbb/seasons/{year}.html')
    except HTTPError as e:
        return 'Error'
    year_bs = BeautifulSoup(year_html, 'html.parser')
    season_tables = year_bs.findAll('table')
    if len(season_tables) == 0:
        return 'Error'
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
            try:
                flips.append(int(table.find('td',{'data-stat':'wins'}).get_text())+int(table.find('td',{'data-stat':'losses'}).get_text()))
            except:
                pass
    if len(flips) <= 0:
        return 'Error'
    flips = sum(flips)/len(flips) # mean number of games played (not ideal, but these tables sometimes include playoff games)
    # get observed variance minus variance attributable to chance
    var_diff = variance(win_pct)-(0.5*0.5/flips)
    if var_diff > 0:
        return round(sqrt(var_diff),3) #return standard deviation, not variance, for readability
    else:
        return 'Error'

def get_NCAABB_history():
    csvFile = open('./results/NCAABB_history.csv', 'w', newline='')
    try:
        writer = csv.writer(csvFile)
        for i in range(1971,2020):
            score = [i, get_season_var_NCAABB(i)]
            if 'Error' not in score:
                print (f'Loaded NCAABB season {i}', end="\r", flush=True)
                writer.writerow(score)
    finally:
        csvFile.close()
        print('\nNCAABB .csv written', flush=True)

get_NCAABB_history()