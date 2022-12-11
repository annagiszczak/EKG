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


        self.setWindowIcon(QIcon('icons/app_icon.png'))
        self.setWindowTitle("EKG")
        self.resize(800, 600)

        self.x = []
        self.ecg = []

        self.ecg_peaks_methods = ["neurokit", "pantompkins1985", "hamilton2002", "elgendi2010", "engzeemod2012", "gamboa2008"]
        self.ecg_clean_methods = ["neurokit", "biosppy", "pantompkins1985", "hamilton2002", "elgendi2010", "engzeemod2012"]        
        
        def create_menuBar():
            def open():
                # self.x = np.arange(0,15000)
                # self.ecg = nk.ecg_simulate(duration = 15, sampling_rate = 1000, heart_rate = 80)
                # ecg_line.setData(self.x, self.ecg)
                
                #read file
                filename = QFileDialog.getOpenFileName(self, 'Open file', './data/')
                #read file

            def save():
                print('clicked save')

            def help():
                print('clicked help')

            def quit():
                QApplication.quit()


            self.menuBar = self.menuBar()

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

        def ecg_clean_f(i):
            if len(self.x) == 0:
                print('open file')
            else:
                ecg_cleaned = nk.ecg_clean(self.ecg, 1000, self.ecg_clean_methods[i])
                ecg_line.setData(self.x, ecg_cleaned)

        def create_ecg_clean_combo():
            ecg_clean_label = QLabel("Clean method")
            self.comboLayout.addWidget(ecg_clean_label)

            ecg_clean =  QComboBox()
           
            for method in self.ecg_clean_methods:
                ecg_clean.addItem(method) 

            ecg_clean.activated[int].connect(ecg_clean_f)   
            self.comboLayout.addWidget(ecg_clean)

        def ecg_peaks_f(i):
            if len(self.x) == 0:
                print('open file')
            else:
                s, info = nk.ecg_peaks(self.ecg, method = 'neurokit', correct_artifacts = True)
                for peaks in info["ECG_R_Peaks"]:
                    self.graphWidget.addItem(pg.InfiniteLine(peaks, pen = pg.mkPen(color=(255, 0, 0))))
                   


        def create_ecg_peaks_combo():
            ecg_peak_label = QLabel("Find peak method")
            self.comboLayout.addWidget(ecg_peak_label)

            ecg_peaks = QComboBox()
            for method in self.ecg_peaks_methods:
                ecg_peaks.addItem(method)

            self.comboLayout.addWidget(ecg_peaks)
            ecg_peaks.activated[int].connect(ecg_peaks_f)  



        create_menuBar()

        self.centralWidget = QWidget()

        self.setCentralWidget(self.centralWidget)

        self.gridLayout = QGridLayout()
        self.centralWidget.setLayout(self.gridLayout)

        self.graphWidget = pg.PlotWidget(background=QColor(69, 83, 100, 255)) #setting graph

        ecg_line = self.graphWidget.plot(self.x, self.ecg)

        self.gridLayout.addWidget(self.graphWidget, 0, 0) 

        self.comboLayout = QVBoxLayout()
        self.comboLayout.addStretch()
   

        self.gridLayout.addLayout(self.comboLayout, 0, 1)
        
        create_ecg_clean_combo()

        self.comboLayout.addStretch()

        create_ecg_peaks_combo()

        self.comboLayout.addStretch()
        self.comboLayout.addStretch()
        self.comboLayout.addStretch()

        # self.button = QPushButton("SAVE")
        # self.button.clicked.connect(save())
        # self.gridLayout.addWidget(self.button, 1, 1)