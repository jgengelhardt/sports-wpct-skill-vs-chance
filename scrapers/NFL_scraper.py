import csv
import os
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError
from statistics import variance
from math import sqrt

def get_season_var_NFL(year):
    try:     # check if the URL exists; else print('No season played')
        year_html = urlopen(f'https://www.pro-football-reference.com/years/{year}/')
    except HTTPError as e:
        return 'Error'
    year_bs = BeautifulSoup(year_html, 'html.parser')
    season_tables = year_bs.findAll('table')
    # pull all win percentages into a list
    win_pct_raw = []
    for table in season_tables:
        win_pct_raw += (table.findAll('td',attrs={'data-stat':'win_loss_perc'}))
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
            wins = int(table.find('td',{'data-stat':'wins'}).get_text())
            losses = int(table.find('td',{'data-stat':'losses'}).get_text())
            ties = 0 if table.find('td',{'data-stat':'ties'}) is None else int(table.find('td',{'data-stat':'ties'}).get_text())
            flips.append(wins+losses+ties)
    flips = sum(flips)/len(flips) # mean number of games played (not ideal, but these tables sometimes include playoff games)
    # get observed variance minus variance attributable to chance
    var_diff = variance(win_pct)-(0.5*0.5/flips)
    if var_diff > 0:
        return round(sqrt(var_diff),3) #return standard deviation, not variance, for readability
    else:
        return 'Error'

def get_NFL_history():
    csvFile = open('./results/NFL_history.csv', 'w', newline='')
    try:
        writer = csv.writer(csvFile)
        for i in range(1920,2020):
            score = [i, get_season_var_NFL(i)]
            if 'Error' not in score:
                print (f'Loaded NFL season {i}', end="\r", flush=True)
                writer.writerow(score)
    finally:
        csvFile.close()
        print('\nNFL .csv written', flush=True)

get_NFL_history()
