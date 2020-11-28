import numpy
import matplotlib.pyplot as plt
from matplotlib import pylab

# define datasets and labels
leagues = (NHL_history, NBA_history)
colors = ('k', '#FA8320')
groups = ('NHL','NBA')

# plot data grouped by league
for league, color, group in zip(leagues, colors, groups):
    x,y = zip(*league)
    plt.scatter(x, y, c=color, label=group)
    z = numpy.polyfit(x, y, 1)
    p = numpy.poly1d(z)
    pylab.plot(x,p(x),color)

# design layout
plt.title('How Well Does Win% Represent Skill?')
plt.ylabel('Influence of Skill')
plt.xlabel('Season')
plt.legend(loc=0)
plt.show()