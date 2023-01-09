import sys
import numpy as np

import neurokit2 as nk
import pyqtgraph as pg

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from ishneholterlib import Holter
import wfdb
import os

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowIcon(QIcon('icons/app_icon.png'))
        self.setWindowTitle("EKG")
        self.resize(800, 600)

        self.x = []
        self.ecg = []
        self.ecg_cleaned = []
        self.peaks = []
        self.noext_fname = None
        self.fs = None

        self.ecg_peaks_methods = ["neurokit", "pantompkins1985", "hamilton2002", "gamboa2008"]
        self.ecg_clean_methods = ["neurokit", "biosppy", "pantompkins1985", "hamilton2002"]        
        
        def create_menuBar():
            def open_sim():
                self.x = np.arange(0,15000)
                self.ecg = nk.ecg_simulate(duration = 15, sampling_rate = 1000, heart_rate = 80)
                
                self.graphWidget.clear()
                
                ecg_line = self.graphWidget.plot(self.x, self.ecg)
                ecg_line.setData(self.x, self.ecg)

            def open_file():
                
                filename = QFileDialog.getOpenFileName(self, 'Open file', './data/')
                self.noext_fname = os.path.splitext(filename[0])[0]
                print(self.noext_fname)
                self.graphWidget.clear()

                self.x = np.arange(0,15000)  
                ecg_line = self.graphWidget.plot(self.x, self.ecg)

                #open .ecg file
                if filename[0].endswith('.ecg'):
                    self.holt = Holter(filename[0])
                    self.fs = self.holt.sr
                    self.holt.load_data()
                
                    self.ecg = self.holt.lead[0].data[0:15000]

                #open .dat file
                elif filename[0].endswith('.dat'):
                    signal, field = wfdb.rdsamp(self.noext_fname, channels=[0], sampto=15000)
                    self.ecg = [element for list in signal for element in list] 
                    self.fs = field['fs']
                                
                    
                ecg_line.setData(self.x, self.ecg)
                self.graphWidget.setXRange(0, 300)
                self.graphWidget.setYRange(min(self.ecg)*1.1, max(self.ecg)*1.1)

            def save():
                print('clicked save')

            def help():
                print('clicked help')

            def quit():
                QApplication.quit()

            self.menuBar = self.menuBar()

            self.openMenu = self.menuBar.addMenu('Open')

            open_file_action = QAction('Open File', self)
            open_file_action.triggered.connect(lambda:open_file())
            self.openMenu.addAction(open_file_action)

            open_sim_action = QAction('Open Sim', self)
            open_sim_action.triggered.connect(lambda:open_sim())
            self.openMenu.addAction(open_sim_action)

            save_action = QAction('Save', self)
            save_action.triggered.connect(lambda:save())
            self.menuBar.addAction(save_action)

            help_action = QAction('Help', self)
            help_action.triggered.connect(lambda:help())
            self.menuBar.addAction(help_action)

            quit_action = QAction('&Quit', self)
            quit_action.triggered.connect(lambda:quit())
            self.menuBar.addAction(quit_action)

        def ecg_clean_f(met):
            if len(self.x) == 0:
                print('open file')
            elif met != -1:
                self.ecg_cleaned = nk.ecg_clean(self.ecg, 1000, self.ecg_clean_methods[met])

        def ecg_peaks_f(met):
            if len(self.x) == 0:
                print('open file')
            elif met != -1:
                s, info = nk.ecg_peaks(self.ecg, method = self.ecg_peaks_methods[met], correct_artifacts = True)
                self.peaks = info["ECG_R_Peaks"]

        def confirm():
            self.graphWidget.clear()

            ecg_line = self.graphWidget.plot(self.x, self.ecg)
            ecg_line.setData(self.x, self.ecg_cleaned)

            for peak in self.peaks:
                    self.graphWidget.addItem(pg.InfiniteLine(peak, pen = pg.mkPen(color=(255, 0, 0))))

        def calc():
            intervals = []
            for i in range(0, len(self.peaks)-1):
                intervals.append(self.peaks[i+1] - self.peaks[i])
            
            if  self.noext_fname == None:
                print('open file')
            else:
                with open(self.noext_fname + '.rr', 'w+') as file:
                    for item in intervals:
                        # write each item on a new line
                        file.write("%s\n" % (item/self.fs))
                    print('Done')

        def create_ecg_clean_combo():
            ecg_clean_label = QLabel("Clean method")
            self.comboLayout.addWidget(ecg_clean_label)

            ecg_clean =  QComboBox()
           
            for method in self.ecg_clean_methods:
                ecg_clean.addItem(method) 

            ecg_clean.activated[int].connect(ecg_clean_f)
            self.comboLayout.addWidget(ecg_clean)

            ecg_clean.setCurrentIndex(-1)

        def create_ecg_peaks_combo():
            ecg_peak_label = QLabel("Find peak method")
            self.comboLayout.addWidget(ecg_peak_label)

            ecg_peaks = QComboBox()
            for method in self.ecg_peaks_methods:
                ecg_peaks.addItem(method)

            ecg_peaks.activated[int].connect(ecg_peaks_f)
            self.comboLayout.addWidget(ecg_peaks)

            ecg_peaks.setCurrentIndex(-1)

        def create_confirm_button():
            confirm_button = QPushButton('Confirm')
            confirm_button.clicked.connect(lambda:confirm())
            self.comboLayout.addWidget(confirm_button)

        def create_interval_button():
            interval_button = QPushButton('Calc intervals RR')
            interval_button.clicked.connect(lambda:calc())
            self.comboLayout.addWidget(interval_button)

        create_menuBar()

        self.centralWidget = QWidget()

        self.setCentralWidget(self.centralWidget)

        self.gridLayout = QGridLayout()
        self.centralWidget.setLayout(self.gridLayout)

        self.graphWidget = pg.PlotWidget(background=QColor(69, 83, 100, 255)) #setting graph

        self.graphWidget.setLabel('left', 'Voltage [mV]', color ='white', size = "20pt")
        self.graphWidget.setLabel('bottom', 'samples', color ='white', size = "20pt")

        self.graphWidget.setTitle("Wykres EKG", color="w", size="20pt")

        ecg_line = self.graphWidget.plot(self.x, self.ecg)

        self.gridLayout.addWidget(self.graphWidget, 0, 0) 

        self.comboLayout = QVBoxLayout()

        self.comboLayout.addStretch()

        self.gridLayout.addLayout(self.comboLayout, 0, 1)
        
        create_ecg_clean_combo()

        self.comboLayout.addStretch()

        create_ecg_peaks_combo()

        self.comboLayout.addStretch()

        create_confirm_button()

        self.comboLayout.addStretch()

        create_interval_button()

        self.comboLayout.addStretch()