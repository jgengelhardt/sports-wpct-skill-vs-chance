import matplotlib.pyplot as plt
from matplotlib import pylab
import numpy
import pandas as pd


# define datasets and labels
leagues = ('NHL','NBA', 'NCAABB', 'NFL','MLB')
colors = ('#8394a1', '#C9082A', '#005eb8', '#013369','#37ae0f')

# plot data grouped by league
col_names = ['year','variance','games']
for league, color in zip(leagues, colors):
    df = pd.read_csv(f'./results/{league}_history.csv', names=col_names)
    x = df['year']
    y = df['variance']
    plt.scatter(x, y, c=color, alpha=0.2, label=league)
    z = numpy.polyfit(x, y, 2)
    p = numpy.poly1d(z)
    pylab.plot(x,p(x),color)

# design
# plt.figure(figsize=(8, 6), dpi=80, facecolor='w', edgecolor='k')
plt.title('How Well Does Win% Represent Skill?')
plt.ylabel('Influence of Skill')
plt.xlabel('Season')
plt.legend(loc=0)
plt.show()