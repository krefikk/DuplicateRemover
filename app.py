import sys
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon

class fileCleaner(QMainWindow):

    def __init__(self):

        super(fileCleaner, self).__init__()
        self.setWindowTitle("File Cleaner")
        self.setWindowIcon(QIcon("python.png"))
        #self.setGeometry(300, 300, 500, 500)

        uic.loadUi("dialog.ui", self)

        self.buttonRemoveDups = self.findChild(QPushButton, "pushButton")
        self.buttonReverse = self.findChild(QPushButton, "pushButton_2")
        self.label = self.findChild(QLabel, "label")

        self.buttonRemoveDups.clicked.connect(self.clickerRemoveDups)
        self.buttonReverse.clicked.connect(self.clickerReverse)
        
    
    def clickerRemoveDups(self):
        
        fname = QFileDialog.getOpenFileName(self, "Select the file you want to remove duplicate lines from.", "", "Text Files (*.txt)")

        try:   

            if fname:
                dupRemover(fname[0])
                self.label.setText("Duplicate lines in the " +fname[0]+ " file have been removed.")
        
        except FileNotFoundError:

            fileNotFound()

        except:

            errorOccured()


    def clickerReverse(self):
        fnameOriginal = QFileDialog.getOpenFileName(self, "Select the original file.", "", "Text Files (*.txt)")
        fnameChanged = QFileDialog.getOpenFileName(self, "Select the non-duplicate file you modified.", "", "Text Files (*.txt)")

        try:
            
            if fnameOriginal and fnameChanged:

                f1 = open(fnameOriginal[0], "r")
                f2 = open(fnameChanged[0], "r")

                f1list = f1.readlines()
                f2list = f2.readlines()

                if len(f1list) < len(f2list):

                    mismatchedFiles()
                
                dupReverser(self, fnameChanged[0], fnameOriginal[0])
                self.label.setText(fnameChanged[0] + " file reinstated by adding duplicate lines.")
        
        except FileNotFoundError:

            fileNotFound()

        except:

            errorOccured()
        
        
def dupRemover(file):
    
    input = open(file, "r")

    inputList = input.readlines()
    outputList = []

    for l in inputList:
        if l not in outputList:
            outputList.append(l)

    input.close()

    output = open("output.txt", "w")

    for element in outputList:

        output.write(element)

    output.close()


def dupRemoverWithoutFileOutput(file):
    
    input = open(file, "r")

    inputList = input.readlines()
    outputList = []

    for l in inputList:
        if l not in outputList:
            outputList.append(l)

    input.close()

    return outputList


def dupReverser(self, fileNoDup, fileOriginal):

    unrepeated = open(fileNoDup, "r")
    original = open(fileOriginal, "r")

    unrepeatedModifiedList = unrepeated.readlines()
    originalList = original.readlines()
    unrepeatedOriginalList = dupRemoverWithoutFileOutput(fileOriginal)

    unrepeated.close()
    original.close()

    lastList = [None] * len(originalList)

    j = 0
    for line in unrepeatedOriginalList:

        i = 0

        for originalline in originalList:

            if originalline == line:

                lastList[i] = unrepeatedModifiedList[j]

        
            i = i + 1

        j = j + 1

    newOriginal = open("last.txt", "w")

    for line in lastList:

        newOriginal.write(line)

    newOriginal.close()


def fileNotFound():

    errorMsg = QMessageBox()
    errorMsg.setIcon(QMessageBox.Critical)
    errorMsg.setText("File Not Found")
    errorMsg.setInformativeText("You have to choose a file.")
    errorMsg.setWindowTitle("Error")
    errorMsg.setWindowIcon(QIcon("error-icon.png"))
    errorMsg.exec_()

def mismatchedFiles():

    errorMsg = QMessageBox()
    errorMsg.setIcon(QMessageBox.Critical)
    errorMsg.setText("Wrong File")
    errorMsg.setInformativeText("First, you have to choose the original file and then the modified non-duplicate file.")
    errorMsg.setWindowTitle("Error")
    errorMsg.setWindowIcon(QIcon("error-icon.png"))
    errorMsg.exec_()

def errorOccured():

    errorMsg = QMessageBox()
    errorMsg.setIcon(QMessageBox.Critical)
    errorMsg.setText("An Error Occured")
    errorMsg.setInformativeText("Please reach me out from Github: 'krefikk'.")
    errorMsg.setWindowTitle("Error")
    errorMsg.setWindowIcon(QIcon("error-icon.png"))
    errorMsg.exec_()


def app():
    app = QApplication(sys.argv)
    window = fileCleaner()
    window.show()
    sys.exit(app.exec_())


app()
