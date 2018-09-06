# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mpl.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
import sys
import design_color_histogram as dc
import design_mblbp_extraction as dm
import design_adaboost_training as da
import design_identification
import design_mblbp_proof


class Ui_MainWindow(object):

    def initHeader(self):
        font = QtGui.QFont()
        font.setPointSize(12)

        hBtn = 100
        wBtn = 85
        hIcon = 55
        wIcon = 55
        # QToolButton
        self.btn_ada = QtWidgets.QToolButton()
        self.btn_ada.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.btn_ada.setText("Adaboost")
        self.btn_ada.setIcon(QtGui.QIcon('icon/icon_adaboost.png'))
        self.btn_ada.setMinimumSize(QtCore.QSize(wBtn, hBtn))
        self.btn_ada.setIconSize(QtCore.QSize(wIcon, hIcon))
        self.btn_ada.setContentsMargins(0, 0, 0, 0)
        self.btn_ada.clicked.connect(self.switchAdaboostLayout)
        self.horizontalLayout.addWidget(self.btn_ada, 0, QtCore.Qt.AlignHCenter)
        ################################################
        self.btn_color = QtWidgets.QToolButton()
        self.btn_color.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.btn_color.setText("Color Histogram")
        self.btn_color.setIcon(QtGui.QIcon('icon/icon_color_histogram.png'))
        self.btn_color.setMinimumSize(QtCore.QSize(wBtn, hBtn))
        self.btn_color.setIconSize(QtCore.QSize(wIcon, hIcon))
        self.btn_color.setContentsMargins(0, 0, 0, 0)
        self.btn_color.clicked.connect(self.switchColorHistogramLayout)
        self.horizontalLayout.addWidget(self.btn_color, 0, QtCore.Qt.AlignHCenter)
        ################################################
        self.btn_texture = QtWidgets.QToolButton()
        self.btn_texture.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.btn_texture.setText("MB-LBP")
        self.btn_texture.setIcon(QtGui.QIcon('icon/icon_mblbp.png'))
        self.btn_texture.setMinimumSize(QtCore.QSize(wBtn, hBtn))
        self.btn_texture.setIconSize(QtCore.QSize(wIcon, hIcon))
        self.btn_texture.setContentsMargins(0, 0, 0, 0)
        self.btn_texture.clicked.connect(self.switchMblbpLayout)
        self.horizontalLayout.addWidget(self.btn_texture)
        ################################################
        self.btn_texture = QtWidgets.QToolButton()
        self.btn_texture.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.btn_texture.setText("Visualisasi\nMB-LBP")
        self.btn_texture.setIcon(QtGui.QIcon('icon/icon_mblbp.png'))
        self.btn_texture.setMinimumSize(QtCore.QSize(wBtn, hBtn))
        self.btn_texture.setIconSize(QtCore.QSize(wIcon, hIcon))
        self.btn_texture.setContentsMargins(0, 0, 0, 0)
        self.btn_texture.clicked.connect(self.openDialogMblbp)
        self.horizontalLayout.addWidget(self.btn_texture)
        ################################################
        self.btn_combine = QtWidgets.QToolButton()
        self.btn_combine.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.btn_combine.setText("Identifikasi")
        self.btn_combine.setIcon(QtGui.QIcon('icon/icon_identification.png'))
        self.btn_combine.setMaximumSize(QtCore.QSize(wBtn, hBtn))
        self.btn_combine.setIconSize(QtCore.QSize(wIcon, hIcon))
        self.btn_combine.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.addWidget(self.btn_combine)
        self.btn_combine.clicked.connect(self.openDialogIdentification)
        ################################################

    def setupUi(self, MainWindow):

        MainWindow.resize(700, 450)
        MainWindow.setFixedSize(700, 450)
        MainWindow.setStyleSheet(open("style.qss", "r").read())
        MainWindow.setAutoFillBackground(True)


        self.widget = QtWidgets.QWidget(MainWindow)
        self.widget.setObjectName("widget")

        self.centralwidget = QtWidgets.QStackedWidget(self.widget)
        self.centralwidget.setObjectName("centralwidget")

        self.color_histogram_widget = dc.myColorHistogram()
        self.mblbp_widget = dm.myMblbplayout()
        self.adaboost_widget = da.myAdaboostTraining()
        self.centralwidget.addWidget(self.color_histogram_widget)
        self.centralwidget.addWidget(self.mblbp_widget)
        self.centralwidget.addWidget(self.adaboost_widget)
        self.centralwidget.setCurrentWidget(self.color_histogram_widget)

        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setAlignment(QtCore.Qt.AlignVCenter)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setAlignment(QtCore.Qt.AlignHCenter)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setSpacing(0)

        self.fonth1 = QFont()
        self.fonth1.setPointSize(14)
        self.fonth1.setBold(True)

        self.title = QLabel('Identifikasi Atribut Pejalan Kaki')
        self.title.setObjectName("label_file")
        self.title.setAlignment(QtCore.Qt.AlignHCenter)
        self.title.setFont(self.fonth1)
        self.title.setContentsMargins(0, 15, 0, 0)

        self.verticalLayout.addWidget(self.title)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.addWidget(self.centralwidget)

        self.initHeader()

        MainWindow.setCentralWidget(self.widget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Identifikasi Atribut Pejalan Kaki"))

    def switchMblbpLayout(self):
        self.centralwidget.setCurrentWidget(self.mblbp_widget)

    def switchColorHistogramLayout(self):
        self.centralwidget.setCurrentWidget(self.color_histogram_widget)

    def switchAdaboostLayout(self):
        self.centralwidget.setCurrentWidget(self.adaboost_widget)

    def openDialogIdentification(self):
        #Dialog = identification.IdentificationDialog(self)
        self.identification_widget = design_identification.IdentificationDialog()
        self.identification_widget.show()

    def openDialogMblbp(self):
        self.mblbp_proof_widget = design_mblbp_proof.DesignMblbpProof()
        self.mblbp_proof_widget.show()


app = QApplication(sys.argv)
window = QMainWindow()

ui = Ui_MainWindow()
ui.setupUi(window)

window.show()
sys.exit(app.exec_())