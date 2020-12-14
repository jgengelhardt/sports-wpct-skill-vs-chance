import csv
import os
from bs4 import BeautifulSoup, Comment
from math import sqrt
from statistics import variance
from urllib.error import HTTPError
from urllib.request import Request, urlopen

def get_season_var_MLB(year):
    try:     # check if the URL exists
        url = f'https://www.baseball-reference.com/leagues/MLB/{year}.shtml'
        req = Request(url)
        year_html = urlopen(req).read()
    except HTTPError as e:
        return 'Error'
    year_bs = BeautifulSoup(year_html, 'html.parser')
    year_comments = year_bs.find_all(text=lambda text:isinstance(text, Comment))
    season_tables = []
    for comment in year_comments:
        readable = BeautifulSoup(comment, 'html.parser')
        season_tables += readable.findAll('table')
    if season_tables == 0:
        return 'Error'
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
            try:
                flips.append(int(table.find('td',{'data-stat':'G'}).get_text()))
            except:
                pass
    flips = sum(flips)/len(flips) # mean number of games played (not ideal, but these tables sometimes include playoff games)
    # get observed variance minus variance attributable to chance
    var_diff = variance(win_pct)-(0.5*0.5/flips)
    if var_diff > 0:
        return year, round(sqrt(var_diff),3), flips #return standard deviation, not variance, for readability
    else:
        return 'Error'

def get_MLB_history():
    csvFile = open('./results/MLB_history.csv', 'w', newline='')
    try:
        writer = csv.writer(csvFile)
        for i in range(1900,2020):
            score = get_season_var_MLB(i)
            if 'Error' not in score:
                print (f'Loaded MLB season {i}', end="\r", flush=True)
                writer.writerow(score)
    finally:
        csvFile.close()
        print('\nMLB .csv written', flush=True)

get_MLB_history()
