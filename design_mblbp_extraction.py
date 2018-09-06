import sys

from PyQt5.QtCore import QThread
from qtpy import QtWidgets

import mblbp as mb
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QLabel, \
    QTextEdit, QLineEdit, QGridLayout
from PyQt5.QtGui import QFont
from functools import partial


class mblbpthread(QThread):
    def __init__(self, height, width, bins, img_path, output):
        QThread.__init__(self)
        self.height = int(height)
        self.width = int(width)
        self.bin = int(bins)
        self.img_path = img_path
        self.output = output

    def __del__(self):
        self.wait()

    def run(self):
        mb.findAllAttributeMBLBPFeature(imgpath=self.img_path, bin=self.bin, height=self.height,
                                     width=self.width, outputname=self.output)


class myMblbplayout(QtWidgets.QWidget):
    def process(self):
        self.bin = self.bin_textbox.text()
        self.height = self.height_textbox.text()
        self.width = self.width_textbox.text()
        self.img_path = self.dir_label.text()
        print(self.bin)
        print(self.height)
        print(self.width)
        print(self.img_path)
        self.myThread = mblbpthread(self.height, self.width, self.bin, self.img_path, self.output_string)
        self.myThread.started.connect(self.start)
        self.myThread.start()
        self.myThread.finished.connect(self.please_done)

    def selectfolderpartial(self, btn):
        pathfolder = QFileDialog.getExistingDirectory(
            self, 'Select a directory')
        if (btn == self.select_dir_button):
            pathfolder = pathfolder+"/"
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
        self.title = QLabel('Multi Block Local Binary Pattern')
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
        # label Height Rule
        self.height_label = QLabel(
            'Tinggi deskriptor MB-LBP')
        ############################################
        # Input height operator mblbp
        self.height_textbox = QLineEdit(self)
        self.height_textbox.setMaximumWidth(100)
        self.height_textbox.setFixedWidth(100)
        reg_ex = QtCore.QRegExp("\d+")
        self.height_textbox.setText("0")
        input_validator = QtGui.QRegExpValidator(reg_ex, self.height_textbox)
        self.height_textbox.setValidator(input_validator)
        ############################################
        # label Width Rule
        self.width_label = QLabel('Lebar deksriptor MB-LBP')
        ############################################
        # Input width operator mblbp
        self.width_textbox = QLineEdit(self)
        self.width_textbox.setMaximumWidth(100)
        self.width_textbox.setFixedWidth(100)
        reg_ex = QtCore.QRegExp("\d+")
        self.width_textbox.setText("0")
        input_validator = QtGui.QRegExpValidator(reg_ex, self.width_textbox)
        self.width_textbox.setValidator(input_validator)
        ############################################
        # label Bin Rule
        self.bin_label = QLabel('Kuantisasi')
        ############################################
        # Input bin operator mblbp
        self.bin_textbox = QLineEdit(self)
        self.bin_textbox.setMaximumWidth(100)
        self.bin_textbox.setFixedWidth(100)
        reg_ex = QtCore.QRegExp("\d+")
        self.bin_textbox.setText("0")
        input_validator = QtGui.QRegExpValidator(reg_ex, self.bin_textbox)
        self.bin_textbox.setValidator(input_validator)
        ############################################
        self.secondLayout.addWidget(self.height_textbox, 1, 0)
        self.secondLayout.addWidget(self.height_label, 1, 1)
        self.secondLayout.addWidget(self.width_textbox, 2, 0)
        self.secondLayout.addWidget(self.width_label, 2, 1)
        self.secondLayout.addWidget(self.bin_textbox, 3, 0)
        self.secondLayout.addWidget(self.bin_label, 3, 1)
        ############################################
        # button Select Directory Image
        self.select_dir_button = QPushButton('Select Folder')
        self.select_dir_button.setMinimumSize(QtCore.QSize(100, 30))
        self.select_dir_button.setMaximumSize(QtCore.QSize(100, 30))
        self.select_dir_button.setObjectName("pushButton")
        self.select_dir_button.clicked.connect(partial(self.selectfolderpartial, self.select_dir_button))
        ############################################
        # label dir
        self.dir_label = QLabel('Folder yang berisi set data citra')
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
        self.height = ''
        self.width = ''
        self.bin = ''
        self.img_path = ''
        self.output_string = ''

    def setEnabledWidget(self, stat):
        self.height_textbox.setEnabled(stat)
        self.width_textbox.setEnabled(stat)
        self.bin_textbox.setEnabled(stat)
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
        super(myMblbplayout, self).__init__(parent)
        self.fontInit()
        self.initMainLayout()
        self.initLayout()
        self.setMinimumSize(self.mainlayout.sizeHint())