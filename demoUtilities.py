import numpy as np
import matplotlib as mp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def plotSetup(xmin = -3.0, xmax = 3.0, ymin = -3.0, ymax = 3.0, size=(6,6)):
    """
    refactored version of ut.plotSetup to hide as much as possible when showing code
    basics of 2D plot setup
    defaults: xmin = -3.0, xmax = 3.0, ymin = -3.0, ymax = 3.0, size=(6,6)
    size is by default 6 inches by 6 inches
    """
    fig = plt.figure(figsize=size)
    ax = fig.add_subplot(1, 1, 1, aspect='equal')
    plt.xlim([xmin, xmax])
    plt.ylim([ymin, ymax])
    ax.axes.set_xlim([xmin, xmax])
    centerAxes(ax)
    return ax

def AxVS(A,x):
    """
    Takes a matrix A and a vector x and returns their product
    """
    m,n = np.shape(A)
    b = np.zeros(m)
    for i in range(n):
        b = b + x[i] * A[:,i]
    return b

def mnote():
    res = np.array(
        [[193,47],
        [140,204],
        [123,193],
        [99,189],
        [74,196],
        [58,213],
        [49,237],
        [52,261],
        [65,279],
        [86,292],
        [113,295],
        [135,282],
        [152,258],
        [201,95],
        [212,127],
        [218,150],
        [213,168],
        [201,185],
        [192,200],
        [203,214],
        [219,205],
        [233,191],
        [242,170],
        [244,149],
        [242,131],
        [233,111]])
    return res.T/150.0


def centerAxes (ax):
    ax.spines['left'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_position('zero')
    ax.spines['top'].set_color('none')
    ax.spines['left'].set_smart_bounds(True)
    ax.spines['bottom'].set_smart_bounds(True)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    bounds = np.array([ax.axes.get_xlim(), ax.axes.get_ylim()])
    ax.plot(bounds[0][0],bounds[1][0],'')
    ax.plot(bounds[0][1],bounds[1][1],'')
    # ax.plot(bounds, '')

def plotSquare(x,color='b'):
    y = np.concatenate((x,x[:,[0]]),axis=1)
    plt.plot(y[0],y[1],'b-')
    plt.plot(y[0,0],y[1,0],'ro')
    plt.plot(y[0,1],y[1,1],'go')
    plt.plot(y[0,2],y[1,2],'co')
    plt.plot(y[0,3],y[1,3],'yo')
    plt.fill(x[0],x[1],color,alpha=0.15)

def plotShape(x,color='b'):
    y = np.concatenate((x,x[:,[0]]),axis=1)
    plt.plot(y[0],y[1],'{}-'.format(color))
    plt.fill(x[0],x[1],color,alpha=0.15)
    

if __name__ == "__main__":
    
    # circle = np.zeros((2,20))
    # for i in range(20):
    #     circle[0,i] = np.sin(2 * 3.14 * (i/20.0))
    #     circle[1,i] = np.cos(2 * 3.14 * (i/20.0))

    # fig = plt.figure()
    # ax = fig.add_subplot(111, aspect='equal')
    # plt.plot(circle[0,:],circle[1,:],'o')

    square = np.array([[0.0,1,1,0],[1,1,0,0]])

    fig = plt.figure()
    ax = plotSetup(-4,4,-4,4)
    centerAxes(ax)
    plotSquare(square)

    # shear matrix
    shear = np.array([[1.0, 1.5],[0.0,1.0]])
    ssquare = shear.dot(square)
    plotSquare(ssquare)

    # rotation matrix
    angle = 10.0
    theta = (angle/360.0) * 2.0 * np.pi
    rotate = np.array([[np.cos(theta), -np.sin(theta)],[np.sin(theta), np.cos(theta)]])
    rsquare = rotate.dot(square)
    plotSquare(2*rsquare)
    
