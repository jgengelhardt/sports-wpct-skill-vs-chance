import matplotlib.pyplot as plt
from matplotlib import pylab
import numpy
import numpy.polynomial.polynomial as poly
import pandas as pd

plt.figure(figsize=(8, 6), dpi=80, facecolor='w', edgecolor='k')

# define datasets and labels
leagues = ('NHL','NBA', 'NCAABB', 'NFL','MLB')
colors = ('#8394a1', '#C9082A', '#005eb8', '#013369','#37ae0f')

# aggregate league data
def plot_by_games():
    x = []
    y = []
    col_names = ['year','variance','games']
    for league in leagues:
        df = pd.read_csv(f'./results/{league}_history.csv', names=col_names)
        x += df['games'].tolist()
        y += df['variance'].tolist()

    plt.scatter(x, y, c='k', alpha=0.2)
    coefs = poly.polyfit(x, y, 3)
    ffit = poly.polyval(x, coefs)
    plt.plot(x, ffit)
    
    # design
    plt.title('How Well Does Win% Represent Skill?')
    plt.ylabel('Influence of Skill')
    plt.xlabel('Number of Games Played')
    plt.legend(loc=0)
    plt.show()
    
plot_by_games()