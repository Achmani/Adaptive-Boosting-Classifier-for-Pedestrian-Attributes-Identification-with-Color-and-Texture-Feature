import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QLabel, \
    QTextEdit, QLineEdit, QGridLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.gridspec import GridSpec
import matplotlib.pyplot as plt
import mblbp as mb
import numpy as np
from skimage.io import imread
from skimage.color import rgb2gray


class DesignMblbpProof(QDialog):
    def openfile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()", "",
                                                  "Image Files (*.png *.jpg *.bmp)", options=options)
        if fileName:
            print(fileName)
            self.label_file.setText(fileName)

    def __init__(self, parent=None):
        super(DesignMblbpProof, self).__init__(parent)
        # self.resize(900,600)

        # a figure instance to plot on
        plt.axis('off')
        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

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

        # Just some button connected to `plot` method
        self.button = QPushButton('Identifikasi')
        self.button.clicked.connect(self.identification)
        # button Search File
        self.pushButton = QPushButton('Search File')
        self.pushButton.setMinimumSize(QtCore.QSize(100, 30))
        self.pushButton.setMaximumSize(QtCore.QSize(100, 30))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.openfile)
        ############################################
        # button Pilih File
        self.pushButton = QPushButton('Pilih File')
        self.pushButton.setMinimumSize(QtCore.QSize(100, 30))
        self.pushButton.setMaximumSize(QtCore.QSize(100, 30))
        self.pushButton.setObjectName("fileButton")
        self.pushButton.clicked.connect(self.openfile)
        ############################################
        # Label Search File
        self.label_file = QLabel('')
        self.label_file.setObjectName("label_file")
        ############################################
        # set the layout
        mainlayout = QVBoxLayout()
        self.hLayout = QHBoxLayout()
        self.gridLayout = QGridLayout()
        self.mainHlayout = QHBoxLayout()
        self.vlayout = QVBoxLayout()
        # self.hLayout.addWidget(self.pushButton)
        # self.hLayout.addWidget(self.label_file)
        self.gridLayout.addWidget(self.pushButton, 1, 0)
        self.gridLayout.addWidget(self.label_file, 1, 1)
        self.gridLayout.addWidget(self.height_textbox, 2, 0)
        self.gridLayout.addWidget(self.height_label, 2, 1)
        self.gridLayout.addWidget(self.width_textbox, 3, 0)
        self.gridLayout.addWidget(self.width_label, 3, 1)
        # self.vlayout.addWidget(self.toolbar)
        self.vlayout.addWidget(self.canvas)
        # self.vlayout.addWidget(self.button)
        self.mainHlayout.addLayout(self.vlayout)
        mainlayout.addLayout(self.gridLayout)
        mainlayout.addWidget(self.toolbar)
        mainlayout.addLayout(self.mainHlayout)
        mainlayout.addWidget(self.button)
        self.setLayout(mainlayout)

    def identification(self):
        height = int(self.height_textbox.text())
        width = int(self.width_textbox.text())
        print("Masuk")
        filename = self.label_file.text()
        img = imread(filename)
        gray_img = rgb2gray(img) * 255
        mblbpfeature = mb.genAverageMat(img, height, width)
        mblbpfeature = mb.lbpCompare(mblbpfeature)
        draw_mblbp = mb.drawAll(img, mblbpfeature, height, width)
        sortfeature = np.sort(mblbpfeature.flatten())
        print(draw_mblbp)
        ###PLOT
        # instead of ax.hold(False)
        self.figure.clear()
        ax = self.figure.add_subplot(121)
        ax.axis('off')
        ax.imshow(img)
        ax = self.figure.add_subplot(122)
        # ax.axis('off')
        ax.imshow(draw_mblbp, cmap='gray')
        # ax = self.figure.add_subplot(133)
        # ax.hist(hist)
        self.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = DesignMblbpProof()
    main.show()
    sys.exit(app.exec_())
