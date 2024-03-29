##################################################
## Software interface and backend created to track division and 
## trajectory of Drosophila Melanogaster Cells.
##################################################
## Author: Mayra Banuelos
## Copyright: Copyright 2018, CLONETIFY-IT
## Credits: Sarai Aquino, Ted
## Version: 1.0.0
## Mmaintainer: Mayra Banuelos
## Status: Currently being translated to Python3 and PyQt5
##################################################

def create_connections(self):

        self.uploadImgButton.pressed.connect(self.button_pressed)
        self.uploadImgButton.released.connect(self.button_released)
        self.inButton.pressed.connect(self.inButton_pressed)
        self.inButton.released.connect(self.inButton_released)
        self.outButton.pressed.connect(self.outButton_pressed)
        self.outButton.released.connect(self.outButton_released)
        self.countButton.pressed.connect(self.countButton_pressed)
        self.countButton.released.connect(self.countButton_released)
        self.saveButton.pressed.connect(self.saveButton_pressed)
        self.saveButton.released.connect(self.saveButton_released)
        self.uploadVidButton.pressed.connect(self.uploadVidButton_pressed)
        self.uploadVidButton.released.connect(self.uploadVidButton_released)
        self.countVidButton.pressed.connect(self.countVidButton_pressed)
        self.countVidButton.released.connect(self.countVidButton_released)
        self.extractFButton.pressed.connect(self.extractFButton_pressed)
        self.extractFButton.released.connect(self.extractFButton_released)
        self.trackButton.pressed.connect(self.trackButton_pressed)
        self.trackButton.released.connect(self.trackButton_released)
        self.playButton.pressed.connect(self.playButton_pressed)
        self.playButton.released.connect(self.playButton_released)
        self.stopButton.pressed.connect(self.stopButton_pressed)
        self.stopButton.released.connect(self.stopButton_released)
        self.selectButton.pressed.connect(self.selectButton_pressed)
        self.selectButton.released.connect(self.selectButton_released)
        self.unselectButton.pressed.connect(self.unselectButton_pressed)
        self.unselectButton.released.connect(self.unselectButton_released)
        self.nextFrameButton.pressed.connect(self.nextFrameButton_pressed)
        self.nextFrameButton.released.connect(self.nextFrameButton_released)
        self.backFrameButton.pressed.connect(self.backFrameButton_pressed)
        self.backFrameButton.released.connect(self.backFrameButton_released)
        self.saveImageButton.pressed.connect(self.saveImageButton_pressed)
        self.saveImageButton.released.connect(self.saveImageButton_released)
        self.addCellButton.pressed.connect(self.addCellButton_pressed)
        self.addCellButton.released.connect(self.addCellButton_released)
        self.graphButton.pressed.connect(self.graphButton_pressed)
        self.graphButton.released.connect(self.graphButton_released)
