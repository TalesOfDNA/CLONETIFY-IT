
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
        #self.resize(1000, 1000)
        self.center()
        self.setWindowTitle('CALCULESCENCE DEMO') 
        self.setWindowIcon(QtGui.QIcon('bacteria.png'))

        self.pic = QtGui.QWidget()
        self.l1 = QtGui.QLabel()
        self.l1.setPixmap(QPixmap('bacteria.png'))
        self.l1.setAlignment(Qt.AlignCenter)

        self.titleLabel = QtGui.QLabel('CALCULESCENCE')
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Cooper Black"))
        font.setPointSize(16)
        self.titleLabel.setFont(font)
        self.titleLabel.setAlignment(Qt.AlignCenter)
        
        self.imageLabel = QtGui.QLabel('Image or Video')
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.imageLabel.setBackgroundRole(QtGui.QPalette.Base)
        self.imageLabel.setScaledContents(True)
        self.imageLabel.adjustSize()
        self.imageLabel.resize(700,500)

        self.scrollArea = QtGui.QScrollArea()
        self.scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
        #self.scrollArea.setGeometry(QtCore.QRect(30, 100, 1171, 1041))
        self.scrollArea.setWidget(self.titleLabel)
        self.scrollArea.setWidget(self.imageLabel)
        self.scrollArea.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.scrollArea)

        self.createActions()
        self.createToolbar()
        self.createMenu()

    
        
    def createActions(self):  

        self.openvidAction = QtGui.QAction(QtGui.QIcon('openvid.png'), '&Open Video', self)        
        self.openvidAction.setShortcut('Ctrl+O')
        self.openvidAction.setStatusTip('Open Video')
        self.openvidAction.triggered.connect(self.openvidEvent)

        self.openimgAction = QtGui.QAction(QtGui.QIcon('openimg.png'), '&Open Image', self)        
        self.openimgAction.setShortcut('Ctrl+I')
        self.openimgAction.setStatusTip('Open Image')
        self.openimgAction.triggered.connect(self.openimgEvent)

        self.saveAction = QtGui.QAction(QtGui.QIcon('save.png'), '&Save', self)        
        self.saveAction.setShortcut('Ctrl+S')
        self.saveAction.setStatusTip('Save Video or Image')
        self.saveAction.triggered.connect(self.saveEvent)

        self.editAction = QtGui.QAction(QtGui.QIcon('edit.png'), '&Edit', self)        
        self.editAction.setShortcut('Ctrl+E')
        self.editAction.setStatusTip('Edit Image')
        #openAction.triggered.connect(QtGui.qApp.open)

        self.extractAction = QtGui.QAction(QtGui.QIcon('extract.png'), '&Extract Video Frame', self)        
        self.extractAction.setShortcut('Ctrl+X')
        self.extractAction.setStatusTip('Extract Video Frame')
        #openAction.triggered.connect(QtGui.qApp.open)

        self.trackingAction = QtGui.QAction(QtGui.QIcon('tracking.png'), '&Track Selected Cell', self)        
        self.trackingAction.setShortcut('Ctrl+T')
        self.trackingAction.setStatusTip('Track Selected Cell')
        #openAction.triggered.connect(QtGui.qApp.open)

        self.zoomInAction = QtGui.QAction(QtGui.QIcon('zoom-in.png'), '&ZoomIn', self)        
        self.zoomInAction.setShortcut('Ctrl+Z')
        self.zoomInAction.setStatusTip('Zoom In')
        self.zoomInAction.triggered.connect(self.zoominEvent)

        self.zoomOutAction = QtGui.QAction(QtGui.QIcon('zoomout.png'), '&ZoomOut', self)        
        self.zoomOutAction.setShortcut('Ctrl+O')
        self.zoomOutAction.setStatusTip('Zoom Out')
        self.zoomOutAction.triggered.connect(self.zoomoutEvent)

        self.countAction = QtGui.QAction(QtGui.QIcon('count.png'), 'Count Cells', self)        
        self.countAction.setShortcut('Ctrl+C')
        self.countAction.setStatusTip('Count Cells')
        #self.countAction.triggered.connect(self.countEvent)

        self.selectAction = QtGui.QAction(QtGui.QIcon('select.png'), 'Select Cell to Tracked', self)        
        self.selectAction.setShortcut('Ctrl+Shift+S')
        self.selectAction.setStatusTip('Select Cell to be Tracked')
        #self.countAction.triggered.connect(self.countEvent)

        self.settingsAction = QtGui.QAction(QtGui.QIcon('settings2.png'), '&Settings', self)        
        self.settingsAction.setShortcut('Ctrl+G')
        self.settingsAction.setStatusTip('Settings')
        #openAction.triggered.connect(QtGui.qApp.open)

        self.exitAction = QtGui.QAction(QtGui.QIcon('close2.png'), '&Exit', self)        
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Exit application')
        self.exitAction.triggered.connect(QtGui.qApp.quit)

    def createToolbar(self):

        self.toolbar = self.addToolBar('Open Video')
        self.toolbar.addAction(self.openvidAction)

        self.toolbar = self.addToolBar('Open Image')
        self.toolbar.addAction(self.openimgAction)

        self.toolbar = self.addToolBar('Save')
        self.toolbar.addAction(self.saveAction)

        self.toolbar = self.addToolBar('Edit')
        self.toolbar.addAction(self.editAction)

        self.toolbar = self.addToolBar('Extract Video Frame')
        self.toolbar.addAction(self.extractAction)

        self.toolbar = self.addToolBar('Execute')
        self.toolbar.addAction(self.trackingAction)

        self.toolbar = self.addToolBar('ZoomIn')
        self.toolbar.addAction(self.zoomInAction)

        self.toolbar = self.addToolBar('ZoomOut')
        self.toolbar.addAction(self.zoomOutAction)

        self.toolbar = self.addToolBar('Count Cells')
        self.toolbar.addAction(self.countAction)

        self.toolbar = self.addToolBar('Select Cell')
        self.toolbar.addAction(self.selectAction)

        self.toolbar = self.addToolBar('Settings')
        self.toolbar.addAction(self.settingsAction)

        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(self.exitAction)

    def createMenu(self):

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(self.openvidAction)
        fileMenu.addAction(self.openimgAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.editAction)
        fileMenu.addAction(self.extractAction)
        #fileMenu.addAction(self.trackingAction)
        fileMenu.addAction(self.settingsAction)
        fileMenu.addAction(self.exitAction)

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

    def openimgEvent(self):

        file = QtGui.QFileDialog.getOpenFileName(self, 'Open Image File', QtCore.QDir.currentPath())
        if file:
            image = QtGui.QImage(file)
            if image.isNull():
                QtGui.QMessageBox.information(self, "Image Viewer",
                        "Cannot load %s." % file)
                return

            self.imageLabel.setPixmap(QtGui.QPixmap(image))
            self.scaleFactor = 1.0


    def saveEvent(self):

        name = QtGui.QFileDialog.getSaveFileName(self, 'Save File')
        cv2.imwrite(name)
        #text = self.textEdit.toPlaintText()
        #file.write(file)
        #file.close()

    def zoominEvent(self):
        #self.imageLabel.adjustSize()
        self.scaleImage(1.25)

    def zoomoutEvent(self):
        #self.imageLabel.adjustSize()
        self.scaleImage(0.8)

    def print_(self):
        dialog = QtGui.QPrintDialog(self.printer, self)
        if dialog.exec_():
            painter = QtGui.QPainter(self.printer)
            rect = painter.viewport()
            size = self.imageLabel.pixmap().size()
            size.scale(rect.size(), QtCore.Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
            painter.setWindow(self.imageLabel.pixmap().rect())
            painter.drawPixmap(0, 0, self.imageLabel.pixmap())

    def normalSize(self):
        self.imageLabel.adjustSize()
        self.scaleFactor = 1.0

    def scaleImage(self, factor):
        self.scaleFactor *= factor
        self.imageLabel.resize(self.scaleFactor * self.imageLabel.pixmap().size())

        self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)

        self.zoomInAct.setEnabled(self.scaleFactor < 3.0)
        self.zoomOutAct.setEnabled(self.scaleFactor > 0.333)


    #def countEvent(self):
        #



def main():    
    app = QtGui.QApplication(sys.argv)
    window = Calculescence()
    window.resize(1000,1000)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    sys.exit(main())     



#ICON CREDIT
#<div>Icons made by <a href="http://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a> is licensed by <a href="http://creativecommons.org/licenses/by/3.0/" title="Creative Commons BY 3.0" target="_blank">CC 3.0 BY</a></div>


