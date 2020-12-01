import numpy
import matplotlib.pyplot as plt
from matplotlib import pylab

# define datasets and labels
leagues = ('NHL','NBA', 'WNBA', 'NFL','MLB')
colors = ('#8394a1', '#C9082A','#FA8320', '#013369','#37ae0f')

# plot data grouped by league
for league, color in zip(leagues, colors):
    x=[]
    y=[]
    with open(f'./scrapers/results/{league}_history.csv', 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        for row in plots:
            x.append(int(row[0]))
            y.append(float(row[1]))
    plt.scatter(x, y, c=color, alpha=0.3, label=league)
    z = numpy.polyfit(x, y, 1)
    p = numpy.poly1d(z)
    pylab.plot(x,p(x),color)

# design
plt.title('How Well Does Win% Represent Skill?')
plt.ylabel('Influence of Skill')
plt.xlabel('Season')
plt.legend(loc=0)
plt.show()