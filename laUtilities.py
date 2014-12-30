import numpy as np
import matplotlib as mp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plotSetup(xmin = -6.0, xmax = 6.0, ymin = -2.0, ymax = 4.0):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    plt.xlim([xmin, xmax])
    plt.ylim([ymin, ymax])
    return ax

def formatEqn(coefs, b):
    leadingLabel = {-1: '-{} x_{}', 0: '', 1: '{} x_{}'}
    followingLabel = {-1: ' - {} x_{}', 0: '', 1: ' + {} x_{}'}
    nterms = len(coefs)
    i = 0
    # skip initial terms with coefficient zero
    while ((i < nterms) and (np.sign(coefs[i]) == 0)):
        i += 1
    # degenerate equation 
    if (i == nterms):
        return '0 = {}'.format(b)
    # first term is formatted slightly differently
    if (np.abs(coefs[i]) == 1):
        label = leadingLabel[np.sign(coefs[i])].format('',i+1)
    else:
        label = leadingLabel[np.sign(coefs[i])].format(np.abs(coefs[i]),i+1)
    # and the rest of the terms if any exist
    for j in range(i+1,len(coefs)):
        if (np.abs(coefs[j]) == 1):
            label = followingLabel[np.sign(coefs[j])].format('',j+1)
        else:
            label = label + followingLabel[np.sign(coefs[j])].format(np.abs(coefs[j]),j+1)
    label = label + ' = {}'.format(b)
    return label

def plotLinEqn (a1, a2, b):
    # a1 x + a2 y = b
    [xmin, xmax] = plt.xlim()
    x1 = xmin
    y1 = (b - (x1 * a1))/float(a2)
    x2 = xmax
    y2 = (b - (x2 * a1))/float(a2)
    plt.plot([x1, x2],[y1, y2], label='${}$'.format(formatEqn([a1, a2],b)))

def centerAxes (ax):
    ax.spines['left'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_position('zero')
    ax.spines['top'].set_color('none')
    ax.spines['left'].set_smart_bounds(True)
    ax.spines['bottom'].set_smart_bounds(True)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

def plotSetup3d(xmin = -3.0, xmax = 3.0, ymin = -3.0, ymax = 3.0, zmin = -3.0, zmax = 3.0):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.axes.set_xlim([xmin, xmax])
    ax.axes.set_ylim([ymin, ymax])
    ax.axes.set_zlim([zmin, zmax])
    return ax

def plotLinEqn3d(ax, a1, a2, a3, b, color):
    from matplotlib.tri import Triangulation
    # a1 x + a2 y + a3 z = b
    pts = intersectionPlaneCube(ax, a1, a2, a3, b)
    ptlist = triangulatePoints(pts)
    x = ptlist[:,0]
    y = ptlist[:,1]
    z = ptlist[:,2]
    tris = []
    for i in range(len(ptlist)-2):
        tris.append([0,i+1,i+2])
    tri = Triangulation(x, y, tris)
    ax.plot_trisurf(tri, z, color=color, alpha=0.3, linewidth=0)

def triangulatePoints(p):
    # construct a correct triangulation of the input points 
    pts = [np.array(i) for i in p]
    next = pts.pop(0)
    tset = [next]
    while (len(pts)>0):
        dists = [np.linalg.norm(next-pts[i]) for i in range(len(pts))]
        next = pts.pop(np.argmin(dists))
        tset.append(next)
    return np.array(tset)
    

def intersectionPlaneCube(ax, a1, a2, a3, b):
    # returns the vertices of the polygon defined by the intersection of a plane
    # and the rectangular prism defined by the limits of the axes
    xmin, xmax = ax.axes.get_xlim()
    ymin, ymax = ax.axes.get_ylim()
    zmin, zmax = ax.axes.get_zlim()
    bounds = [[xmin, xmax], [ymin, ymax], [zmin, zmax]]
    coefs = [a1, a2, a3]
    points = []
    for x in [0, 1]:
        for y in [0, 1]:
            for z in [0, 1]:
                corner = [x, y, z]
                # 24 corner-pairs 
                for i in range(3):
                    # but only consider each edge once (12 unique edges)
                    if corner[i] == 0:
                        # we are looking for the intesection of the line defined by
                        # the two constant values with the plane
                        isect = (b - np.sum([coefs[k] * corner[k] for k in range(3) if k != i]))/float(coefs[i])
                        if ((isect >= bounds[i][0]) & (isect <= bounds[i][1])):
                            pt = [bounds[k][corner[k]] for k in range(3)]
                            pt[i] = isect
                            points.append(tuple(pt))
    return set(points)

def plotIntersection3d(ax, a1, a2, a3, b, c1, c2, c3, d):
    xmin, xmax = ax.axes.get_xlim()
    ymin, ymax = ax.axes.get_ylim()
    zmin, zmax = ax.axes.get_zlim()
    def yzForx(x):
        y = (a3*d - a3*c1*x - c3*b + c3*a1*x)/float(a3*c2 - c3*a2)
        z = (b - a1*x - a2*y)/float(a3)
        return x,y
    x1 = xmin
    y1, z1 = yzForx(x1)
    x2 = xmax
    y2, z2 = yzForx(x2)
    ax.plot([x1, x2],[y1,y2],zs=[z1,z2])

# current status:
# these work:
ax = ut.plotSetup3d(0,1,0,1,0,1)
ut.plotLinEqn3d(ax, 1, 1, 1, 1, 'Beige')
ut.plotLinEqn3d(ax, 1, 1, 1, 1.5, 'Navy')
ut.plotLinEqn3d(ax, 1, 1, 1, 2, 'Green')
# this doesnt:
ax = ut.plotSetup3d()
ut.plotLinEqn3d(ax, 1, 1, 0.1, 0, 'Beige')
# nor does this:
ax = ut.plotSetup3d(0,1,0,1,0,1)
ut.plotLinEqn3d(ax, 1, 1, 0.1, 0, 'Beige')
