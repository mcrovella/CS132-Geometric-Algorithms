'''
Created on Wed Jan 16 17:40:27 2013
Author: Indranil Sinharoy
Licence: BSD
'''
from __future__ import division
#import Matplotlib related modules
import matplotlib
matplotlib.use('TkAgg')
#import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.widgets import Button
#import Tkinter related modules
import tkinter as Tk
import sys
#import Numpy
import numpy as np

#disable 'Casting complex values' warning to the console. complex values/vectors
#warning is indicated on plot.
import warnings
warnings.simplefilter('ignore', np.ComplexWarning)

#define some global variables
global A,fig,ax,oldModeText,tlr,root,line1old,line2old,text1old,text2old,bSVD,svdVis
global line3old,line4old,text3old,text4old,egv1,egv2,singv1,singv2,redrawCount
global egv1txt,egv2txt,indTxt,svd1txt,svd2txt,w


#List of matrices for analysis ...one can add more...
matrixList = ['[[ 5/4,  0 ],[  0 , 3/4]]',
              '[[ 5/4,  0 ],[  0 ,-3/4]]',
              '[[ 1,    0 ],[  0 ,  1 ]] : (Identity matrix)',
              '[[ 0,    1 ],[  1 ,  0 ]] : (Reflection matrix)',
              '[[ 0,    1 ],[ -1 ,  0 ]] : (Rotation by 90 deg)',
              '[[ 1,   6 ],[5 , 2]] : (Lecture Example)',
              '[[ 1/4, 3/4],[ 4/4, 2/4]]',
              '[[ 1/4, 3/4],[ 2/4, 4/4]]',
              '[[ 3/4, 1/4],[ 4/4, 2/4]]',
              '[[ 3/4, 1/4],[-2/4, 4/4]]',
              '[[ 2/4, 4/4],[ 2/4, 4/4]]',
              '[[ 2/4, 4/4],[-1/4,-2/4]]',
              '[[ 6/4, 4/4],[-1/4,-2/4]]',
              '[[ 0.5, 0.5],[ 0.5, 0.5]] : (Projection matrix)',
              '[[ 0.8, 0.3],[ 0.2, 0.7]] : (Markov matrix)',
              'randn(2,2) : (Random matrix)']

def randn(a,b):
    return np.random.rand(4).reshape(a,b)

def tkQuit():
    '''Stop Tk main loop and destroy figure canvas'''
    global root
    root.quit()       # stops tk mainloop
    root.destroy()    # necessary to call, at least in windows

def resetAxes():
    global ax, w
    ax.clear()   #Clear axes if already drawn
    lim = np.max([1.5, np.round(np.abs(np.max(w)))])
    ax.set_xlim(-lim,lim)
    ax.set_ylim(-lim,lim)
    ax.set_aspect('equal')

def selectMatrix(num=1):
    '''To select a particular matrix'''
    global A
    mat = matrixList[num].partition(':')[0]
    expression = 'np.matrix('+mat+')'
    A = eval(expression)
    reset()

def toggleSVDmode(event=None):
    '''Function to determine/toggle the visibility of y and Ay'''
    global bSVD, svdVis,indTxt
    bSVD = not(bSVD)
    svdVis = not(svdVis)
    indTxt.set_visible(False)
    reset()

def toggleEigenSVDvectorsVisibility(event):
    '''Function to determine/toggle the visibility of the eigen and
       singular vectors '''
    global egv1, egv2, singv1,singv2,egv1txt,egv2txt,svd1txt, svd2txt
    #Toggle visibility of the eigen vectors
    visible = egv1.get_visible()
    egv1.set_visible(not visible and not bSVD)
    egv2.set_visible(not visible and not bSVD)
    egv1txt.set_visible(not visible and not bSVD)
    egv2txt.set_visible(not visible and not bSVD)
    #Toggle for the svd vectors
    visible = singv1.get_visible()
    singv1.set_visible(not visible and bSVD)
    singv2.set_visible(not visible and bSVD)
    svd1txt.set_visible(not visible and bSVD)
    svd2txt.set_visible(not visible and bSVD)
    redrawPlot(event)
    drawlegend()

def reset(event=None):
    '''Reset - clear the current plot, set axes, re-draw plot and legend'''
    global redrawCount
    redrawCount = 0
    resetAxes()
    drawPlot()
    drawlegend()

def closeFigure(event):
    '''Close the main figure'''
    tkQuit()

def rotMat2D(angle,angleType='r'):
    '''Return a 2D Rotation Matrix based on the input angle. The rotation is
    performed in Euclidean space.'''
    if angleType=='d':
        angle = np.radians(angle)
    R = np.matrix(((np.cos(angle),-np.sin(angle)),
                   (np.sin(angle), np.cos(angle))))

    return R

def redrawPlot(event):
    '''This function is called for every mouse-click. It calculated x, Ax, y, Ay,
    and re-draws it on the canvas. Since the canvas is not changed, the visibility
    of older lines are set to false'''
    global line1old,line2old,line3old,line4old
    global text1old,text2old,text3old,text4old
    global svdVis,bSVD, redrawCount
    t = ax.get_window_extent().extents  #returns x_0,y_0,x_1,y_1 for the axes in pixels
    if ((-1 <= event.xdata <=1) and (-1 <= event.ydata <=1) and # mouse click within unit circle
        (t[0]<=event.x <= t[2]) and (t[1]<= event.y<=t[3])):    # mouse click within the axes (necessary)
        x = np.matrix([event.xdata,event.ydata]).T
        x = x/np.linalg.norm(x)                  #normalize the vector
        Axnew = A*x
        y = rotMat2D(np.pi/2)*x                 #perpendicular to x
        y = y/np.linalg.norm(y)                 #normalize
        Aynew = A*y

        #The purpose of zordering (toggling) the scatter plot is that both red
        #and blue scatter dots can be seen if they exactly overlap
        zorder_b = 20
        zorder_r = zorder_b + (-1)**redrawCount
        redrawCount+=1

        ax.scatter(x[0,0],x[1,0],c=u'r',marker='o',s=18, alpha=1.0,\
        zorder=zorder_r) # x
        ax.scatter(Axnew[0,0],Axnew[1,0],c=u'b',marker='o',s=18, alpha=1.0,\
        zorder=zorder_b) # Ax
        if bSVD:
            ax.scatter(y[0,0],y[1,0],c=u'r',marker='o',s=18, alpha=1.0,\
            zorder=zorder_r) # y
            ax.scatter(Aynew[0,0],Aynew[1,0],c=u'b',marker='o',s=18,alpha=1.0,\
            zorder=zorder_b) #Ay

        #erase the old lines
        line1old.set_visible(False); line2old.set_visible(False)
        text1old.set_visible(False); text2old.set_visible(False)
        line3old.set_visible(False); line4old.set_visible(False)
        text3old.set_visible(False); text4old.set_visible(False)

        #draw new lines -- x and Ax
        line1new, = ax.plot([0.0,x[0,0]],[0.0,x[1,0]],c='r',aa=True)
        line2new, = ax.plot([0.0,Axnew[0,0]],[0.0,Axnew[1,0]],c='b',aa=True)
        text1new = ax.text( (0.0 + 0.8*tlr*x[0,0]),(0.0 + 0.8*tlr*x[1,0]),\
        '$x$',fontsize=15,color='r',bbox=dict(facecolor='white',\
        edgecolor='white',alpha=0.5) )
        text2new = ax.text( (0.0 + tlr*Axnew[0,0]),(0.0 + tlr*Axnew[1,0]),\
        '$Ax$',fontsize=15,color='b',bbox=dict(facecolor='white',\
        edgecolor='white',alpha=0.5) )

        #draw new lines -- y and Ay
        line3new, = ax.plot([0.0,y[0,0]],[0.0,y[1,0]],c='m',aa=True)
        line4new, = ax.plot([0.0,Aynew[0,0]],[0.0,Aynew[1,0]],c='g',aa=True)
        text3new = ax.text( (0.0 + 0.8*tlr*y[0,0]),(0.0 + 0.8*tlr*y[1,0]),\
        '$y$',fontsize=15,color='m',bbox=dict(facecolor='white',\
        edgecolor='white',alpha=0.5) )
        text4new = ax.text( (0.0 + tlr*Aynew[0,0]),(0.0 + tlr*Aynew[1,0]),\
        '$Ay$',fontsize=15,color='g',bbox=dict(facecolor='white',\
        edgecolor='white',alpha=0.5))
        line3new.set_visible(svdVis);line4new.set_visible(svdVis)
        text3new.set_visible(svdVis);text4new.set_visible(svdVis)

        line1old,line2old = line1new,line2new
        text1old,text2old = text1new,text2new
        line3old,line4old = line3new,line4new
        text3old,text4old = text3new,text4new
    fig.canvas.draw()

def drawPlot():
    '''Function to set up the lines, calculate the eigenvalue and svd '''
    global tlr,line1old,line2old,line3old,line4old
    global text1old,text2old,text3old,text4old, oldModeText
    global egv1, egv2, singv1, singv2 ,bSVD
    global egv1txt, egv2txt,indTxt, svd1txt, svd2txt
    global A, fig, ax, root, w #(w is make a global as it is used in resetAxis())
    # update the figure text to indicate current mode (eigen/svd)
    if bSVD:
        currmode = 'SVD'
    else:
        currmode = 'Eigen'
    #Calculate the eigen value and set the axis limits accordingly
    w, v = np.linalg.eig(A)   # w contains the eigen values, v contains the eigen vectors
    resetAxes()
    detA = np.linalg.det(A)   #determinant
    # rankA = np.rank(A)        #rank
    traceA = np.trace(A)      #trace

    #complexity test
    if np.sum(np.iscomplex(v)) >= 1:
        complexEigenVecs = True
    else:
        complexEigenVecs = False
    if np.sum(np.iscomplex(w)) >= 1:
        complexEigenVals = True
    else:
        complexEigenVals = False

    #fixed text to show the array
    arrtext = 'Matrix A = \n[[%1.3f, %1.3f],\n[%1.3f, %1.3f]]\n\ndet(A) \
    = \n%1.3f\n\ntrace(A) = \n%1.3f\n\nrank(A) = \n' \
    %(A[0,0],A[0,1],A[1,0],A[1,1],detA,traceA)
    fig.text(0.013,0.20,arrtext,fontsize='medium',color='b',\
    bbox=dict(facecolor='white',edgecolor='white',alpha=1.0),zorder=0)

    #fixed text to indicate mode (eigen mode/svd mode)
    oldModeText.set_visible(False)
    modeText = fig.text(0.04,0.8,currmode,fontsize='xx-large',\
    fontweight='semibold',color='#FF8000')
    oldModeText = modeText

    #starting lines/vectors
    xstart = np.matrix([1,0]).T
    ystart = np.matrix([0,1]).T  #for svd mode
    Axstart = np.dot(A,xstart)
    Aystart = np.dot(A,ystart)   #for svd mode

    #Plot the columns of the matrix A
    col1, = ax.plot([0.0,A[0,0]],[0.0,A[1,0]],'k--',alpha=0.6,lw='3',\
    label='$col_1(A)$')
    col2, = ax.plot([0.0,A[0,1]],[0.0,A[1,1]],'k--',alpha=0.4,lw='2',\
    label='$col_2 (A)$')

    #plot the eigen vectors (it will not be seen initially as the visibility is false)
    #w, v = np.linalg.eig(A)   # moved up
    egv1, = ax.plot([0.0,v[0,0]],[0.0,v[1,0]],'b',lw='2',alpha=0.5,\
    aa=True,label='$eigvec_1$',visible=False)
    egv2, = ax.plot([0.0,v[0,1]],[0.0,v[1,1]],'r',lw='2',alpha=0.5,\
    aa=True,label='$eigvec_2$',visible=False)
    egv1str = 'e0=%1.2f, v0=[%1.3f,%1.3f]'%(w[0],v[0,0],v[1,0])
    egv2str = 'e1=%1.2f, v1=[%1.3f,%1.3f]'%(w[1],v[0,1],v[1,1])
    egv1txt = ax.text(0.01,0.06,egv1str,ha='left',color='r',\
    bbox=dict(facecolor='white',edgecolor='white',alpha=1.0),\
    visible=False,transform = ax.transAxes)
    egv2txt = ax.text(0.01,0.02,egv2str,ha='left',color='r',\
    bbox=dict(facecolor='white',edgecolor='white',alpha=1.0),\
    visible=False,transform = ax.transAxes)

    #calculate the svd
    U,S,V = np.linalg.svd(A)

    #complexity test
    if np.sum(np.iscomplex(U)) >= 1:
        complexSingVecs = True
    else:
        complexSingVecs = False
    if np.sum(np.iscomplex(S)) >= 1:
        complexSingVals = True
    else:
        complexSingVals = False

    #plot the svd (it will not be seen initially as the visibility is false)
    singv1, = ax.plot([0.0,U[0,0]],[0.0,U[1,0]],'g--',lw='2',alpha=0.5,\
    aa=True,label='$singvec_1$',visible=False)
    singv2, = ax.plot([0.0,U[0,1]],[0.0,U[1,1]],'m--',lw='2',alpha=0.5,\
    aa=True,label='$singvec_2$',visible=False)
    svd1str = 's0=%1.2f, u0=[%1.3f,%1.3f]'%(S[0],U[0,0],U[1,0])
    svd2str = 's1=%1.2f, u1=[%1.3f,%1.3f]'%(S[1],U[0,1],U[1,1])
    svd1txt = ax.text(0.01,0.06,svd1str,ha='left',color='r',\
    bbox=dict(facecolor='white',edgecolor='white',alpha=1.0),visible=False,\
    transform = ax.transAxes)
    svd2txt = ax.text(0.01,0.02,svd2str,ha='left',color='r',\
    bbox=dict(facecolor='white',edgecolor='white',alpha=1.0),visible=False,\
    transform = ax.transAxes)

    #lines related to just the eigen vectors
    line1, = ax.plot([0.0,xstart[0,0]],[0.0,xstart[1,0]],aa=True,c='r')
    line2, = ax.plot([0.0,Axstart[0,0]],[0.0,Axstart[1,0]],aa=True,c='b')
    text1 = ax.text( (0.0 + 0.8*tlr*xstart[0,0]),(0.0 + 0.8*tlr*xstart[1,0]),\
    '$x$',fontsize=15,color='r',bbox=dict(facecolor='white',edgecolor='white',\
    alpha=0.5) )
    text2 = ax.text( (0.0 + tlr*Axstart[0,0]),(0.0 + tlr*Axstart[1,0]),'$Ax$',\
    fontsize=15,color='b',bbox=dict(facecolor='white',edgecolor='white',alpha=0.5))
    line1old,line2old = line1,line2
    text1old,text2old = text1,text2

    #lines related to just the svd vectors (depending on the svdVis)
    line3, = ax.plot([0.0,ystart[0,0]],[0.0,ystart[1,0]],aa=True,c='m',\
    visible=svdVis)
    line4, = ax.plot([0.0,Aystart[0,0]],[0.0,Aystart[1,0]],aa=True,c='g',\
    visible=svdVis)
    text3 = ax.text( (0.0 + 0.8*tlr*ystart[0,0]),(0.0 + 0.8*tlr*ystart[1,0]),\
    '$y$',fontsize=15,color='m',bbox=dict(facecolor='white',edgecolor='white',\
    alpha=0.5),visible=svdVis)
    text4 = ax.text( (0.0 + tlr*Aystart[0,0]),(0.0 + tlr*Aystart[1,0]),'$Ay$',\
    fontsize=15,color='g',bbox=dict(facecolor='white',edgecolor='white',\
    alpha=0.5),visible=svdVis)
    line3old,line4old = line3,line4
    text3old,text4old = text3,text4

    #Text to indicate complex/real nature of vectors and values
    if complexEigenVals and not bSVD:
        comValTxt = ax.text(0- 0.5*ax.get_xlim()[1],0.5*ax.get_ylim()[1],\
        'Complex eigen values',ha='left',\
        color='y',fontsize='large',fontweight='bold',alpha=0.4)
    if complexEigenVecs and not bSVD:
        comVecTxt = ax.text(0- 0.5*ax.get_xlim()[1],0.4*ax.get_ylim()[1],\
        'Complex eigen vectors',ha='left',\
        color='y',fontsize='large',fontweight='bold',alpha=0.4)
    if complexSingVals and bSVD:
        comValTxt = ax.text(0- 0.5*ax.get_xlim()[1],0.5*ax.get_ylim()[1],\
        'Complex singular values',ha='left',\
        color='y',fontsize='large',fontweight='bold',alpha=0.4)
    if complexSingVecs and bSVD:
        comVecTxt = ax.text(0- 0.5*ax.get_xlim()[1],0.4*ax.get_ylim()[1],\
        'Complex singular vectors',ha='left',\
        color='y',fontsize='large',fontweight='bold',alpha=0.4)

    # Text to indicate goal
    if not bSVD:
        indStr = 'Make A*x parallel to x               .'  #don't change space
    else:
        indStr = 'Make A*x perpendicular to A*y .'  #don't change space
    indTxt = fig.text(0.3,0.03,indStr,ha='left',color='g',fontsize='large',\
    fontweight='bold',bbox=dict(facecolor='white',edgecolor='white',alpha=1.0),\
    visible=True)

def drawlegend():
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1),ncol=3, \
    fancybox=True, shadow=True)

def eigshow(matrix = None):
    '''Main function to plot eigshow.
    Usage: eigshow()
           or
           eigshow(A)
    where, A is a Numpy 2x2 matrix or array.
    When no aguments are passed to eigshow(), it starts with a default matrix
    A = np.matrix([[1/4,3/4],[1,2/4]]) and one can choose several other matrices
    using the 'Select Matrix' menu on the top menu panel.
    When A is given, eigshow starts with the given matrix.'''
    global line1old,line2old,text1old,text2old,line3old,line4old,text3old
    global text4old,egv1,egv2,singv1,singv2,egv1txt,egv2txt,indTxt
    global svd1txt, svd2txt, bSVD, svdVis, oldModeText, tlr, redrawCount
    global root, A, fig, ax

    bSVD = False   #svd mode or not (initially set to eigen mode)
    svdVis = False #Visibility of lines for svd mode (not visible in eigen mode)
    tlr = 0.75 #text on line position ratio
    redrawCount = 0

    if matrix == None:
        #The matrix (initial matrix)
        A = np.matrix([[1/4,3/4],[1,2/4]])  #matrixList[4]
    else:
        A = np.matrix(matrix)

    root = Tk.Tk()
    root.wm_title('eigshow')

    #Create a toplevel menu (for selecting matrices)
    menubar = Tk.Menu(root)

    #Create the Matrix pulldown menu, and add it to the menubar
    filemenu = Tk.Menu(menubar,tearoff=0)
    for i, mat in enumerate(matrixList):
        expression = \
        'filemenu.add_command(label=mat,command=lambda: selectMatrix({}))'.format(i)
        eval(expression)
    menubar.add_cascade(label='Select Matrix',menu=filemenu)

    #Display the menu
    root.config(menu=menubar)

    #Create a figure and an axes within it
    fig = Figure(facecolor='w')
    ax = fig.add_subplot(111)

    # a tk drawing area
    canvas = FigureCanvasTkAgg(fig,master=root)#no resize callback as of now
    canvas.get_tk_widget().pack(side=Tk.BOTTOM)

    #Connect redrawPlot callback function to mouse-click event
    fig.canvas.mpl_connect('button_press_event',redrawPlot)

    #buttons on the right on main figure
    ax_reset = fig.add_axes([0.83, 0.70, 0.16, 0.12])
    b_reset = Button(ax_reset, 'Reset',color='0.95',hovercolor='0.85')
    b_reset.on_clicked(reset)

    ax_eigen_svd = fig.add_axes([0.83, 0.55, 0.16, 0.12])
    b_eigen_svd =Button(ax_eigen_svd,'Eigen/SVD',color='0.95',hovercolor='0.85')
    b_eigen_svd.on_clicked(toggleSVDmode)

    ax_showvecs = fig.add_axes([0.83, 0.40, 0.16, 0.12])
    b_showvecs = Button(ax_showvecs, 'Show\nEigen/Singular\nvectors',\
    color='0.95', hovercolor='0.85')
    b_showvecs.on_clicked(toggleEigenSVDvectorsVisibility)

    ax_closeFig = fig.add_axes([0.83, 0.25, 0.16, 0.12])
    b_closeFig = Button(ax_closeFig,'Close',color='0.95',hovercolor='0.85')
    b_closeFig.on_clicked(closeFigure)

    #Initialize some of the objects (lines, texts, etc)
    oldModeText = fig.text(0.01,0.8,'dummytext',fontsize='large')  #dummy text

    #Start rendering the plot
    drawPlot()

    drawlegend()

    #Draw the plot on the canvas
    canvas.draw()

    Tk.mainloop()

if __name__ == '__main__':
    eigshow()
