
import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import cv2

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Calculescence(QtGui.QMainWindow):
    
    def __init__(self):
        super(Calculescence, self).__init__()
        self.resize(1600, 1500)
        self.center()
        self.setWindowTitle('CALCULESCENCE DEMO') 
        self.setWindowIcon(QtGui.QIcon('bacteria.png'))
        self.form_widget = FormWidget(self)
        _widget = QtGui.QWidget()
        _layout = QtGui.QVBoxLayout(_widget)
        _layout.addWidget(self.form_widget)
        self.setCentralWidget(_widget)
        self.initUI()
        
    def initUI(self):  

        openvidAction = QtGui.QAction(QtGui.QIcon('openvid.png'), '&Open Video', self)        
        openvidAction.setShortcut('Ctrl+O')
        openvidAction.setStatusTip('Open Video')
        openvidAction.triggered.connect(self.openvidEvent)

        openimgAction = QtGui.QAction(QtGui.QIcon('openimg.png'), '&Open Image', self)        
        openimgAction.setShortcut('Ctrl+I')
        openimgAction.setStatusTip('Open Image')
        openimgAction.triggered.connect(self.openimgEvent)

        saveAction = QtGui.QAction(QtGui.QIcon('save.png'), '&Save', self)        
        saveAction.setShortcut('Ctrl+S')
        saveAction.setStatusTip('Save Video or Image')
        saveAction.triggered.connect(self.saveEvent)

        editAction = QtGui.QAction(QtGui.QIcon('edit.png'), '&Edit', self)        
        editAction.setShortcut('Ctrl+E')
        editAction.setStatusTip('Edit Image')
        #openAction.triggered.connect(QtGui.qApp.open)

        extractAction = QtGui.QAction(QtGui.QIcon('extract.png'), '&Extract Video Frame', self)        
        extractAction.setShortcut('Ctrl+X')
        extractAction.setStatusTip('Extract Video Frame')
        #openAction.triggered.connect(QtGui.qApp.open)

        runAction = QtGui.QAction(QtGui.QIcon('run.png'), '&Execute', self)        
        runAction.setShortcut('Ctrl+R')
        runAction.setStatusTip('Execute')
        #openAction.triggered.connect(QtGui.qApp.open)

        settingsAction = QtGui.QAction(QtGui.QIcon('settings2.png'), '&Settings', self)        
        settingsAction.setShortcut('Ctrl+G')
        settingsAction.setStatusTip('Settings')
        #openAction.triggered.connect(QtGui.qApp.open)

        exitAction = QtGui.QAction(QtGui.QIcon('close2.png'), '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtGui.qApp.quit)

        self.toolbar = self.addToolBar('Open Video')
        self.toolbar.addAction(openvidAction)

        self.toolbar = self.addToolBar('Open Image')
        self.toolbar.addAction(openimgAction)

        self.toolbar = self.addToolBar('Save')
        self.toolbar.addAction(saveAction)

        self.toolbar = self.addToolBar('Edit')
        self.toolbar.addAction(editAction)

        self.toolbar = self.addToolBar('Extract Video Frame')
        self.toolbar.addAction(extractAction)

        self.toolbar = self.addToolBar('Execute')
        self.toolbar.addAction(runAction)

        self.toolbar = self.addToolBar('Settings')
        self.toolbar.addAction(settingsAction)

        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openvidAction)
        fileMenu.addAction(openimgAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(editAction)
        fileMenu.addAction(extractAction)
        fileMenu.addAction(runAction)
        fileMenu.addAction(settingsAction)
        fileMenu.addAction(exitAction)

        self.statusBar().showMessage('Ready for Input...') 
        self.show()
        
    def center(self):

        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()   
        
    def openvidEvent(self):

        name = QtGui.QFileDialog.getOpenFileName(self, 'Open Video File')
        #file = open(name, 'r')
        Video_Hist_Var(name)

    def openimgEvent(self, windows=1):

        name = QtGui.QFileDialog.getOpenFileName(self, 'Open Image File')
        #name = QtGui.QPixmap(_fromUtf8(name))
        image = cv2.imread(name, cv2.COLOR_BGR2RGB)
        self.pic.setPixMap(QPixmap.fromImage(image))
        self.pic.setAlignment(QtCore.Qt.AlignHCenter|Qt.AlignVCenter)
        #cv2.imshow('pic',image)
        
    def saveEvent(self):

        name = QtGui.QFileDialog.getSaveFileName(self, 'Save File')
        cv2.imwrite(name)
        #text = self.textEdit.toPlaintText()
        #file.write(file)
        #file.close()

class FormWidget(QtGui.QWidget):

    def __init__(self, parent=Calculescence):
        super(FormWidget, self).__init__(parent)
        self.__controls()
        self.__layout()

    def __controls(self):
        self.label = QtGui.QLabel("Name for backdrop")
        self.txted = QtGui.QLineEdit()
        self.lbled = QtGui.QLabel("Select a readNode")
        self.cmbox = QtGui.QComboBox()
        self.pic = QtGui.QLabel("something")
        #self.pic.setGeometry(QtCore.QRect(790, 30, 701, 61))

    def __layout(self):
        self.vbox = QtGui.QVBoxLayout()
        self.hbox = QtGui.QHBoxLayout()
        self.v1box = QtGui.QVBoxLayout()
        self.h2Box = QtGui.QHBoxLayout()

        self.hbox.addWidget(self.label)
        self.hbox.addWidget(self.txted)

        self.h2Box.addWidget(self.lbled)
        self.h2Box.addWidget(self.cmbox)
        self.v1box.addWidget(self.pic)

        self.vbox.addLayout(self.hbox)
        self.vbox.addLayout(self.h2Box)
        self.vbox.addLayout(self.v1box)
        self.setLayout(self.vbox)

def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Calculescence()
    # widget=FormWidget()
    # widget.setGeometry(800,800, 400,200)
    # widget.show()
    # Form = QtGui.QWidget()
    # ui = Ui_Form()
    # ui.setupUi(Form)
    # Form.show()
    app.exec_()
    #sys.exit(app.exec_())


if __name__ == '__main__':
    sys.exit(main())     



#ICON CREDIT
#<div>Icons made by <a href="http://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a> is licensed by <a href="http://creativecommons.org/licenses/by/3.0/" title="Creative Commons BY 3.0" target="_blank">CC 3.0 BY</a></div>


