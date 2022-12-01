import sys
import numpy as np

import neurokit2 as nk
import pyqtgraph as pg

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("EKG")
        self.resize(800, 600)


        self.x = []
        self.ecg = []
        # self.ecg_cleaned = []
        # Create a menu bar
        self.menuBar = self.menuBar()
        

        def open():
            self.x = np.arange(0,15000)
            self.ecg = nk.ecg_simulate(duration = 15, sampling_rate = 1000, heart_rate = 80)
            ecg_line.setData(self.x, self.ecg)

        def save():
            print('clicked save')

        def help():
            print('clicked help')

        def quit():
            QApplication.quit()

        def ecg_clean_f(i):
            if len(self.x) == 0:
                print('open file')
            elif i == 0:
                ecg_cleaned = nk.ecg_clean(self.ecg, 1000, 'neurokit')
                ecg_line.setData(self.x, ecg_cleaned)
            elif i == 1:
                ecg_cleaned = nk.ecg_clean(self.ecg, 1000, 'biosppy')
                ecg_line.setData(self.x, ecg_cleaned)
            elif i == 2:
                ecg_cleaned = nk.ecg_clean(self.ecg, 1000, 'pantompkins1985')
                ecg_line.setData(self.x, ecg_cleaned)
            elif i == 3:
                ecg_cleaned = nk.ecg_clean(self.ecg, 1000, 'hamilton2002')
                ecg_line.setData(self.x, ecg_cleaned)
            elif i == 4:
                ecg_cleaned = nk.ecg_clean(self.ecg, 1000, 'elgendi2010')
                ecg_line.setData(self.x, ecg_cleaned)
            elif i == 5:
                ecg_cleaned = nk.ecg_clean(self.ecg, 1000, 'engzeemod2012')
                ecg_line.setData(self.x, ecg_cleaned)

        def ecg_peaks_f(i):
            signals, info = nk.ecg_peaks(self.ecg, method = 'neurokit', correct_artifacts = True)
            for peaks in info["ECG_R_Peaks"]:
                self.graphWidget.addItem(pg.InfiniteLine(peaks, pen = pg.mkPen(color=(255, 0, 0))))




        open_action = QAction('Open', self)
        open_action.triggered.connect(lambda:open())
        self.menuBar.addAction(open_action)

        save_action = QAction('Save', self)
        save_action.triggered.connect(lambda:save())
        self.menuBar.addAction(save_action)

        help_action = QAction('Help', self)
        help_action.triggered.connect(lambda:help())
        self.menuBar.addAction(help_action)

        quit_action = QAction('&Quit', self)
        quit_action.triggered.connect(lambda:quit())
        self.menuBar.addAction(quit_action)

        self.centralWidget = QWidget()

        self.setCentralWidget(self.centralWidget)

        self.gridLayout = QGridLayout()
        self.centralWidget.setLayout(self.gridLayout)

        self.graphWidget = pg.PlotWidget(background='w') #setting graph

        ecg_line = self.graphWidget.plot(self.x, self.ecg)

        self.gridLayout.addWidget(self.graphWidget, 0, 0) 

        self.comboLayout = QVBoxLayout()
        self.gridLayout.addLayout(self.comboLayout, 0, 1)

        self.ecg_clean = QComboBox()
        self.ecg_clean.addItem("nuerokit")       
        self.ecg_clean.addItem("biosppy")  
        self.ecg_clean.addItem("pantompkin1985")
        self.ecg_clean.addItem("hamilton2002")
        self.ecg_clean.addItem("elgendi2010")
        self.ecg_clean.addItem("engzeemod2012")      

        self.ecg_clean.activated[int].connect(ecg_clean_f)   

        self.comboLayout.addWidget(self.ecg_clean)

        self.ecg_peaks = QComboBox()
        self.comboLayout.addWidget(self.ecg_peaks)
        self.ecg_peaks.addItem("neurokit")
        # self.ecg_peaks.addItem("biosppy")  
        # self.ecg_peaks.addItem("pantompkin1985")
        # self.ecg_peaks.addItem("hamilton2002")
        # self.ecg_peaks.addItem("elgendi2010")
        # self.ecg_peaks.addItem("engzeemod2012")

        self.ecg_peaks.activated[int].connect(ecg_peaks_f)   

        self.button = QPushButton("SAVE")
        self.button.clicked.connect(lambda:save())
        self.gridLayout.addWidget(self.button, 1, 1)