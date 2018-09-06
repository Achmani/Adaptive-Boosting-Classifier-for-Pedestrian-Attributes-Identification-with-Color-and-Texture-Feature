import sys

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import math
import colorfeature as cf
from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QLabel, \
    QTextEdit, QLineEdit, QGridLayout, QComboBox, QMessageBox
from PyQt5.QtGui import QFont
from functools import partial
import time
import adaboost as ada


class ResultObj(QtCore.QObject):
    def __init__(self, val):
        self.val = val


class guiadaboost_thread(QThread):
    mySignal = pyqtSignal(str)

    def __init__(self, cf, mf, weak_class, cv, attr, output):
        QThread.__init__(self)
        self.cf_string = cf
        self.mf_string = mf
        self.weak_class_int = int(weak_class)
        self.cv_int = int(cv)
        self.attr_int = int(attr)
        self.output_string = output

    def run(self):
        # result = ada.gui_train(self.cf_string, self.mf_string, self.cv_int, self.weak_class_int, self.attr_int)
        X_array = []
        cf = self.cf_string
        mf = self.mf_string
        cv = self.cv_int
        wc = self.weak_class_int
        output_string = self.output_string
        i_label = self.attr_int
        if (cf != ""):
            X_array = np.load(cf)
            if (mf != ""):
                mf = np.load(mf)
                X_array = np.concatenate((X_array, mf), axis=1)
        else:
            X_array = np.load(mf)
        train_array = np.load("crossvalidation/crossvalidation" + str(cv) + "/train_array.npy")
        test_array = np.load("crossvalidation/crossvalidation" + str(cv) + "/test_array.npy")
        label_subset = np.load("labelsubset/AllLabelSubset.npy")
        temp_result = np.zeros([cv, 5])
        for k in range(0, cv):
            X_train = X_array[train_array[k, :]]
            X_test = X_array[test_array[k, :]]
            y_train = label_subset[train_array[k, :], i_label]
            y_test = label_subset[test_array[k, :], i_label]
            # This point start calculating a computation time
            clf = ada.training(X=X_train, y=y_train, estimator=wc, output=output_string)
            temp = ada.eval_score(clf, X_test, y_test)
            temp_result[k, :] = temp
        result = np.mean(temp_result, axis=0)
        # result_string = "Time to training is " + str(end - start) + " milisecond \n"
        # FP, FN, TN, TP, Acc
        FP = math.ceil(result[0])
        FN = math.ceil(result[1])
        TN = math.ceil(result[2])
        TP = math.ceil(result[3])
        ACC = result[4]
        result_string = "From " + str(y_test.shape[0]) + " Data Test the result is : \n"
        result_string = result_string + "False Positive = " + str(FP) + "\n"
        result_string = result_string + "False Negative = " + str(FN) + "\n"
        result_string = result_string + "True Negative = " + str(TN) + "\n"
        result_string = result_string + "True Positive = " + str(TP) + "\n"
        precision = 0
        try:
            precision = TP / (TP + FP)
        except ZeroDivisionError:
            precision = 0
        recall = 0
        try:
            recall = TP / (TP + FN)
        except ZeroDivisionError:
            recall = 0
        F1score = 2 * ((precision * recall) * (precision + recall))
        result_string = result_string + "Precision = " + str(precision) + "\n"
        result_string = result_string + "Recall = " + str(recall) + "\n"
        result_string = result_string + "F1 Score = " + str(F1score) + "\n"
        result_string = result_string + "Accuracy = " + str(ACC) + "\n"
        print(result_string)
        self.mySignal.emit(result_string)


class myAdaboostTraining(QtWidgets.QWidget):
    def process(self):
        self.cf_string = self.cf_label.text()
        self.mf_string = self.mf_label.text()
        self.weak_class_string = self.weak_class_textbox.text()
        self.myThread = guiadaboost_thread(self.cf_string, self.mf_string, self.weak_class_string,
                                           self.cv_string,
                                           self.attr_label_string, self.save_string)
        self.myThread.started.connect(self.start)
        self.myThread.start()
        self.myThread.mySignal.connect(self.hello)
        self.myThread.finished.connect(self.please_done)

    def hello(self, result):
        QMessageBox.information(self, "Pelatihan Berhasil", result)
        print(result)

    def selectfilepartial(self, btn):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Open file *.npy", "",
                                                  "Numpy Files (*.npy)", options=options)
        if (btn == self.select_mf_button):
            self.mf_label.setText(fileName)
            self.mf_string = fileName
            self.mf_label.setFixedWidth(500)
        if (btn == self.select_cf_button):
            self.cf_label.setText(fileName)
            self.cf_string = fileName
            self.cf_label.setFixedWidth(500)

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "Save as *.pkl", "",
                                                  "Pickle Files (*.pkl)", options=options)
        fileName = fileName + ".pkl"
        self.save_label.setText(fileName)
        self.save_string = fileName

    def fontInit(self):
        self.fonth1 = QFont()
        self.fonth1.setPointSize(12)
        self.fonth1.setBold(True)

    def initMainLayout(self):
        # Title
        self.title = QLabel('Adaboost Training')
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
        # label weak classifier Rule
        self.weak_class_label = QLabel('Jumlah Weak Classifier')
        ############################################
        # Input weak classifier mblbp
        self.weak_class_textbox = QLineEdit(self)
        self.weak_class_textbox.setMaximumWidth(100)
        self.weak_class_textbox.setFixedWidth(100)
        reg_ex = QtCore.QRegExp("\d+")
        self.weak_class_textbox.setText("0")
        input_validator = QtGui.QRegExpValidator(reg_ex, self.weak_class_textbox)
        self.weak_class_textbox.setValidator(input_validator)
        ############################################
        # label Cross Validation Rule
        self.cv_label = QLabel('Cross Validation')
        ############################################
        # Input saturation operator mblbp
        self.cv = QComboBox()
        # self.cv.addItems(["0", "2", "5", "10", "15"])
        # self.cv.addItem("0", 0)
        self.cv.addItem("2", 2)
        self.cv.addItem("5", 5)
        self.cv.addItem("10", 10)
        self.cv.addItem("15", 15)
        self.cv.currentIndexChanged.connect(self.selectionchangecv)
        self.cv.setMaximumWidth(100)
        ############################################
        ############################################
        # Input Attribute
        self.attr_select = QComboBox()
        self.attr_select.addItem('Laki-laki', 77)
        self.attr_select.addItem('Celana Pendek', 88)
        self.attr_select.addItem('Rambut Panjang', 49)
        self.attr_select.addItem('Sandal', 85)
        self.attr_select.addItem('Membawa Sesuatu', 81)
        self.attr_select.addItem('Topi', 42)
        self.attr_select.addItem('Tas Punggung', 28)
        self.attr_select.currentIndexChanged.connect(self.selectionchangeattr)
        self.attr_select.setMaximumWidth(100)
        ############################################
        # label Cross Validation Rule
        self.attr_label = QLabel('Label Atribut')
        ############################################
        self.secondLayout.addWidget(self.weak_class_textbox, 1, 0)
        self.secondLayout.addWidget(self.weak_class_label, 1, 1)
        self.secondLayout.addWidget(self.cv, 2, 0)
        self.secondLayout.addWidget(self.cv_label, 2, 1)
        self.secondLayout.addWidget(self.attr_select, 3, 0)
        self.secondLayout.addWidget(self.attr_label, 3, 1)
        ############################################
        # button Select Color Feature
        self.select_cf_button = QPushButton('Fitur Warna')
        self.select_cf_button.setMinimumSize(QtCore.QSize(100, 30))
        self.select_cf_button.setMaximumSize(QtCore.QSize(100, 30))
        self.select_cf_button.setObjectName("pushButton")
        self.select_cf_button.clicked.connect(partial(self.selectfilepartial, self.select_cf_button))
        ############################################
        # label Select Color Feature
        self.cf_label = QLabel('')
        ############################################
        # button Select MBLBP  Feature
        self.select_mf_button = QPushButton('Fitur Tekstur')
        self.select_mf_button.setMinimumSize(QtCore.QSize(100, 30))
        self.select_mf_button.setMaximumSize(QtCore.QSize(100, 30))
        self.select_mf_button.setObjectName("pushButton")
        self.select_mf_button.clicked.connect(partial(self.selectfilepartial, self.select_mf_button))
        ############################################
        # label dir
        self.mf_label = QLabel('')
        ############################################
        # Save Process
        self.save_button = QPushButton('Output')
        self.save_button.setMinimumSize(QtCore.QSize(100, 30))
        self.save_button.setMaximumSize(QtCore.QSize(100, 30))
        self.save_button.setObjectName("pushButton")
        self.save_button.clicked.connect(self.saveFileDialog)
        ############################################
        # label Save
        self.save_label = QLabel('')
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
        self.secondLayout.addWidget(self.select_cf_button, 4, 0)
        self.secondLayout.addWidget(self.cf_label, 4, 1)
        self.secondLayout.addWidget(self.select_mf_button, 5, 0)
        self.secondLayout.addWidget(self.mf_label, 5, 1)
        self.secondLayout.addWidget(self.save_button, 6, 0)
        self.secondLayout.addWidget(self.save_label, 6, 1)
        self.secondLayout.addWidget(self.process_button, 7, 0)
        self.secondLayout.addWidget(self.process_label, 7, 1)

    def selectionchangecv(self, i):
        print("Current index", self.cv.itemText(i))
        print("Current Data", self.cv.itemData(i))
        self.cv_string = self.cv.itemData(i)

    def selectionchangeattr(self, i):
        print("Current index", self.attr_select.itemText(i))
        print("Current Data", self.attr_select.itemData(i))
        self.attr_label_string = self.attr_select.itemData(i)
        print(self.attr_label_string)

    def initGlobalVariable(self):
        self.weak_class_string = ''
        self.cv_string = '2'
        self.cf_string = ''
        self.mf_string = ''
        self.attr_label_string = '77'
        self.save_string = ''

    def setEnabledWidget(self, stat):
        self.weak_class_textbox.setEnabled(stat)
        self.select_cf_button.setEnabled(stat)
        self.select_mf_button.setEnabled(stat)
        self.attr_select.setEnabled(stat)
        self.cv.setEnabled(stat)
        self.process_button.setEnabled(stat)

    def start(self):
        self.setEnabledWidget(False)
        self.process_label.setText("Silahkan Tunggu")

    def please_done(self):
        self.setEnabledWidget(True)
        self.process_label.setText("Berhasil")
        self.myThread.terminate()

    def __init__(self, parent=None):
        super(myAdaboostTraining, self).__init__(parent)
        self.initGlobalVariable()
        self.fontInit()
        self.initMainLayout()
        self.initLayout()
        self.setMinimumSize(self.mainlayout.sizeHint())
