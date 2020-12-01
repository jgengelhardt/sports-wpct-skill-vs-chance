import csv
import os
from bs4 import BeautifulSoup, Comment
from urllib.request import urlopen
from urllib.error import HTTPError
from statistics import variance
from math import sqrt

def get_season_var_WNBA(year):
    try:     # check if the URL exists; else print('No season played')
        year_html = urlopen(f'https://www.basketball-reference.com/wnba/years/{year}.html')
    except HTTPError as e:
        return 'Error'
    year_bs = BeautifulSoup(year_html, 'html.parser')
    year_comments = year_bs.find_all(text=lambda text:isinstance(text, Comment))
    season_tables = []
    for comment in year_comments:
        readable = BeautifulSoup(comment, 'html.parser')
        season_tables += readable.findAll('table')
    # pull all win percentages into a list
    win_pct_raw = []
    for table in season_tables:
        win_pct_raw += (table.findAll('td',{'data-stat':'win_loss_pct'} ))
    if len(win_pct_raw) == 0:
        return 'Error'
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
                flips = sum(flips)/len(flips) # mean number of games played (not ideal, but these tables might include playoff games)
            except:
                pass
    # get observed variance minus variance attributable to chance
    var_diff = variance(win_pct)-(0.5*0.5/flips)
    if var_diff > 0:
        return round(sqrt(var_diff),3) #return standard deviation, not variance, for readability
    else:
        return 'Error'

def get_WNBA_history():
    csvFile = open('./results/WNBA_history.csv', 'w', newline='')
    try:
        writer = csv.writer(csvFile)
        for i in range(1997,2021):
            score = [i, get_season_var_WNBA(i)]
            if 'Error' not in score:
                print (f'Loaded WNBA season {i}', end="\r", flush=True)
                writer.writerow(score)
    finally:
        csvFile.close()
        print('\nWNBA .csv written', flush=True)

get_WNBA_history()
