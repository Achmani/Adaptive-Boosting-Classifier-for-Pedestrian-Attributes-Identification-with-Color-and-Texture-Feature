import sys
import makeRules as mk
from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QFileDialog, QLabel, \
    QTextEdit, QLineEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QThread, pyqtSignal
from functools import partial

class makeLabelThread(QThread):

    def __init__(self,rule_string,label_string,dir_string,extention_string,delimiter_string,output_string):
        QThread.__init__(self)
        self.rule_string = rule_string
        self.label_string = label_string
        self.dir_string = dir_string
        self.extention_string = extention_string
        self.delimiter_string = delimiter_string
        self.output_string = output_string

    def __del__(self):
        self.wait()

    def run(self):
        mk.makeLabelMatriks(self.rule_string,self.label_string,self.dir_string,self.extention_string,self.delimiter_string,self.output_string)

class Window(QDialog):
    
    def setEnabledWidget(self,stat):
        self.process_button.setEnabled(stat)
        self.rule_button.setEnabled(stat)
        self.label_data_button.setEnabled(stat)
        self.select_dir_button.setEnabled(stat)
        self.delimiter_textbox.setEnabled(stat)
        self.extention_textbox.setEnabled(stat)
        self.output_button.setEnabled(stat)        
    
    def start(self):
        self.setEnabledWidget(False)
        self.process_label.setText("Silahkan Tunggu")
    
    def please_done(self):
        self.setEnabledWidget(True)
        self.process_label.setText("Berhasil")
        self.myThread.terminate()
        
    def process(self):
        self.delimiter_string = self.delimiter_textbox.text()
        self.extention_string = self.extention_textbox.text()
        self.myThread = makeLabelThread(self.rule_string,self.label_string,self.dir_string,self.extention_string,self.delimiter_string,self.output_string)
        #self.connect(self.myThread, SIGNAL("started()"), self.start)
        #self.connect(self.myThread, SIGNAL("finished()"), self.done)
        self.myThread.started.connect(self.start)
        self.myThread.start()
        self.myThread.finished.connect(self.please_done)


    def openfilepartial(self, btn):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(None, "Open *.csv", "",
                                                  "Image Files (*.csv)", options=options)
        if btn == self.rule_button:
            self.rule_file.setText(fileName)
            self.rule_string = fileName
        elif btn == self.label_data_button:
            self.label_data_file.setText(fileName)
            self.label_string = fileName

    def selectfolderpartial(self, btn):
        pathfolder = QFileDialog.getExistingDirectory(
            self, 'Select a directory')
        if (btn == self.select_dir_button):
            self.select_file.setText(pathfolder)
            self.dir_string = pathfolder

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "Save as *.csv and *.npy", "",
                                                  "All Files (*);;Text Files (*.txt)", options=options)
        self.output_file.setText(fileName)
        self.output_string = fileName

    def fontInit(self):
        self.fonth1 = QFont()
        self.fonth1.setPointSize(12)
        self.fonth1.setBold(True)

    def initMainLayout(self):
        # Title
        self.title = QLabel('Converting Attribute Labels To Attribute Matrices')
        self.title.setObjectName("label_file")
        self.title.setAlignment(QtCore.Qt.AlignHCenter)
        self.title.setFont(self.fonth1)
        ################################################
        self.mainlayout = QVBoxLayout()
        self.setLayout(self.mainlayout)
        self.gridLayout = QGridLayout()
        self.mainlayout.addWidget(self.title)
        self.mainlayout.addLayout(self.gridLayout)

    def initLeftLayout(self):
        # button Search Rule
        self.rule_button = QPushButton('Search Rule')
        self.rule_button.setMinimumSize(QtCore.QSize(100, 30))
        self.rule_button.setMaximumSize(QtCore.QSize(100, 30))
        self.rule_button.setObjectName("pushButton")
        self.rule_button.clicked.connect(partial(self.openfilepartial, self.rule_button))
        ############################################
        # button Search label
        self.label_data_button = QPushButton('Search Label')
        self.label_data_button.setMinimumSize(QtCore.QSize(100, 30))
        self.label_data_button.setMaximumSize(QtCore.QSize(100, 30))
        self.label_data_button.setObjectName("pushButton")
        self.label_data_button.clicked.connect(partial(self.openfilepartial, self.label_data_button))
        ############################################
        # button Select Directory Image
        self.select_dir_button = QPushButton('Select Folder')
        self.select_dir_button.setMinimumSize(QtCore.QSize(100, 30))
        self.select_dir_button.setMaximumSize(QtCore.QSize(100, 30))
        self.select_dir_button.setObjectName("pushButton")
        self.select_dir_button.clicked.connect(partial(self.selectfolderpartial, self.select_dir_button))
        ############################################
        # Input delimiter
        self.delimiter_textbox = QLineEdit(self)
        self.delimiter_textbox.setMaximumWidth(100)
        self.delimiter_textbox.setFixedWidth(100)
        ############################################
        # Input ekstensi gambar
        self.extention_textbox = QLineEdit(self)
        self.extention_textbox.setMaximumWidth(100)
        self.extention_textbox.setFixedWidth(100)
        ############################################
        # button Output
        self.output_button = QPushButton('Output')
        self.output_button.setMinimumSize(QtCore.QSize(100, 30))
        self.output_button.setMaximumSize(QtCore.QSize(100, 30))
        self.output_button.setObjectName("pushButton")
        self.output_button.clicked.connect(self.saveFileDialog)
        ############################################
        # button Process
        self.process_button = QPushButton('Process')
        self.process_button.setMinimumSize(QtCore.QSize(100, 30))
        self.process_button.setMaximumSize(QtCore.QSize(100, 30))
        self.process_button.setObjectName("pushButton")
        self.process_button.clicked.connect(self.process)
        ############################################

        self.gridLayout.addWidget(self.rule_button, 1, 0)
        self.gridLayout.addWidget(self.label_data_button, 2, 0)
        self.gridLayout.addWidget(self.select_dir_button, 3, 0)
        self.gridLayout.addWidget(self.delimiter_textbox, 4, 0)
        self.gridLayout.addWidget(self.extention_textbox, 5, 0)
        self.gridLayout.addWidget(self.output_button, 6, 0)
        self.gridLayout.addWidget(self.process_button, 7, 0)

    def initRightLayout(self):
        # label Search Rule
        ############################################
        # label Search Rule
        plusHeight = 500
        self.rule_file = QLabel(
            'File csv yang berisi list atribut dataset PETA yang akan diubah ke dalam bentuk matriks')
        self.rule_file.setObjectName("label_file")
        self.rule_file.setGeometry(QtCore.QRect(self.rule_file.x(), self.rule_file.y()+plusHeight, self.rule_file.width(), self.rule_file.height()))
        ############################################
        # label Search Label
        self.label_data_file = QLabel(
            'File label yang ada di setiap sub atribut peta yang telah diubah ke dalam bentuk matriks')
        self.label_data_file.setObjectName("label_file")
        self.label_data_file.setGeometry(QtCore.QRect(self.label_data_file.x(), self.label_data_file.y()+plusHeight, self.label_data_file.width(), self.label_data_file.width()))
        ############################################
        # label Search Rule
        self.title = QLabel('converting attribute labels to attribute matrices')
        self.title.setObjectName("label_file")
        self.title.setGeometry(QtCore.QRect(self.title.x(), self.title.y(), self.title.width(), self.title.height()+plusHeight))
        ############################################
        # label Select Folder
        self.select_file = QLabel('Pilih sub folder dari set data PETA')
        self.select_file.setObjectName("label_file")
        ############################################
        # label delimiter
        self.delimiter_file = QLabel('Inputkan pembatas file')
        self.delimiter_file.setObjectName("label_file")
        ############################################
        # label Ekstensi
        self.extention_file = QLabel('Inputkan ekstensi gambar')
        self.extention_file.setObjectName("label_file")
        ############################################
        # label Output
        self.output_file = QLabel('')
        self.output_file.setObjectName("label_file")
        ############################################
        # label Output
        self.process_label = QLabel('')
        self.process_label.setObjectName("label_file")
        ############################################

        self.gridLayout.addWidget(self.rule_file, 1, 1)
        self.gridLayout.addWidget(self.label_data_file, 2, 1)
        self.gridLayout.addWidget(self.select_file, 3, 1)
        self.gridLayout.addWidget(self.delimiter_file, 4, 1)
        self.gridLayout.addWidget(self.extention_file, 5, 1)
        self.gridLayout.addWidget(self.output_file, 6, 1)
        self.gridLayout.addWidget(self.process_label, 7, 1)

    def initGlobalVariable(self):
        self.rule_string = ''
        self.label_string = ''
        self.dir_string = ''
        self.delimiter_string = ''
        self.extention_string = ''
        self.output_string = ''

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.fontInit()
        self.initMainLayout()
        self.initLeftLayout()
        self.initRightLayout()
        self.setFixedSize(self.mainlayout.sizeHint())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Window()
    main.show()
    sys.exit(app.exec_())
