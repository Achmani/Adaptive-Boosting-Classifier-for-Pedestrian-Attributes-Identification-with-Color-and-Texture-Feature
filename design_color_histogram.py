import sys

from PyQt5.QtCore import QThread
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import colorfeature as cf
from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QLabel, \
    QTextEdit, QLineEdit, QGridLayout
from PyQt5.QtGui import QFont
from functools import partial

class colorhist_thread(QThread):
    def __init__(self, hue, saturation, values, img_path, output):
        QThread.__init__(self)
        self.hue = int(hue)
        self.saturation = int(saturation)
        self.value = int(values)
        self.img_path = img_path
        self.output = output

    def __del__(self):
        self.wait()

    def run(self):
        cf.findAllPETAAtributeColorFeature(imgpath=self.img_path,outputname=self.output,h=self.hue, s=self.saturation,
                                     v=self.value)

class myColorHistogram(QtWidgets.QWidget):
    def process(self):
        self.value = self.value_textbox.text()
        self.hue = self.hue_textbox.text()
        self.saturation = self.saturation_textbox.text()
        self.img_path = self.dir_label.text()
        print(self.value)
        print(self.hue)
        print(self.saturation)
        self.myThread = colorhist_thread(self.hue, self.saturation, self.value, self.img_path, self.output_string)
        self.myThread.started.connect(self.start)
        self.myThread.start()
        self.myThread.finished.connect(self.please_done)

    def selectfolderpartial(self, btn):
        pathfolder = QFileDialog.getExistingDirectory(
            self, 'Select a directory')
        if (btn == self.select_dir_button):
            pathfolder = pathfolder + "/"
            self.dir_label.setText(pathfolder)
            self.dir_string = pathfolder
            self.dir_label.setFixedWidth(500)

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "Save as *.csv and *.npy", "",
                                                  "All Files (*);;Text Files (*.txt)", options=options)
        self.output_label.setText(fileName)
        self.output_string = fileName

    def fontInit(self):
        self.fonth1 = QFont()
        self.fonth1.setPointSize(12)
        self.fonth1.setBold(True)

    def initMainLayout(self):
        # Title
        self.title = QLabel('Color Histogram')
        self.title.setObjectName("label_file")
        self.title.setAlignment(QtCore.Qt.AlignHCenter)
        self.title.setFont(self.fonth1)
        ################################################
        self.mainlayout = QVBoxLayout()
        self.mainlayout.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(self.mainlayout)
        self.secondLayout = QGridLayout()
        self.mainlayout.addWidget(self.title)
        self.mainlayout.addLayout(self.secondLayout)

    def initLayout(self):
        # label hue Rule
        self.hue_label = QLabel('Nilai kuantisasi hue')
        ############################################
        # Input hue operator mblbp
        self.hue_textbox = QLineEdit(self)
        self.hue_textbox.setMaximumWidth(100)
        self.hue_textbox.setFixedWidth(100)
        reg_ex = QtCore.QRegExp("\d+")
        self.hue_textbox.setText("0")
        input_validator = QtGui.QRegExpValidator(reg_ex, self.hue_textbox)
        self.hue_textbox.setValidator(input_validator)
        ############################################
        # label saturation Rule
        self.saturation_label = QLabel('Nilai kuantisasi saturation')
        ############################################
        # Input saturation operator mblbp
        self.saturation_textbox = QLineEdit(self)
        self.saturation_textbox.setMaximumWidth(100)
        self.saturation_textbox.setFixedWidth(100)
        reg_ex = QtCore.QRegExp("\d+")
        self.saturation_textbox.setText("0")
        input_validator = QtGui.QRegExpValidator(reg_ex, self.saturation_textbox)
        self.saturation_textbox.setValidator(input_validator)
        ############################################
        # label value Rule
        self.value_label = QLabel('Nilai kuantisasi value')
        ############################################
        # Input value operator mblbp
        self.value_textbox = QLineEdit(self)
        self.value_textbox.setMaximumWidth(100)
        self.value_textbox.setFixedWidth(100)
        reg_ex = QtCore.QRegExp("\d+")
        self.value_textbox.setText("0")
        input_validator = QtGui.QRegExpValidator(reg_ex, self.value_textbox)
        self.value_textbox.setValidator(input_validator)
        ############################################
        self.secondLayout.addWidget(self.hue_textbox, 1, 0)
        self.secondLayout.addWidget(self.hue_label, 1, 1)
        self.secondLayout.addWidget(self.saturation_textbox, 2, 0)
        self.secondLayout.addWidget(self.saturation_label, 2, 1)
        self.secondLayout.addWidget(self.value_textbox, 3, 0)
        self.secondLayout.addWidget(self.value_label, 3, 1)
        ############################################
        # button Select Directory Image
        self.select_dir_button = QPushButton('Select Folder')
        self.select_dir_button.setMinimumSize(QtCore.QSize(100, 30))
        self.select_dir_button.setMaximumSize(QtCore.QSize(100, 30))
        self.select_dir_button.setObjectName("pushButton")
        self.select_dir_button.clicked.connect(partial(self.selectfolderpartial, self.select_dir_button))
        ############################################
        # label dir
        self.dir_label = QLabel('Folder dataset PETA')
        ############################################
        # button Output
        self.output_button = QPushButton('Output')
        self.output_button.setMinimumSize(QtCore.QSize(100, 30))
        self.output_button.setMaximumSize(QtCore.QSize(100, 30))
        self.output_button.setObjectName("pushButton")
        self.output_button.clicked.connect(self.saveFileDialog)
        ############################################
        # label Output
        self.output_label = QLabel('')
        ############################################
        # button Process
        self.process_button = QPushButton('Process')
        self.process_button.setMinimumSize(QtCore.QSize(100, 30))
        self.process_button.setMaximumSize(QtCore.QSize(100, 30))
        self.process_button.setObjectName("pushButton")
        self.process_button.clicked.connect(self.process)
        ############################################
        # label Process
        self.process_label = QLabel('')
        ############################################
        self.secondLayout.addWidget(self.select_dir_button, 4, 0)
        self.secondLayout.addWidget(self.dir_label, 4, 1)
        self.secondLayout.addWidget(self.output_button, 5, 0)
        self.secondLayout.addWidget(self.output_label, 5, 1)
        self.secondLayout.addWidget(self.process_button, 6, 0)
        self.secondLayout.addWidget(self.process_label, 6, 1)

    def initGlobalVariable(self):
        self.hue = ''
        self.saturation = ''
        self.value = ''
        self.img_path = ''
        self.output_string = ''

    def setEnabledWidget(self, stat):
        self.hue_textbox.setEnabled(stat)
        self.saturation_textbox.setEnabled(stat)
        self.value_textbox.setEnabled(stat)
        self.select_dir_button.setEnabled(stat)
        self.output_button.setEnabled(stat)
        self.process_button.setEnabled(stat)

    def start(self):
        self.setEnabledWidget(False)
        self.process_label.setText("Silahkan Tunggu")

    def please_done(self):
        self.setEnabledWidget(True)
        self.process_label.setText("Berhasil")
        self.myThread.terminate()

    def __init__(self, parent=None):
        super(myColorHistogram, self).__init__(parent)
        self.fontInit()
        self.initMainLayout()
        self.initLayout()
        self.setMinimumSize(self.mainlayout.sizeHint())