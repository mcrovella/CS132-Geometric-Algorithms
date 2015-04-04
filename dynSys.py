import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# A = np.array([[1.1, 0],[0, 0.9]])
# A = np.array([[0.8, 0.5],[-0.1, 1.0]])
A = np.array([[np.cos(0.1),-np.sin(0.1)],[ np.sin(0.1),np.cos(0.1)]])

# we are putting x into an array so that it can be read inside the
# animate() closure.   Currently can only read bound variables in a closure
x = [np.array([1,500.])]

fig = plt.figure()
ax = plt.axes(xlim=(-500,500),ylim=(-500,500))
plt.plot(-500, -500,'')
plt.plot(500, 500,'')
plt.axis('equal')

# this is the routine that will be called on each timestep
def animate(i):
    newx = A.dot(x[0])
    plt.plot([x[0][0],newx[0]],[x[0][1],newx[1]],'r-')
    plt.plot(newx[0],newx[1],'ro')
    x[0] = newx
    # fig.canvas.draw()

# instantiate the animator.
# we are animating at 3Hz
anim = animation.FuncAnimation(fig, animate, 
                                    frames=75, interval=1000/3, repeat=False, blit=False)
plt.show()


    
