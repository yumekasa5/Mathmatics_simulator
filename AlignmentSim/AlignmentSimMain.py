# *-* coding: utf-8 *-*
import sys
import random
import matplotlib
matplotlib.use('Qt5Agg')

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QApplication
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from MplCanvas import MplCanvas2D
from MplCanvas import MplCanvas3D
from AlignmentSim.MainWindowUI import Ui_MainWindow


class AlignmentSimMainClass(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Canvasにグラフを描画
        # self.canvas = MplCanvas2D(self, width=5, height=4, dpi=100)
        self.canvas = MplCanvas3D(self, width=5, height=4, dpi=100)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.ui.formLayout.addWidget(self.toolbar)
        self.ui.formLayout.addWidget(self.canvas)
        

        # 座標軸をベクトルで表示する
        self.origin = [0, 0, 0]
        self.x = [1, 0, 0]
        self.x = [3, 0, 0]
        self.canvas.axes.quiver(
            *self.origin, 
            *self.x,  
            color='r'
            )
        
        self.canvas.axes.set_xlim(-10, 10)
        self.canvas.axes.set_ylim(-10, 10)
        self.canvas.axes.set_zlim(-10, 10)
        self.update_plot()

        self.show()

        # Setup a timer to trigger the redraw by calling update_plot.
        # self.timer = QTimer()
        # self.timer.setInterval(100)
        # self.timer.timeout.connect(self.update_plot)
        # self.timer.start()

    def update_plot(self):
        # Drop off the first y element, append a new one.
        # self.ydata = self.ydata[1:] + [random.randint(0, 10)]
        self.canvas.axes.cla()  # Clear the canvas.
        self.canvas.axes.set_xlim(-10, 10)
        self.canvas.axes.set_ylim(-10, 10)
        self.canvas.axes.set_zlim(-10, 10)        
        self.canvas.axes.quiver(*self.origin, *self.x, color='r')
        # Trigger the canvas to update and redraw.
        self.canvas.draw()
