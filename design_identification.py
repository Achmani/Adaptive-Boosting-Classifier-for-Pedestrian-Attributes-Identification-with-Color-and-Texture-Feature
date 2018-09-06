import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QLabel, QTextEdit
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.gridspec import GridSpec
import matplotlib.pyplot as plt
#import MBLBPBimbingan as mb
import mblbp as mb
import colorfeature as cf
import numpy as np
from skimage.io import imread
from skimage.color import rgb2gray
from sklearn.externals import joblib

maleclf = joblib.load('classifier_model/h32m16c200/male.pkl')
hairclf = joblib.load('classifier_model/h32m16c200/hairlong.pkl')
footclf = joblib.load('classifier_model/h32m16c200/footwearsandals.pkl')
trousersclf = joblib.load('classifier_model/h32m16c200/lowerbody.pkl')
nothingclf = joblib.load('classifier_model/h32m16c200/carryingNothing.pkl')
backpackclf = joblib.load('classifier_model/h32m16c200/carryingBackpack.pkl')
hatclf = joblib.load('classifier_model/h32m16c200/accessoryHat.pkl')

maleclfc = joblib.load('classifier_model/h32c100/male.pkl')
hairclfc = joblib.load('classifier_model/h32c100/hairlong.pkl')
footclfc = joblib.load('classifier_model/h32c100/footwearsandals.pkl')
trousersclfc = joblib.load('classifier_model/h32c100/lowerbody.pkl')
nothingclfc = joblib.load('classifier_model/h32c100/carryingNothing.pkl')
backpackclfc = joblib.load('classifier_model/h32c100/carryingBackpack.pkl')
hatclfc = joblib.load('classifier_model/h32c100/accessoryHat.pkl')

maleclfm = joblib.load('classifier_model/m16c100/male.pkl')
hairclfm = joblib.load('classifier_model/m16c100/hairlong.pkl')
footclfm = joblib.load('classifier_model/m16c100/footwearsandals.pkl')
trousersclfm = joblib.load('classifier_model/m16c100/lowerbody.pkl')
nothingclfm = joblib.load('classifier_model/m16c100/carryingNothing.pkl')
backpackclfm = joblib.load('classifier_model/m16c100/carryingBackpack.pkl')
hatclfm = joblib.load('classifier_model/m16c100/accessoryHat.pkl')


class IdentificationDialog(QDialog):
    def openfile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()", "",
                                                  "Image Files (*.png *.jpg *.jpeg *.gif *.bmp)", options=options)
        if fileName:
            print(fileName)
            self.label_file.setText(fileName)

    def __init__(self, parent=None):
        super(IdentificationDialog, self).__init__(parent)
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
        self.mainHlayout = QHBoxLayout()
        self.vlayout = QVBoxLayout()
        self.hLayout.addWidget(self.pushButton)
        self.hLayout.addWidget(self.label_file)
        # self.vlayout.addWidget(self.toolbar)
        self.vlayout.addWidget(self.canvas)
        # self.vlayout.addWidget(self.button)
        self.mainHlayout.addLayout(self.vlayout)
        mainlayout.addLayout(self.hLayout)
        mainlayout.addWidget(self.toolbar)
        mainlayout.addLayout(self.mainHlayout)
        mainlayout.addWidget(self.button)
        self.setLayout(mainlayout)

    def identification(self):
        print("Masuk")
        filename = self.label_file.text()
        img = imread(filename)
        gray_img = rgb2gray(img) * 255
        mblbpfeature = mb.imgMblbpFeature(gray_img, 16, 3, 3)
        colorfeature = cf.colorfeatureextractpythonic(img=img, hbin=32)
        colorfeaturetemp = np.asarray(colorfeature)
        X = np.reshape(np.concatenate((mblbpfeature, colorfeaturetemp)), (1, -1))
        result = maleclf.predict(X)
        # print(result)
        if (result == 1):
            gender = "Laki-laki"
        else:
            gender = "Perempuan"
        result = hairclf.predict(X)
        print(result)
        if (result == 1):
            hair = "Rambut Panjang"
        else:
            hair = "Rambut Pendek"
        result = footclf.predict(X)
        print(result)
        if (result == 1):
            foot = "Sandal"
        else:
            foot = "Sepatu"
        result = trousersclf.predict(X)
        print(result)
        if (result == 1):
            lowerbody = "Celana Pendek"
        else:
            lowerbody = "Celana Panjang"
        result = nothingclf.predict(X)
        print(result)
        if (result == 1):
            notcarrying = "Tidak Membawa Barang"
        else:
            notcarrying = "Membawa Barang"
        result = backpackclf.predict(X)
        print(result)
        if (result == 1):
            backpack = "Membawa Ransel"
        else:
            backpack = "Tidak Membawa Ransel"
        result = hatclf.predict(X)
        print(result)
        if (result == 1):
            hat = "Memakai Topi"
        else:
            hat = "Tidak Memakai Topi"
        ###PLOT
        # instead of ax.hold(False)
        self.figure.clear()
        ax = self.figure.add_subplot(232)
        ax.axis('off')
        ax.imshow(img)
        ax = self.figure.add_subplot(234)
        ax.axis('off')
        left, width = 0, .5
        bottom, height = .25, .5
        right = left + width
        top = bottom + height
        ax.text(right, .95, "Warna dan Tekstur",
                horizontalalignment='center',
                verticalalignment='top',
                color='blue',
                transform=ax.transAxes)
        ax.text(right, .85, gender,
                horizontalalignment='center',
                verticalalignment='top',
                transform=ax.transAxes)
        ax.text(right, .75, hair,
                horizontalalignment='center',
                verticalalignment='top',
                transform=ax.transAxes)
        ax.text(right, .65, lowerbody,
                horizontalalignment='center',
                verticalalignment='top',
                transform=ax.transAxes)
        ax.text(right, .55, foot,
                horizontalalignment='center',
                verticalalignment='top',
                transform=ax.transAxes)
        ax.text(right, .45, notcarrying,
                horizontalalignment='center',
                verticalalignment='top',
                transform=ax.transAxes)
        ax.text(right, .35, backpack,
                horizontalalignment='center',
                verticalalignment='top',
                transform=ax.transAxes)
        ax.text(right, .25, hat,
                horizontalalignment='center',
                verticalalignment='top',
                transform=ax.transAxes)

        X = np.reshape(colorfeaturetemp, (1, -1))
        result = maleclfc.predict(X)
        if (result == 1):
            gender = "Laki-laki"
        else:
            gender = "Perempuan"
        result = hairclfc.predict(X)
        print(result)
        if (result == 1):
            hair = "Rambut Panjang"
        else:
            hair = "Rambut Pendek"
        result = footclfc.predict(X)
        print(result)
        if (result == 1):
            foot = "Sandal"
        else:
            foot = "Sepatu"
        result = trousersclfc.predict(X)
        print(result)
        if (result == 1):
            lowerbody = "Celana Pendek"
        else:
            lowerbody = "Celana Panjang"
        result = nothingclfc.predict(X)
        print(result)
        if (result == 1):
            notcarrying = "Tidak Membawa Barang"
        else:
            notcarrying = "Membawa Barang"
        result = backpackclfc.predict(X)
        print(result)
        if (result == 1):
            backpack = "Membawa Ransel"
        else:
            backpack = "Tidak Membawa Ransel"
        result = hatclfc.predict(X)
        print(result)
        if (result == 1):
            hat = "Memakai Topi"
        else:
            hat = "Tidak Memakai Topi"
        ###PLOT
        ax = self.figure.add_subplot(235)
        ax.axis('off')
        left, width = 0, .5
        bottom, height = .25, .5
        right = left + width
        top = bottom + height
        ax.text(right, .95, "Warna",
                horizontalalignment='center',
                verticalalignment='top',
                color='red',
                transform=ax.transAxes)
        ax.text(right, .85, gender,
                horizontalalignment='center',
                verticalalignment='top',
                transform=ax.transAxes)
        ax.text(right, .75, hair,
                horizontalalignment='center',
                verticalalignment='top',
                transform=ax.transAxes)
        ax.text(right, .65, lowerbody,
                horizontalalignment='center',
                verticalalignment='top',
                transform=ax.transAxes)
        ax.text(right, .55, foot,
                horizontalalignment='center',
                verticalalignment='top',
                transform=ax.transAxes)
        ax.text(right, .45, notcarrying,
                horizontalalignment='center',
                verticalalignment='top',
                transform=ax.transAxes)
        ax.text(right, .35, backpack,
                horizontalalignment='center',
                verticalalignment='top',
                transform=ax.transAxes)
        ax.text(right, .25, hat,
                horizontalalignment='center',
                verticalalignment='top',
                transform=ax.transAxes)

        X = np.reshape(mblbpfeature, (1, -1))
        result = maleclfm.predict(X)
        if (result == 1):
            gender = "Laki-laki"
        else:
            gender = "Perempuan"
        result = hairclfm.predict(X)
        print(result)
        if (result == 1):
            hair = "Rambut Panjang"
        else:
            hair = "Rambut Pendek"
        result = footclfm.predict(X)
        print(result)
        if (result == 1):
            foot = "Sandal"
        else:
            foot = "Sepatu"
        result = trousersclfm.predict(X)
        print(result)
        if (result == 1):
            lowerbody = "Celana Pendek"
        else:
            lowerbody = "Celana Panjang"
        result = nothingclfm.predict(X)
        print(result)
        if (result == 1):
            notcarrying = "Tidak Membawa Barang"
        else:
            notcarrying = "Membawa Barang"
        result = backpackclfm.predict(X)
        print(result)
        if (result == 1):
            backpack = "Membawa Ransel"
        else:
            backpack = "Tidak Membawa Ransel"
        result = hatclfm.predict(X)
        print(result)
        if (result == 1):
            hat = "Memakai Topi"
        else:
            hat = "Tidak Memakai Topi"
        ###PLOT
        ax = self.figure.add_subplot(236)
        ax.axis('off')
        left, width = 0, .5
        bottom, height = .25, .5
        right = left + width
        top = bottom + height
        ax.text(right, .95, "Tekstur",
                horizontalalignment='center',
                verticalalignment='top',
                color='green',
                transform=ax.transAxes)
        ax.text(right, .85, gender,
                horizontalalignment='center',
                verticalalignment='top',
                transform=ax.transAxes)
        ax.text(right, .75, hair,
                horizontalalignment='center',
                verticalalignment='top',
                transform=ax.transAxes)
        ax.text(right, .65, lowerbody,
                horizontalalignment='center',
                verticalalignment='top',
                transform=ax.transAxes)
        ax.text(right, .55, foot,
                horizontalalignment='center',
                verticalalignment='top',
                transform=ax.transAxes)
        ax.text(right, .45, notcarrying,
                horizontalalignment='center',
                verticalalignment='top',
                transform=ax.transAxes)
        ax.text(right, .35, backpack,
                horizontalalignment='center',
                verticalalignment='top',
                transform=ax.transAxes)
        ax.text(right, .25, hat,
                horizontalalignment='center',
                verticalalignment='top',
                transform=ax.transAxes)

        # create an axis
        # ax = self.figure.add_subplot(111)

        # discards the old graph
        # ax.hold(False) # deprecated, see above

        # refresh canvas
        self.canvas.draw()


"""if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = IdentificationDialog()
    main.show()
    sys.exit(app.exec_())"""
