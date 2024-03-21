# https://gist.github.com/llandsmeer/4681f74efe0349eb187b508ca1575a42
import os

try:
    import numpy as np
except ImportError:
    print('Numpy package not found, install with')
    print('pip install numpy')
    exit(1)

try:
    import matplotlib.pyplot as plt
    from matplotlib.widgets import RadioButtons
    import matplotlib.widgets as W
    from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable
except ImportError:
    print('Matplotlib package not found, install with')
    print('pip install matplotlib')
    exit(1)

EXAMPLE_MATRICES =  [
    '2 0\n0 .5',
    '0.5 1\n0 0.5',
    '0.5 0\n0 2',
    '2 1\n0 2',
    '2 0\n0 -2',
    '1 -1\n1 0',
    '1.25 0\n0 0.75',
    '1.25 0\n0 -0.75',
    '1 0\n0 1',
    '0 1\n1 0',
    '0 1\n-1 0',
#   '0.25 0.75\n1 0.5',
#   '0.25 0.75\n0.5 1',
#   '0.75 0.25\n1 0.5',
#   '0.75 0.25\n-0.5 1',
#   '0.5 1\n0.5 1',
#   '0.5 1\n-0.25 -0.5',
#   '1.5 1\n-0.25 0.5',
    ]

class Eigshow:
    def __init__(self, color_x='blue', color_Ax='black'):
        self.fig, self.ax = fig, ax = plt.subplots()
        self.cid = fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.line_x, = ax.plot([0, 0], [0, 0], color=color_x, label='$x$')
        self.line_Ax, = ax.plot([0, 0], [0, 0], color=color_Ax, label='$A\\cdot x$')
        self.ellipse_Ax, = ax.plot([0], [0], '--', color=color_Ax, alpha=0.5)
        ax.axis('equal')
        ax.set_xlim([-2, 2])
        ax.set_ylim([-2, 2])
        self.A = np.random.random((2, 2))
        self.circle = circle = plt.Circle((0, 0), 1, ls='--', fill=False, color=color_x, alpha=0.5)
        ax.add_patch(circle)
        self.x = 1, 0
        self.d = d = make_axes_locatable(ax)
        self.rax = rax = d.append_axes('right', size='19%', pad='1%')
        self.rad = rad = RadioButtons(rax, EXAMPLE_MATRICES)
        for label in rad.labels:
            label.set_fontsize(9)
            label.set_linespacing(0.9)
        rad.on_clicked(self.on_radion_button_clicked)
        self.update_A()
        self.update_x()
        self.on_radion_button_clicked(EXAMPLE_MATRICES[0])
        ax.legend()
        fig.suptitle('Make $A\\cdot x$ parallel to $x$')
        fig.canvas.manager.set_window_title('Eigshow (python)')

    def on_motion(self, ev):
        mx, my = ev.xdata, ev.ydata
        if ev.button != 1 or mx is None or my is None:
            return
        angle = np.arctan2(my, mx)
        x, y = np.cos(angle), np.sin(angle)
        self.x = x, y
        self.update_x()

    def on_radion_button_clicked(self, label):
        self.A = A = np.array([[float(cell) for cell in row.split()] for row in label.splitlines()])
        self.update_A()

    def update_A(self):
        self.update_x()
        angle = np.linspace(0, 2*np.pi)
        x, y = np.cos(angle), np.sin(angle)
        Ax, Ay = self.A@ np.stack([x, y])
        self.ellipse_Ax.set_xdata(Ax)
        self.ellipse_Ax.set_ydata(Ay)
        self.fig.canvas.draw()

    def update_x(self):
        x, y = self.x
        self.line_x.set_xdata([0, x])
        self.line_x.set_ydata([0, y])
        Ax, Ay = self.A @ (x, y)
        self.line_Ax.set_xdata([0, Ax])
        self.line_Ax.set_ydata([0, Ay])
        self.fig.canvas.draw()

    def __del__(self):
        self.fig.canvas.mpl_disconnect(self.cid)

eig = Eigshow()
plt.show()
