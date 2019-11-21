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

def save(coordinates, file, file_no):
	fileName= file.split(".")[0]
	fileName = str(fileName) + "_Tracking_" + str(file_no) + ".txt"

	file = open(fileName, 'w')
	for item in coordinates:
		file.write("{0}\n".format(item))
	file.close()

