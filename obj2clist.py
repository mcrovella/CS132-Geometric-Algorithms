import numpy as np
import sys
import matplotlib as mp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def obj2flist(fp):
    """
    reads a standard .obj file as used in solid modeling.
    returns a list of 2-d numpy arrays, in which columns are vertices of a face.
    """
    vertices = []
    faces = []
    for line in fp:
        tokens = line.split()
        # vertex lines
        if ((len(tokens) > 0) and (tokens[0] == 'v')):
            vertices.append([float(tokens[1]), float(tokens[2]), float(tokens[3])])
        # face lines
        elif ((len(tokens) > 0) and (tokens[0] == 'f')):
            # note that .obj arrays index from 1
            # each face is a set of indices into the vertex array,
            # with optional additional properties following slashes
            face = [int(t.split('/')[0])-1 for t in tokens[1:]] + [int(tokens[1].split('/')[0])-1]
            faces.append(face)
    coords = [np.array([vertices[i] for i in f]).T for f in faces]
    return coords

def objCenter(flist):
    """
    computes an approximate object center to be used for translation, rotation, etc.
    flist is a list of faces.
    """
    flat = np.concatenate(flist,axis=1)
    return (np.min(flat,axis=1) + np.max(flat,axis=1))/2.0

def homogenize(flist):
    """
    convert every point in flist to homogeneous coordinates.
    flist is a list of faces.
    """
    return [np.concatenate((f,np.ones((1,np.shape(f)[1])))) for f in flist]

def wrl2flist(fp):
    """
    reads a standard .wrl file as used in VRML
    returns a list of 2-d numpy arrays, in which columns are vertices of a face.
    """
    vertices = []
    faces = []
    base = True
    C1 = False
    C2 = False
    F1 = False
    F2 = False
    debug = False
    for line in fp:
        tokens = line.split()
        if (len(tokens) == 0):
            continue
        elif (base and line.find("Coordinate3") != -1):
            C1 = True
            base = False
        elif (C1 and line.find("point") != -1):
            C2 = True
            C1 = False
        elif (C2 and line.find("]") == -1):
            tk = line.rstrip(',\n').split()
            vertices.append([float(tk[0]),float(tk[1]),float(tk[2])])
            if (debug): print("appending vertex {}".format(vertices[-1]))
        elif (C2 and line.find("]") != -1):
            C2 = False
            base = True
        elif (base and line.find("IndexedFaceSet") != -1):
            F1 = True
            base = False
        elif (F1 and line.find("coordIndex") != -1):
            F2 = True
            F1 = False
        elif (F2 and line.find("]") == -1):
            tk = line.split(',')
            if (tk[-2] != "-1"):
                print("error in parsing faces; line doesnt end a face (-1)")
            faces.append([int(f) for f in tk[:-2]])
            if (debug): print("appending face {}".format(faces[-1]))
        elif (F2 and line.find("]") != -1):
            F2 = False
            base = True
    coords = [np.array([vertices[i] for i in f]).T for f in faces]
    return coords

# simple test code
if __name__ == "__main__":
    fp = open('largeBall.obj','r')
    # fp = open('largeHouse.obj','r')

    c = obj2flist(fp)
    fig = plt.figure()
    ax = fig.add_subplot(111,projection='3d')
    for i in range(len(c)):
       ax.plot(c[i][0,:],c[i][1,:],'b',zs=c[i][2,:])
    plt.show()

    
