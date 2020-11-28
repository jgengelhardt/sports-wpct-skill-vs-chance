import numpy
import matplotlib.pyplot as plt
from matplotlib import pylab

# define datasets and labels
leagues = (NHL_history, NBA_history, WNBA_history, NFL_history, MLB_history)
colors = ('#000000', '#C9082A','#FA8320', '#013369','y')
groups = ('NHL','NBA', 'WNBA', 'NFL','MLB')

# plot data grouped by league
for league, color, group in zip(leagues, colors, groups):
    x,y = zip(*league)
    plt.scatter(x, y, c=color, alpha=0.2, label=group)
    z = numpy.polyfit(x, y, 1)
    p = numpy.poly1d(z)
    pylab.plot(x,p(x),color)

# design
plt.title('How Well Does Win% Represent Skill?')
plt.ylabel('Influence of Skill')
plt.xlabel('Season')
plt.legend(loc=0)
plt.show()