from bs4 import BeautifulSoup, Comment
from urllib.request import urlopen
from urllib.error import HTTPError
from statistics import variance
from math import sqrt

def get_season_var_MLB(year):
    try:     # check if the URL exists; else print('No season played')
        year_html = urlopen(f'https://www.baseball-reference.com/leagues/MLB/{year}.shtml')
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
        return round(sqrt(var_diff),3) #return standard deviation, not variance, for readability
    else:
        return 'Error'

def MLB_skill_history(start,stop):
    history = []
    for season in range(start,stop+1):
        score = [season, get_season_var_MLB(season)]
        if 'Error'  not in score:
            history += [score]
    return history

MLB_history = MLB_skill_history(1901,2020)
print(MLB_history)