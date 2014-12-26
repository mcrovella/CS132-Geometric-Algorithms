import numpy as np
import matplotlib as mp
import matplotlib.pyplot as plt

def plotSetup():
    fig = plt.figure()
    return fig.add_subplot(1, 1, 1)

def plotLinEqn (a1, a2, b, xmin = -6.0, xmax = 6.0, ymin = -2.0, ymax = 4.0):
    # a1 x + a2 y = b
    x1 = xmin
    y1 = (b - (x1 * a1))/float(a2)
    x2 = xmax
    y2 = (b - (x2 * a1))/float(a2)
    plt.plot([x1, x2],[y1, y2])
    plt.xlim([xmin, xmax])
    plt.ylim([ymin, ymax])

def centerAxes (ax):
    ax.spines['left'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_position('zero')
    ax.spines['top'].set_color('none')
    ax.spines['left'].set_smart_bounds(True)
    ax.spines['bottom'].set_smart_bounds(True)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
