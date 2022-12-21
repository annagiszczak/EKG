import sys
import numpy as np

import neurokit2 as nk
import pyqtgraph as pg

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from ishneholterlib import Holter
# import wfdb
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

        self.ecg_peaks_methods = ["neurokit", "pantompkins1985", "hamilton2002", "elgendi2010", "engzeemod2012", "gamboa2008"]
        self.ecg_clean_methods = ["neurokit", "biosppy", "pantompkins1985", "hamilton2002", "elgendi2010", "engzeemod2012"]        
        
        def create_menuBar():
            def open_sim():
                self.x = np.arange(0,15000)
                self.ecg = nk.ecg_simulate(duration = 15, sampling_rate = 1000, heart_rate = 80)
                
                self.graphWidget.clear()
                
                ecg_line = self.graphWidget.plot(self.x, self.ecg)
                ecg_line.setData(self.x, self.ecg)

            def open_file():
                
                filename = QFileDialog.getOpenFileName(self, 'Open file', './data/')
                #open .ecg file
                # if filename[0].endswith('.ecg'):
                #     self.yholt = Holter(filename[0])
                #     self.yholt.load_data()
                #     self.x = np.arange(0,15000)
                #     self.ecg = self.yholt.lead[0].data[0:15000]
                #     ecg_line.setData(self.x, self.ecg)
                #open .dat file
                # elif filename[0].endswith('.dat'):
                    # load a record using the 'rdrecord' function
                    # record = wfdb.rdrecord(filename)
                    # print(filename)
                    # plot the record to screen
                    # wfdb.plot_wfdb(record=record, title='Example signals')
                    #load a record using the 'rdrecord' function
                    # record = wfdb.rdrecord(filename[0][:-4])
                    #load the annotation file
                    
                    # record = wfdb.rdrecord(filename[0][:-4], channels=[1], sampfrom=0, sampto=1000)
                    # ecg_list = os.listdir(str(filename[0][:-4]))
                    # sample_list = [ecg[:-4] for ecg in ecg_list]
                    # clean_sample_list = [ecg for ecg in sample_list if
                    #                     ecg not in ['102-0', 'ANNOTA', 'REC', 'SHA256SUMS', 'mitd', 'x_m']]
                    # all_samples = np.zeros((len(clean_sample_list), 650000, 2))
                    # for idx, ecg in enumerate(clean_sample_list):
                    #     record = wfdb.rdrecord(filename + ecg)
                    #     all_samples[idx] = record.p_signal

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

        create_confirm_button()

        self.comboLayout.addStretch()
        self.comboLayout.addStretch()