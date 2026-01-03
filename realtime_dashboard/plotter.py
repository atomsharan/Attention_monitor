import sys

import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore, QtWidgets

class MetricsMonitor():
    def __init__(self, q):
        self.q = q
        pg.setConfigOptions(antialias=True)
        self.traces = dict()
        self.app = QtWidgets.QApplication(sys.argv)

        # Use GraphicsLayoutWidget within a QMainWindow (GraphicsWindow removed in recent pyqtgraph)
        self.win = QtWidgets.QMainWindow()
        self.win.setWindowTitle('Attention Monitor')
        self.central = pg.GraphicsLayoutWidget()
        self.win.setCentralWidget(self.central)

        self.win.resize(1000, 600)

        self.p1 = self.central.addPlot(row=0, col=0, title='Mouth Aspect Ratio (MAR)')
        self.p2 = self.central.addPlot(row=1, col=0, title='Eye Aspect Ratio (EAR)')
        self.p3 = self.central.addPlot(row=2, col=0, title='Head Pose (Yaw/Pitch/Roll)')

        self.p1.addLegend()
        self.p2.addLegend()
        self.p3.addLegend()

        self.x = np.arange(0, 2 * 60, 2)

    def start(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtWidgets.QApplication.instance().exec_()

    def set_plotdata(self, name, data_x, data_y):
        if name in self.traces:
            self.traces[name].setData(data_x, data_y)
        else:
            if name == 'mar':
                self.traces[name] = self.p1.plot(pen='y', name='mar')
            elif name == 'ear':
                self.traces[name] = self.p2.plot(pen='c', name='ear')
            elif name == 'yaw':
                self.traces[name] = self.p3.plot(pen='r', name='yaw')
            elif name == 'pitch':
                self.traces[name] = self.p3.plot(pen='g', name='pitch')
            elif name == 'roll':
                self.traces[name] = self.p3.plot(pen='b', name='roll')
            self.traces[name].setData(data_x, data_y)

    def update(self):
        if not self.q.empty():
            data = self.q.get()
            self.set_plotdata('mar', self.x, data['mar_stream'])
            self.set_plotdata('ear', self.x, data['ear_stream'])
            self.set_plotdata('yaw', self.x, data['yaw_stream'])
            self.set_plotdata('pitch', self.x, data['pitch_stream'])
            self.set_plotdata('roll', self.x, data['roll_stream'])

    def animation(self):
        self.win.show()
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(30)
        self.start()