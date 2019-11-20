
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSignal
import sys
import math
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import cv2
from os import path
QtCore.QCoreApplication.addLibraryPath(path.join(path.dirname(QtCore.__file__), "plugins"))
QtGui.QImageReader.supportedImageFormats()
import ContourCounting
import TESTVIDEODELETE
import SaveImage
import VideoCellCounter
import mousePosition
import VideoCellCounterWMV
import connect
import drawNewCell
import plot_path


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

class Thread(QtCore.QThread):
    def run(self):
        QtCore.QThread.sleep(1)

#ICONS USED IN THIS DEMO WERE FREE FROM
#<div>Icons made by <a href="http://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a> is licensed by <a href="http://creativecommons.org/licenses/by/3.0/" title="Creative Commons BY 3.0" target="_blank">CC 3.0 BY</a></div>

class Calculescence(QtGui.QMainWindow):
    
    def __init__(self):
        super(Calculescence, self).__init__()
        self.resize(1000,700)
        self.center()
        self.setWindowTitle('CLONETIFY-IT DEMO') 
        self.setWindowIcon(QtGui.QIcon('bacteria.png'))
        self.initUI()
        self.createActions()
        self.createToolbar()
        self.createMenu()

    def initUI(self):
        self.l1 = QtGui.QLabel(self)
        self.l1.setPixmap(QPixmap('bacteria.png'))
        self.l1.setGeometry(QtCore.QRect(480, 80, 100, 200))
        self.titleLabel = QtGui.QLabel(self)
        self.titleLabel.setText('CLONETIFY-IT')
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Times New Roman"))
        font.setPointSize(24)
        self.titleLabel.setFont(font)
        self.titleLabel.setGeometry(QtCore.QRect(570,80,700,200))

        self.progress = QtGui.QProgressBar(self)
        self.progress.setGeometry(520, 1560, 440, 50)
        self.progress.setValue(0)
        self.progress.setStyleSheet("font: 8pt; border-radius: 15px; border-style: outset; border-width: 2px; border-color: gray; text-align: center")

        self.imgcontrolsLabel = QtGui.QLabel(self)
        self.imgcontrolsLabel.setText('IMAGE CONTROLS')
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Times New Roman"))
        font.setPointSize(14)
        #font.setBold(True)
        self.imgcontrolsLabel.setFont(font)
        self.imgcontrolsLabel.setStyleSheet("font-weight: bold")
        self.imgcontrolsLabel.setGeometry(QtCore.QRect(1600,150,700,200))
        
        self.imageLabel = QtGui.QLabel()
        self.imageLabel.setPixmap(QPixmap('division.jpg'))
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.imageLabel.setStyleSheet("background-color = white; border-style: inset")
        self.imageLabel.setScaledContents(True)
        self.imageLabel.adjustSize()
        self.imageLabel.resize(1000,1000)

        self.scrollArea = QtGui.QScrollArea(self)
        self.scrollArea.setGeometry(QtCore.QRect(50, 250, 1400, 1200))
        self.scrollArea.setWidget(self.imageLabel)
        self.scrollArea.setAlignment(Qt.AlignCenter)
        self.scrollArea.setStyleSheet("font: 8pt; border-radius: 15px; border-style: outset; border-width: 4px; border-color: gray")
        self.setCentralWidget(self.scrollArea)

        self.uploadImgButton = QtGui.QPushButton(' UPLOAD IMAGE', self)
        icon = QIcon('openimg.png')
        self.uploadImgButton.setIcon(icon)
        self.uploadImgButton.setGeometry(QtCore.QRect(1600,300,350,100))
        self.uploadImgButton.clicked.connect(self.openimgEvent)
        self.uploadImgButton.setStyleSheet("font: 8pt; border-radius: 20px; border-style: outset; border-width: 4px; border-color: gray")
        self.uploadImgButton.setCheckable(True)

        self.inButton = QtGui.QPushButton(' IN', self)
        icon = QIcon('zoom-in.png')
        self.inButton.setIcon(icon)
        self.inButton.setGeometry(QtCore.QRect(1600,420,170,100))
        self.inButton.clicked.connect(self.zoominEvent)
        self.inButton.setStyleSheet("font: 8pt; border-radius: 15px; border-style: outset; border-width: 4px; border-color: gray")

        self.outButton = QtGui.QPushButton(' OUT', self)
        icon = QIcon('zoomout.png')
        self.outButton.setIcon(icon)
        self.outButton.setGeometry(QtCore.QRect(1780,420,170,100))
        self.outButton.clicked.connect(self.zoomoutEvent)
        self.outButton.setStyleSheet("font: 8pt; border-radius: 15px; border-style: outset; border-width: 4px; border-color: gray")

        self.countButton = QtGui.QPushButton('  DETECT CELLS', self)
        icon = QIcon('detect.png')
        self.countButton.setIcon(icon)
        self.countButton.setGeometry(QtCore.QRect(1970,420,350,100))
        self.countButton.clicked.connect(self.countEvent)
        self.countButton.setStyleSheet("font: 8pt; border-radius: 15px; border-style: outset; border-width: 4px; border-color: gray")

        self.saveButton = QtGui.QPushButton('  SAVE IMAGE ', self)
        icon = QIcon('save.png')
        self.saveButton.setIcon(icon)
        self.saveButton.setGeometry(QtCore.QRect(1970,300,350,100))
        self.saveButton.clicked.connect(self.saveEvent)
        self.saveButton.setStyleSheet("font: 8pt; border-radius: 15px; border-style: outset; border-width: 4px; border-color: gray")

        self.vidcontrolsLabel = QtGui.QLabel(self)
        self.vidcontrolsLabel.setText('VIDEO CONTROLS')
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Times New Roman"))
        font.setPointSize(14)
        self.vidcontrolsLabel.setFont(font)
        self.vidcontrolsLabel.setStyleSheet("font-weight: bold")
        self.vidcontrolsLabel.setGeometry(QtCore.QRect(1600,520,700,200))

        self.uploadVidButton = QtGui.QPushButton(' UPLOAD VIDEO', self)
        icon = QIcon('openvid.png')
        self.uploadVidButton.setIcon(icon)
        self.uploadVidButton.setGeometry(QtCore.QRect(1600,670,350,100))
        self.uploadVidButton.clicked.connect(self.openvidEvent)
        self.uploadVidButton.setStyleSheet("font: 8pt; border-radius: 15px; border-style: outset; border-width: 4px; border-color: gray")

        self.countVidButton = QtGui.QPushButton('  DETECT CELLS', self)
        icon = QIcon('detect.png')
        self.countVidButton.setIcon(icon)
        self.countVidButton.setGeometry(QtCore.QRect(1600,790,350,100))
        self.countVidButton.clicked.connect(self.vidCountEvent)
        self.countVidButton.setStyleSheet("font: 8pt; border-radius: 15px; border-style: outset; border-width: 4px; border-color: gray")

        self.extractFButton = QtGui.QPushButton(' EXTRACT FRAME', self)
        icon = QIcon('extract.png')
        self.extractFButton.setIcon(icon)
        self.extractFButton.setGeometry(QtCore.QRect(1970,790,350,100))
        self.extractFButton.setStyleSheet("font: 8pt; border-radius: 15px; border-style: outset; border-width: 4px; border-color: gray")
        self.extractFButton.clicked.connect(self.extractEvent)

        self.addCellButton = QtGui.QPushButton(' ADD CELL', self)
        icon = QIcon('select1.png')
        self.addCellButton.setIcon(icon)
        self.addCellButton.setGeometry(QtCore.QRect(1600,1030,350,100))
        self.addCellButton.clicked.connect(self.addCell)
        self.addCellButton.setStyleSheet("font: 8pt; border-radius: 15px; border-style: outset ; border-width: 4px; border-color: gray")

        self.trackButton = QtGui.QPushButton(' TRACK CELL', self)
        icon = QIcon('tracking.png')
        self.trackButton.setIcon(icon)
        self.trackButton.setGeometry(QtCore.QRect(1970,910,350,100))
        self.trackButton.setStyleSheet("font: 8pt; border-radius: 15px; border-style: outset; border-width: 4px; border-color: gray")
        self.trackButton.clicked.connect(self.trackEvent)

        self.graphButton = QtGui.QPushButton(' MAP TRAJECTORY', self)
        icon = QIcon('graph.png')
        self.graphButton.setIcon(icon)
        self.graphButton.setGeometry(QtCore.QRect(1970,1030,350,100))
        self.graphButton.setStyleSheet("font: 8pt; border-radius: 15px; border-style: outset; border-width: 4px; border-color: gray")
        self.graphButton.clicked.connect(self.graphEvent)

        self.image = None

        self.playButton = QtGui.QPushButton(self)
        icon = QIcon('play2.png')
        self.playButton.setIcon(icon)
        self.playButton.setGeometry(QtCore.QRect(580,1450,80,80))
        self.playButton.clicked.connect(self.playEvent)
        self.playButton.setStyleSheet("font: 8pt; border-width: 4px; border-color: black")
        self.thread = Thread()
        self.thread.finished.connect(lambda: self.playButton.setEnabled(True))
        #self.show()

        self.stopButton = QtGui.QPushButton(self)
        icon = QIcon('stop2.png')
        self.stopButton.setIcon(icon)
        self.stopButton.setGeometry(QtCore.QRect(662,1450,80,80))
        self.stopButton.clicked.connect(self.stopEvent)
        self.stopButton.setStyleSheet("font: 8pt; border-width: 4px; color: white")

        self.selectButton = QtGui.QPushButton(' TAG', self)
        icon = QIcon('tag.png')
        self.selectButton.setIcon(icon)
        self.selectButton.setGeometry(QtCore.QRect(1600,910,170,100))
        self.selectButton.setStyleSheet("font: 8pt; border-radius: 15px; border-style: outset; border-width: 4px; border-color: gray")
        self.selectButton.clicked.connect(self.selectEvent)

        self.unselectButton = QtGui.QPushButton(' UN-TAG', self)
        icon = QIcon('untag.png')
        self.unselectButton.setIcon(icon)
        self.unselectButton.setGeometry(QtCore.QRect(1780,910,170,100))
        self.unselectButton.setStyleSheet("font: 8pt; border-radius: 15px; border-style: outset; border-width: 4px; border-color: gray")
        self.unselectButton.clicked.connect(self.unselectEvent)

        self.nextFrameButton = QtGui.QPushButton(self)
        icon = QIcon('next2.png')
        self.nextFrameButton.setIcon(icon)
        self.nextFrameButton.setGeometry(QtCore.QRect(744,1450,80,80))
        self.nextFrameButton.clicked.connect(self.nextFrameEvent)
        self.nextFrameButton.setStyleSheet("font: 8pt; border-width: 4px; border-color: gray")

        self.backFrameButton = QtGui.QPushButton(self)
        icon = QIcon('back2.png')
        self.backFrameButton.setIcon(icon)
        self.backFrameButton.setGeometry(QtCore.QRect(826,1450,80,80))
        self.backFrameButton.clicked.connect(self.backFrameEvent)
        self.backFrameButton.setStyleSheet("font: 8pt;border-width: 4px; border-color: gray")

        self.saveImageButton = QtGui.QPushButton(' SAVE TAGGED FRAME', self)
        icon = QIcon('savevid.png')
        self.saveImageButton.setIcon(icon)
        self.saveImageButton.setGeometry(QtCore.QRect(1970,670,350,100))
        self.saveImageButton.clicked.connect(self.saveFrameEvent)
        self.saveImageButton.setStyleSheet("font: 8pt; border-radius: 15px; border-style: outset ; border-width: 4px; border-color: gray")

        self.resultsLabel = QtGui.QLabel(self)
        self.resultsLabel.setText('RESULTS')
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Times New Roman"))
        font.setPointSize(14)
        self.resultsLabel.setFont(font)
        self.resultsLabel.setStyleSheet("font-weight: bold")
        self.resultsLabel.setGeometry(QtCore.QRect(1600,1180,700,100))
        self.resultsLabel.hide()

        self.rtextLabel = QtGui.QLabel(self)
        self.rtextLabel.setText('Number of Cells Detected: ')
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Times New Roman"))
        font.setPointSize(13)
        self.rtextLabel.setFont(font)
        self.rtextLabel.setGeometry(QtCore.QRect(1600,1270,400,100))
        self.rtextLabel.hide()

        self.numberCellsLabel = QtGui.QLabel(self)
        self.numberCellsLabel.setText(' 0')
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Times New Roman"))
        font.setPointSize(13)
        self.numberCellsLabel.setFont(font)
        self.numberCellsLabel.setGeometry(QtCore.QRect(2020,1280,300,80))
        self.numberCellsLabel.setStyleSheet("border-radius: 8px; border-style: groove; border-width: 4px; border-color: gray")
        self.numberCellsLabel.hide()

        #VBOX1
        vbox1 = QtGui.QVBoxLayout()
        vbox1.addStretch(1)
        vbox1.addWidget(self.l1)
        vbox1.addWidget(self.titleLabel)
        vbox1.addWidget(self.scrollArea)
        vbox1.addWidget

        #VBOX2
        vbox2 = QtGui.QVBoxLayout()
        vbox2.addStretch(1)
        vbox2.addWidget(self.countButton)
        vbox2.addWidget(self.saveButton)

        #HBOX
        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addLayout(vbox1)
        hbox.addLayout(vbox2)

        self.setLayout(hbox)
        connect.create_connections(self)
        self.show()

    def createActions(self):  

        self.openimgAction = QtGui.QAction(QtGui.QIcon('openimg.png'), '&Open Image', self)        
        self.openimgAction.setShortcut('Ctrl+I')
        self.openimgAction.setStatusTip('Open Image')
        self.openimgAction.triggered.connect(self.openimgEvent)

        self.saveAction = QtGui.QAction(QtGui.QIcon('save.png'), '&Save Image', self)        
        self.saveAction.setShortcut('Ctrl+S')
        self.saveAction.setStatusTip('Save Image')
        self.saveAction.triggered.connect(self.saveEvent)

        self.zoomInAction = QtGui.QAction(QtGui.QIcon('zoom-in.png'), '&ZoomIn', self)        
        self.zoomInAction.setShortcut('Ctrl+Z')
        self.zoomInAction.setStatusTip('Zoom In')
        self.zoomInAction.triggered.connect(self.zoominEvent)

        self.zoomOutAction = QtGui.QAction(QtGui.QIcon('zoomout.png'), '&ZoomOut', self)        
        self.zoomOutAction.setShortcut('Ctrl+O')
        self.zoomOutAction.setStatusTip('Zoom Out')
        self.zoomOutAction.triggered.connect(self.zoomoutEvent)

        self.countAction = QtGui.QAction(QtGui.QIcon('detect.png'), 'Count Cells in Image', self)        
        self.countAction.setShortcut('Ctrl+C')
        self.countAction.setStatusTip('Count Cells')
        #self.countAction.triggered.connect(self.countEvent)

        # self.editAction = QtGui.QAction(QtGui.QIcon('edit.png'), '&Edit', self)        
        # self.editAction.setShortcut('Ctrl+E')
        # self.editAction.setStatusTip('Edit Image')
        # #openAction.triggered.connect(QtGui.qApp.open)

        self.openvidAction = QtGui.QAction(QtGui.QIcon('openvid.png'), '&Open Video', self)        
        self.openvidAction.setShortcut('Ctrl+O')
        self.openvidAction.setStatusTip('Open Video')
        self.openvidAction.triggered.connect(self.openvidEvent)

        self.extractAction = QtGui.QAction(QtGui.QIcon('extract.png'), '&Extract Video Frame', self)        
        self.extractAction.setShortcut('Ctrl+X')
        self.extractAction.setStatusTip('Extract Video Frame')
        self.extractAction.triggered.connect(self.extractEvent)

        self.saveFrameAction = QtGui.QAction(QtGui.QIcon('savevid.png'), '&Save Marked Frame', self)        
        self.saveFrameAction.setShortcut('Ctrl+M')
        self.saveFrameAction.setStatusTip('Save Marked Down Frame')
        self.saveFrameAction.triggered.connect(self.saveFrameEvent)

        self.selectAction = QtGui.QAction(QtGui.QIcon('tag.png'), 'Tag Cell to Track', self)        
        self.selectAction.setShortcut('Ctrl+Shift+T')
        self.selectAction.setStatusTip('Tag Cell to be Tracked')
        self.selectAction.triggered.connect(self.selectEvent)

        self.unselectAction = QtGui.QAction(QtGui.QIcon('untag.png'), 'Un-Tag Cell to Track', self)        
        self.unselectAction.setShortcut('Ctrl+Shift+U')
        self.unselectAction.setStatusTip('Un-Tag Cell to be Tracked')
        self.unselectAction.triggered.connect(self.unselectEvent)

        self.addCellAction = QtGui.QAction(QtGui.QIcon('untag.png'), 'Add Cell', self)        
        self.addCellAction.setShortcut('Ctrl+Shift+U')
        self.addCellAction.setStatusTip('Add Cell')
        self.addCellAction.triggered.connect(self.addCell)

        self.trackingAction = QtGui.QAction(QtGui.QIcon('tracking.png'), '&Track Selected Cell', self)        
        self.trackingAction.setShortcut('Ctrl+T')
        self.trackingAction.setStatusTip('Track Selected Cell')
        self.trackingAction.triggered.connect(self.trackEvent)

        self.graphAction = QtGui.QAction(QtGui.QIcon('graph.png'), '&Map Trajectory', self)        
        self.graphAction.setShortcut('Ctrl+T')
        self.graphAction.setStatusTip('Map Trajectory')
        self.graphAction.triggered.connect(self.graphEvent)

        self.settingsAction = QtGui.QAction(QtGui.QIcon('settings2.png'), '&Settings', self)        
        self.settingsAction.setShortcut('Ctrl+G')
        self.settingsAction.setStatusTip('Settings')
        self.settingsAction.triggered.connect(self.settingsEvent)

        self.helpAction = QtGui.QAction(QtGui.QIcon('help.png'), '&How to...', self)
        self.helpAction.setStatusTip('Search for Help')
        self.helpAction.triggered.connect(self.helpEvent)

        self.updateAction = QtGui.QAction(QtGui.QIcon('update.png'), '&Update', self)
        self.updateAction.setStatusTip('Check for Updates')
        self.updateAction.triggered.connect(self.updateEvent)

        self.aboutAction = QtGui.QAction(QtGui.QIcon('about.png'), '&About', self)
        self.aboutAction.setStatusTip('Who made this program?')
        self.aboutAction.triggered.connect(self.aboutEvent)

        self.exitAction = QtGui.QAction(QtGui.QIcon('close2.png'), '&Exit', self)        
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Exit application')
        #self.exitAction.triggered.connect(self.closeEvent)
        self.exitAction.triggered.connect(QtGui.qApp.quit)

        self.exitAction2 = QtGui.QAction(QtGui.QIcon('close2.png'), '&Exit', self)        
        self.exitAction2.setShortcut('Ctrl+Q')
        self.exitAction2.setStatusTip('Exit application')
        self.exitAction2.triggered.connect(self.closeEvent2)

    def createToolbar(self):

        self.toolbar = self.addToolBar('Open Image')
        self.toolbar.addAction(self.openimgAction)

        # self.toolbar = self.addToolBar('Save Image')
        # self.toolbar.addAction(self.saveAction)

        # self.toolbar = self.addToolBar('ZoomIn')
        # self.toolbar.addAction(self.zoomInAction)

        # self.toolbar = self.addToolBar('ZoomOut')
        # self.toolbar.addAction(self.zoomOutAction)

        # self.toolbar = self.addToolBar('Edit')
        # self.toolbar.addAction(self.editAction)

        self.toolbar = self.addToolBar('Open Video')
        self.toolbar.addAction(self.openvidAction)

        # self.toolbar = self.addToolBar('Extract Video Frame')
        # self.toolbar.addAction(self.extractAction)

        # self.toolbar = self.addToolBar('Save Marked Frame')
        # self.toolbar.addAction(self.saveFrameAction)

        # self.toolbar = self.addToolBar('Tag a Cell')
        # self.toolbar.addAction(self.selectAction)

        # self.toolbar = self.addToolBar('Track a Cell')
        # self.toolbar.addAction(self.trackingAction)

        # self.toolbar = self.addToolBar('Count Cells')
        # self.toolbar.addAction(self.countAction)

        self.toolbar = self.addToolBar('Settings')
        self.toolbar.addAction(self.settingsAction)

        self.toolbar = self.addToolBar('Update')
        self.toolbar.addAction(self.updateAction)

        self.toolbar = self.addToolBar('Help')
        self.toolbar.addAction(self.helpAction)

        self.toolbar = self.addToolBar('About')
        self.toolbar.addAction(self.aboutAction)

        # self.toolbar = self.addToolBar('Exit')
        # self.toolbar.addAction(self.exitAction2)

    def createMenu(self):

        menubar = self.menuBar()
        menubar.setStyleSheet('font-size:10pt')

        fileMenu = menubar.addMenu('&File  ')
        fileMenu.addAction(self.openvidAction)
        fileMenu.addAction(self.openimgAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.saveFrameAction)
        fileMenu.addAction(self.settingsAction)
        fileMenu.addAction(self.exitAction2)

        updateMenu= menubar.addMenu('&Update  ')
        updateMenu.addAction(self.updateAction)

        helpMenu = menubar.addMenu('&Help  ')
        helpMenu.addAction(self.helpAction)

        aboutMenu = menubar.addMenu('&About  ')
        aboutMenu.addAction(self.aboutAction)

        self.statusBar().showMessage('Ready for Input...') 
        self.show()


    def closeEvent2(self):
        choice = QtGui.QMessageBox.question(self, 'Exit', "Are you sure you quit?",
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            sys.exit()
        else:
            pass
        
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
        self.imageLabel.resize(1000,1000)
        self.name = QtGui.QFileDialog.getOpenFileName(self, 'Open Video File', QtCore.QDir.currentPath(), "Video Files (*.avi *.wmv)")
        self.capture =cv2.VideoCapture(self.name)
        self.numberCellsLabel.setText(' 0')
        ret,self.image = self.capture.read()
        self.pos_frame = 1
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        qImage = QtGui.QImage(self.image, self.image.shape[1], self.image.shape[0], QtGui.QImage.Format_RGB888)
        self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(qImage))
        self.count = False
        self.select = False
        self.track = False
        self.graph = False
        self.play = False
        self.c = 0
        
        self.countVidButton.setEnabled(True)
        self.saveImageButton.setEnabled(True)
        self.extractFButton.setEnabled(True)
        self.trackButton.setEnabled(True)
        self.selectButton.setEnabled(True)
        self.unselectButton.setEnabled(True)
        self.playButton.setEnabled(True)
        self.stopButton.setEnabled(True)
        self.nextFrameButton.setEnabled(True)
        self.backFrameButton.setEnabled(True)
        self.addCellButton.setEnabled(True)
        self.graphButton.setEnabled(True)

        self.countButton.setEnabled(False)
        self.inButton.setEnabled(False)
        self.outButton.setEnabled(False)
        self.saveButton.setEnabled(False)
        

    def vidCountEvent(self):
        extension = self.name[self.name.rfind('.'):]
        if extension == '.avi':
            self.tagged, self.counter, self.cells, self.height, self.width, self.avg_area = VideoCellCounter.counter(self.name, self.pos_frame)
            self.frame = cv2.cvtColor(self.tagged, cv2.COLOR_BGR2RGB)
            cv2.imwrite('temp.png', self.frame)
            self.runtime()
            qImage = QtGui.QImage(self.frame, self.frame.shape[1], self.frame.shape[0], QtGui.QImage.Format_RGB888)
            self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(qImage))
            self.numberCellsLabel.setText(str(self.counter))
            self.select = False
            self.track = False
            self.add = False
            self.unselect = False
            #self.graph=False
            self.imageLabel.mousePressEvent = self.getPos
            self.x = 0
            self.y = 0
            self.count = True
            self.resultsLabel.show()
            self.rtextLabel.show()
            self.numberCellsLabel.show()
        elif extension == '.wmv':
            self.tagged, self.counter, self.cells, self.height, self.width, self.avg_area = VideoCellCounterWMV.counter(self.name, self.pos_frame)
            self.frame = cv2.cvtColor(self.tagged, cv2.COLOR_BGR2RGB)
            cv2.imwrite('temp.png', self.frame)
            self.runtime()
            qImage = QtGui.QImage(self.frame, self.frame.shape[1], self.frame.shape[0], QtGui.QImage.Format_RGB888)
            self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(qImage))
            self.numberCellsLabel.setText(str(self.counter))
            self.select = False
            self.track = False
            self.add = False
            self.unselect = False
            #self.graph= False
            self.imageLabel.mousePressEvent = self.getPos
            self.x = 0
            self.y = 0
            self.count = True
            self.resultsLabel.show()
            self.rtextLabel.show()
            self.numberCellsLabel.show()

    def addCell(self):
        if self.count == False:
            self.msgSelectNext = QtGui.QMessageBox()
            self.msgSelectNext.setIcon(QMessageBox.Warning)
            self.msgSelectNext.setWindowIcon(QtGui.QIcon('bacteria.png'))
            self.msgSelectNext.setWindowTitle("You missed a step!")
            self.msgSelectNext.setText("        1. 'Detect Cells'       \n"
                                       "     2. 'Tag' or 'Add Cell'     ")
            self.msgSelectNext.setStandardButtons(QtGui.QMessageBox.Ok)
            self.msgSelectNext.show()
            pass

        if self.x == 0:
            self.msgSelectNext = QtGui.QMessageBox()
            self.msgSelectNext.setIcon(QMessageBox.Warning)
            self.msgSelectNext.setWindowIcon(QtGui.QIcon('bacteria.png'))
            self.msgSelectNext.setWindowTitle("You missed a step!")
            self.msgSelectNext.setText("       1. Click on a Cell          \n"
                                       "     2. Click on 'Add Cell'     ")
            self.msgSelectNext.setStandardButtons(QtGui.QMessageBox.Ok)
            self.msgSelectNext.show()
            pass

        if self.select == True:
            self.msgSelectNext = QtGui.QMessageBox()
            self.msgSelectNext.setIcon(QMessageBox.Warning)
            self.msgSelectNext.setWindowIcon(QtGui.QIcon('bacteria.png'))
            self.msgSelectNext.setWindowTitle("You missed a step!")
            self.msgSelectNext.setText("  1. Please 'UN-TAG' first           \n"
                                       "        2. 'ADD CELL'                ")
            self.msgSelectNext.setStandardButtons(QtGui.QMessageBox.Ok)
            self.msgSelectNext.show()
            pass

        if self.count == True:
            self.add = True
            r = int(round((math.sqrt(self.avg_area/(math.pi)))))
            cx = int(round(self.x/2))
            cy= int(round(self.y/2))
            x1 = math.ceil(cx - r)
            y1 = math.ceil(cy - r)
            self.cells.append([x1, y1, x1+(2*r), y1+(2*r), cx, cy])
            side = int(round(r/math.e))
            print(x1, y1, x1+side, y1+side, cx, cy)
            self.frame = drawNewCell.draw(self.name, self.pos_frame, self.cells)
            self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            self.counter = self.counter + 1
            qImage = QtGui.QImage(self.frame, self.frame.shape[1], self.frame.shape[0], QtGui.QImage.Format_RGB888)
            self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(qImage))
            self.numberCellsLabel.setText(str(self.counter))
            self.x = 0
            self.add = False
            self.track = False

    def playEvent(self):

        if self.play == False:
            self.play = True
            if self.pos_frame == 1:
                #self.name = QtGui.QFileDialog.getOpenFileName(self, 'Open Video File')
                self.capture =cv2.VideoCapture(self.name)
                self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1000)
                self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1000)
                self.timer=QTimer(self)
                self.timer.timeout.connect(self.loopEvent)
                self.timer.start(15)
                if not self.thread.isRunning():
                    self.playButton.setEnabled(False)
                    self.thread.start()
                    self.pos_frame = self.pos_frame - 2
            else:
                if not self.thread.isRunning():
                    self.playButton.setEnabled(False)
                    self.thread.start()
                    self.timer=QTimer(self)
                    self.timer.timeout.connect(self.loopEvent)
                    self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1000)
                    self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1000)
                    self.capture.get(7)
                    self.capture.set(1,(self.pos_frame))
                    self.timer.start(30)
                    self.pos_frame = self.pos_frame + 1
        else:
            pass

    def stopEvent(self):
        self.play = False
        self.timer.stop()
        print(self.pos_frame)
        self.unselect = False
        #self.pos_frame = self.pos_frame

    def loopEvent(self):
        self.pos_frame = self.pos_frame + 1
        ret,self.image = self.capture.read()
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        qImage = QtGui.QImage(self.image, self.image.shape[1], self.image.shape[0], QtGui.QImage.Format_RGB888)
        self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(qImage))
        print(self.pos_frame)

    def nextFrameEvent(self):
        self.pos_frame = self.pos_frame + 1
        self.capture.get(7)
        self.capture.set(1,(self.pos_frame))
        ret,self.image = self.capture.read()
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        qImage = QtGui.QImage(self.image, self.image.shape[1], self.image.shape[0], QtGui.QImage.Format_RGB888)
        self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(qImage))
        self.count = False
        self.select = False
        self.track = False
        self.unselect = False
        self.numberCellsLabel.setText(' 0')
        # self.pos_frame = self.pos_frame+1
        # ret,self.image = self.capture.read()
        # self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        # qImage = QtGui.QImage(self.image, self.image.shape[1], self.image.shape[0], QtGui.QImage.Format_RGB888)
        # self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(qImage))

    def backFrameEvent(self):
        self.pos_frame = self.pos_frame - 1
        self.capture.get(7)
        self.capture.set(1,(self.pos_frame))
        ret,self.image = self.capture.read()
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        qImage = QtGui.QImage(self.image, self.image.shape[1], self.image.shape[0], QtGui.QImage.Format_RGB888)
        self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(qImage))
        self.count = False
        self.select = False
        self.track = False
        self.unselect = False
        self.numberCellsLabel.setText(' 0')
        
    def extractEvent(self):
        self.image = TESTVIDEODELETE.extraction(self.name, self.pos_frame)
        self.saveEvent()

    def selectEvent(self):
        #self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        if self.count == False:
            self.msgSelectNext = QtGui.QMessageBox()
            self.msgSelectNext.setIcon(QMessageBox.Warning)
            self.msgSelectNext.setWindowIcon(QtGui.QIcon('bacteria.png'))
            self.msgSelectNext.setWindowTitle("You missed a step!")
            self.msgSelectNext.setText("    1. 'Detect Cells'         \n"
                                       "     2. 'Tag' a Cell        ")
            self.msgSelectNext.setStandardButtons(QtGui.QMessageBox.Ok)
            self.msgSelectNext.show()
            pass

        elif self.x == 0:
            self.msgSelectNext = QtGui.QMessageBox()
            self.msgSelectNext.setIcon(QMessageBox.Warning)
            self.msgSelectNext.setWindowIcon(QtGui.QIcon('bacteria.png'))
            self.msgSelectNext.setWindowTitle("You missed a step!")
            self.msgSelectNext.setText("    1. Click on a Cell         \n"
                                       "    2. Click on 'TAG'       ")
            self.msgSelectNext.setStandardButtons(QtGui.QMessageBox.Ok)
            self.msgSelectNext.show()
            pass

        if self.count == True:
            self.select = True
            self.track = False
            self.graph = False
            self.unselect = False
            qImage = QtGui.QImage(self.frame, self.frame.shape[1], self.frame.shape[0], QtGui.QImage.Format_RGB888)
            self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(qImage))
            
            self.subset=[]
            self.subsetFinal=[]
            self.subsetFinal2=[]
            distanceList=[]
            self.x1 = int(round(self.x/2))
            self.y1 = int(round(self.y/2))
            for i in range (0,len(self.cells)):    
                if self.x1 > self.cells[i][0]:
                    if self.y1 > self.cells[i][1]:
                        self.subset.append(self.cells[i])
                    else:
                        pass
                else:
                    pass

            for j in range(0, len(self.subset)):
                distance = math.sqrt( ((self.x1-self.subset[j][0])**2)+((self.y1-self.subset[j][1])**2))
                self.subsetFinal.append(self.subset[j])
                distanceList.append(distance)
                
            index = distanceList.index(min(distanceList))
            self.subsetFinal2.append(self.subsetFinal[index])

            self.frame2 = VideoCellCounter.drawRectangle(self.frame, self.subsetFinal2)
            #self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            qImage = QtGui.QImage(self.frame2, self.frame2.shape[1], self.frame2.shape[0], QtGui.QImage.Format_RGB888)
            self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(qImage))
            #self.x = 0
            #self.y = 0

    def unselectEvent(self):
        if self.count == True and self.select == True:
            self.unselect = True
            self.select = False
            self.frame = cv2.imread('temp.png')
            qImage = QtGui.QImage(self.frame, self.frame.shape[1], self.frame.shape[0], QtGui.QImage.Format_RGB888)
            self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(qImage))

        elif self.count == False:
            self.msgwarning = QtGui.QMessageBox()
            self.msgwarning.setIcon(QMessageBox.Warning)
            self.msgwarning.setWindowIcon(QtGui.QIcon('bacteria.png'))
            self.msgwarning.setWindowTitle("You missed a step!")
            self.msgwarning.setText("       Please first 'DETECT' Cells              ")
            self.msgwarning.setStandardButtons(QtGui.QMessageBox.Ok)
            self.msgwarning.show()
            pass

        elif self.select == False:
            self.msgwarning = QtGui.QMessageBox()
            self.msgwarning.setIcon(QMessageBox.Warning)
            self.msgwarning.setWindowIcon(QtGui.QIcon('bacteria.png'))
            self.msgwarning.setWindowTitle("You missed a step!")
            self.msgwarning.setText("       Please first 'TAG' a Cell              ")
            self.msgwarning.setStandardButtons(QtGui.QMessageBox.Ok)
            self.msgwarning.show()
            pass

    def getPos(self, event):
        self.x = event.pos().x()
        self.y = event.pos().y()
        #return self.x, self.y
        #printernt(self.x,self.y)

    def trackEvent(self):
        if self.x == 0:
            self.msgwarning = QtGui.QMessageBox()
            self.msgwarning.setIcon(QMessageBox.Warning)
            self.msgwarning.setWindowIcon(QtGui.QIcon('bacteria.png'))
            self.msgwarning.setWindowTitle("You missed a step!")
            self.msgwarning.setText("       Please first 'TAG' a Cell              ")
            self.msgwarning.setStandardButtons(QtGui.QMessageBox.Ok)
            self.msgwarning.show()
            pass

        elif self.select == False:
            self.msgwarning = QtGui.QMessageBox()
            self.msgwarning.setIcon(QMessageBox.Warning)
            self.msgwarning.setWindowIcon(QtGui.QIcon('bacteria.png'))
            self.msgwarning.setWindowTitle("You missed a step!")
            self.msgwarning.setText("       Please first 'TAG' a Cell              ")
            self.msgwarning.setStandardButtons(QtGui.QMessageBox.Ok)
            self.msgwarning.show()
            pass

        if self.select == True:
            self.track = True
            self.graph = False
            self.c = self.c + 1
            self.Xarray, self.Yarray = mousePosition.track(self.name, self.subsetFinal2, self.pos_frame, self.c)
            self.subsetFinal2 = ([0,0])
            self.x = 0
            self.y = 0

    def graphEvent(self):

        if self.graph == False:
            self.graph = True
            plot_path.plot(self.Xarray,self.Yarray)
        else:
            self.msgwarning = QtGui.QMessageBox()
            self.msgwarning.setIcon(QMessageBox.Warning)
            self.msgwarning.setWindowIcon(QtGui.QIcon('bacteria.png'))
            self.msgwarning.setWindowTitle("You missed a step!")
            self.msgwarning.setText("Please first 'TRACK' a Cell to obtain its trajectory         ")
            self.msgwarning.setStandardButtons(QtGui.QMessageBox.Ok)
            self.msgwarning.show()
            pass


    def openimgEvent(self):
        self.file = QtGui.QFileDialog.getOpenFileName(self, 'Open Image File', QtCore.QDir.currentPath(), "Image Files (*.jpg *.gif *.png)")
        
        if self.file:
            self.image = QtGui.QImage(self.file)
            if self.image.isNull():
                QtGui.QMessageBox.information(self, "Image Viewer",
                        "Cannot load %s." % self.file)
                return

            self.imageLabel.setPixmap(QtGui.QPixmap(self.image))
            self.scaleFactor = 1.0

        self.numberCellsLabel.setText(' 0')
        self.saveImageButton.setEnabled(False)
        self.countVidButton.setEnabled(False)
        self.extractFButton.setEnabled(False)
        self.trackButton.setEnabled(False)
        self.selectButton.setEnabled(False)
        self.unselectButton.setEnabled(False)
        self.playButton.setEnabled(False)
        self.stopButton.setEnabled(False)
        self.nextFrameButton.setEnabled(False)
        self.backFrameButton.setEnabled(False)
        self.addCellButton.setEnabled(False)
        self.graphButton.setEnabled(False)

        self.countButton.setEnabled(True)
        self.inButton.setEnabled(True)
        self.outButton.setEnabled(True)
        self.saveButton.setEnabled(True)

    def saveEvent(self):
        name = QtGui.QFileDialog.getSaveFileName(self, 'Save File')
        SaveImage.save(name, self.image)

    def saveFrameEvent(self):
        name = QtGui.QFileDialog.getSaveFileName(self, 'Save File')
        SaveImage.save(name, self.frame)

    def zoominEvent(self):
        self.scaleImage(1.25)

    def zoomoutEvent(self):
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

    def countEvent(self):
        if self.image:
            
            self.image, self.counter = ContourCounting.counting(self.file)
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            qImage = QtGui.QImage(self.image, self.image.shape[1], self.image.shape[0], QtGui.QImage.Format_RGB888)
            self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(qImage))
            self.runtime()
            self.numberCellsLabel.setText(str(self.counter))
            self.resultsLabel.show()
            self.rtextLabel.show()
            self.numberCellsLabel.show()

    def aboutEvent(self):
        self.msg = QtGui.QMessageBox()
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setWindowIcon(QtGui.QIcon('bacteria.png'))
        self.msg.setWindowTitle("About")
        self.msg.setText("      Clonetify-It\n    Version SJ 1.0                 ")
        self.msg.setInformativeText("       Created By\n   Mayra Banuelos\n      © 2018 MB \n\n   Acknowledgments\n"
            "Anagha Kulkarni, PhD. \n"
            "       Sarai Aquino\n"
            "      Cecelia Brown\n")
        self.msg.setStandardButtons(QtGui.QMessageBox.Ok)
        return self.msg.show()

    def updateEvent(self):
        self.updatemsg = QtGui.QMessageBox()
        self.updatemsg.setIcon(QMessageBox.Information)
        self.updatemsg.setWindowIcon(QtGui.QIcon('bacteria.png'))
        self.updatemsg.setWindowTitle("Check for Update")
        self.updatemsg.setText("         Version SJ 1.0                 ")
        self.updatemsg.setInformativeText("Your software is up to date.\n")
        self.updatemsg.setStandardButtons(QtGui.QMessageBox.Ok)

        return self.updatemsg.show()

    def settingsEvent(self):
        self.settingsmsg = QtGui.QMessageBox()
        self.settingsmsg.setIcon(QMessageBox.Information)
        self.settingsmsg.setWindowIcon(QtGui.QIcon('bacteria.png'))
        self.settingsmsg.setWindowTitle("Settings")
        self.settingsmsg.setText("         Under construction.                 ")
        self.settingsmsg.setInformativeText("      New stuff coming soon!  \n")
        self.settingsmsg.setStandardButtons(QtGui.QMessageBox.Ok)

        return self.settingsmsg.show()

    def runtime(self):
        self.completed = 0
        while self.completed < 100:
            self.completed += 0.001
            self.progress.setValue(self.completed)

    def helpEvent(self):
        self.msgHelp = QtGui.QMessageBox()
        self.msgHelp.setIcon(QMessageBox.Information)
        self.msgHelp.setWindowIcon(QtGui.QIcon('bacteria.png'))
        self.msgHelp.setWindowTitle("       Need Help?      ")
        self.msgHelp.setText("FAQ and How-to Pages Coming Up Soon.                           ")
        self.msgHelp.setInformativeText("\nQuestions or Comments?     \nContact me:\nmbanuelo@mail.sfsu.edu\n")
        self.msgHelp.setStandardButtons(QtGui.QMessageBox.Ok)
        self.msgHelp.show()


    def saveImageButton_pressed(self):
        self.saveImageButton.setStyleSheet("""
            border: 0px;
            background: #99CCFF; border-radius: 20px; border-style: inset; border-width: 10px; border-color: gray;
            """)

    def saveImageButton_released(self):
        self.saveImageButton.setStyleSheet("""
            font: 8pt; border-radius: 20px; border-style: outset; border-width: 4px; border-color: gray;
            """)  


    def backFrameButton_pressed(self):
        self.backFrameButton.setStyleSheet("""
            border: 0px;
            background: #99CCFF; border-radius: 20px; border-style: inset; border-width: 10px; border-color: gray;
            """)

    def backFrameButton_released(self):
        self.backFrameButton.setStyleSheet("""
            font: 8pt; border-style: outset; border-width: 4px; border-color: gray;
            """)  


    def nextFrameButton_pressed(self):
        self.nextFrameButton.setStyleSheet("""
            border: 0px;
            background: #99CCFF; border-radius: 20px; border-style: inset; border-width: 10px; border-color: gray;
            """)

    def nextFrameButton_released(self):
        self.nextFrameButton.setStyleSheet("""
            font: 8pt; border-style: outset; border-width: 4px; border-color: gray;
            """)  


    def unselectButton_pressed(self):
        self.unselectButton.setStyleSheet("""
            border: 0px;
            background: #99CCFF; border-radius: 20px; border-style: inset; border-width: 10px; border-color: gray;
            """)

    def unselectButton_released(self):
        self.unselectButton.setStyleSheet("""
            font: 8pt; border-radius: 20px; border-style: outset; border-width: 4px; border-color: gray;
            """)  


    def selectButton_pressed(self):
        self.selectButton.setStyleSheet("""
            border: 0px;
            background: #99CCFF; border-radius: 20px; border-style: inset; border-width: 10px; border-color: gray;
            """)

    def selectButton_released(self):
        self.selectButton.setStyleSheet("""
            font: 8pt; border-radius: 20px; border-style: outset; border-width: 4px; border-color: gray;
            """)  


    def stopButton_pressed(self):
        self.stopButton.setStyleSheet("""
            border: 0px;
            background: #99CCFF; border-radius: 20px; border-style: inset; border-width: 10px; border-color: gray;
            """)

    def stopButton_released(self):
        self.stopButton.setStyleSheet("""
            font: 8pt; border-style: outset; border-width: 4px; border-color: gray;
            """)  


    def playButton_pressed(self):
        self.playButton.setStyleSheet("""
            border: 0px;
            background: #99CCFF; border-radius: 20px; border-style: inset; border-width: 10px; border-color: gray;
            """)

    def playButton_released(self):
        self.playButton.setStyleSheet("""
            font: 8pt; border-style: outset; border-width: 4px; border-color: gray;
            """)  

    def trackButton_pressed(self):
        self.trackButton.setStyleSheet("""
            border: 0px;
            background: #99CCFF; border-radius: 20px; border-style: inset; border-width: 10px; border-color: gray;
            """)

    def trackButton_released(self):
        self.trackButton.setStyleSheet("""
            font: 8pt; border-radius: 20px; border-style: outset; border-width: 4px; border-color: gray;
            """)  

    def extractFButton_pressed(self):
        self.extractFButton.setStyleSheet("""
            border: 0px;
            background: #99CCFF; border-radius: 20px; border-style: inset; border-width: 10px; border-color: gray;
            """)

    def extractFButton_released(self):
        self.extractFButton.setStyleSheet("""
            font: 8pt; border-radius: 20px; border-style: outset; border-width: 4px; border-color: gray;
            """)  


    def countVidButton_pressed(self):
        self.countVidButton.setStyleSheet("""
            border: 0px;
            background: #99CCFF; border-radius: 20px; border-style: inset; border-width: 10px; border-color: gray;
            """)

    def countVidButton_released(self):
        self.countVidButton.setStyleSheet("""
            font: 8pt; border-radius: 20px; border-style: outset; border-width: 4px; border-color: gray;
            """)   


    def uploadVidButton_pressed(self):
        self.uploadVidButton.setStyleSheet("""
            border: 0px;
            background: #99CCFF; border-radius: 20px; border-style: inset; border-width: 10px; border-color: gray;
            """)

    def uploadVidButton_released(self):
        self.uploadVidButton.setStyleSheet("""
            font: 8pt; border-radius: 20px; border-style: outset; border-width: 4px; border-color: gray;
            """)


    def saveButton_pressed(self):
        self.saveButton.setStyleSheet("""
            border: 0px;
            background: #99CCFF; border-radius: 20px; border-style: inset; border-width: 10px; border-color: gray;
            """)

    def saveButton_released(self):
        self.saveButton.setStyleSheet("""
            font: 8pt; border-radius: 20px; border-style: outset; border-width: 4px; border-color: gray;
            """)


    def countButton_pressed(self):
        self.countButton.setStyleSheet("""
            border: 0px;
            background: #99CCFF; border-radius: 20px; border-style: inset; border-width: 10px; border-color: gray;
            """)

    def countButton_released(self):
        self.countButton.setStyleSheet("""
            font: 8pt; border-radius: 20px; border-style: outset; border-width: 4px; border-color: gray;
            """)


    def button_pressed(self):
        self.uploadImgButton.setStyleSheet("""
            border: 0px;
            background: #99CCFF; border-radius: 20px; border-style: inset; border-width: 10px; border-color: gray;
            """)

    def button_released(self):
        self.uploadImgButton.setStyleSheet("""
            font: 8pt; border-radius: 20px; border-style: outset; border-width: 4px; border-color: gray;
            """)

    def inButton_pressed(self):
        self.inButton.setStyleSheet("""
            border: 0px;
            background: #99CCFF; border-radius: 20px; border-style: inset; border-width: 10px; border-color: gray;
            """)

    def inButton_released(self):
        self.inButton.setStyleSheet("""
            font: 8pt; border-radius: 20px; border-style: outset; border-width: 4px; border-color: gray;
            """)

    def outButton_pressed(self):
        self.outButton.setStyleSheet("""
            border: 0px;
            background: #99CCFF; border-radius: 20px; border-style: inset; border-width: 10px; border-color: gray;
            """)

    def outButton_released(self):
        self.outButton.setStyleSheet("""
            font: 8pt; border-radius: 20px; border-style: outset; border-width: 4px; border-color: gray;
            """)

    def addCellButton_pressed(self):
        self.addCellButton.setStyleSheet("""
            border: 0px;
            background: #99CCFF; border-radius: 20px; border-style: inset; border-width: 10px; border-color: gray;
            """)

    def addCellButton_released(self):
        self.addCellButton.setStyleSheet("""
            font: 8pt; border-radius: 20px; border-style: outset; border-width: 4px; border-color: gray;
            """)

    def graphButton_pressed(self):
        self.graphButton.setStyleSheet("""
            border: 0px;
            background: #99CCFF; border-radius: 20px; border-style: inset; border-width: 10px; border-color: gray;
            """)

    def graphButton_released(self):
        self.graphButton.setStyleSheet("""
            font: 8pt; border-radius: 20px; border-style: outset; border-width: 4px; border-color: gray;
            """)

def main():    
    app = QtGui.QApplication(sys.argv)
    window = Calculescence()
    p = QPalette()
    gradient = QLinearGradient(0, 10, 0, 400)
    window.setStyleSheet("background-color: white")
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    sys.exit(main())     

