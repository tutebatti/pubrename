#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: tutebatti
"""

# 2do:
#     - improve error handling
#     - handling for files other than pdf
#     - check for bugs...
#     - implement internal pdf display

import time  # for delay when opening evince
import subprocess  # for starting and closing evince
import os  # for operations concerning files and folders
import random  # for choosing random file
from normalize_pubfilename import normalize_pubfilename as normpfn  # custom script for normalizing filename

# for pyqt GUI
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, \
    QVBoxLayout, QGroupBox, QFileDialog, QStatusBar, QMenu, QAction, QMessageBox

class Pubrename(QMainWindow):
    def __init__(self):
        super().__init__()

        # set window properties
        self.setWindowTitle("Pubrename")
        self.setGeometry(50, 500, 960, 500) # adapt to be flexible for any resolution
        self.move(0, 0)

        # set general layout and central widget
        self.generalLayout = QGridLayout()
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.centralWidget.setLayout(self.generalLayout)

        self.createMenuBar()
        self.createStatusBar()
        self.createBoxes()

        # variable to check if evince is running
        self.evinceRunning = False

    def closeEvent(self, event):
        self.closeEvince()

    def clearAllFields(self):
        self.bibBox.clearFields()
        self.filenameBox.clearFields()

    ### handle old file

    def setDirectory(self):
        self.directory = QFileDialog.getExistingDirectory() + "/"
        self.updateStatusBar(self.directory)

    def createFileVariables(self):

        self.baseName = os.path.basename(self.fullPath)
        self.oldFilename, self.fileExtension = os.path.splitext(self.baseName)

    def checkFiletype(self):

        self.createFileVariables()

        acceptedFiletypes = [".pdf"]

        if (self.fileExtension in acceptedFiletypes):
            return True
        else:
            return False

    def showFileTypeError(self):

        wrongFiletype = QMessageBox()
        wrongFiletype.setWindowTitle("Fehler")
        wrongFiletype.setText("Keine pdf-Datei!")
        wrongFiletype.setIcon(QMessageBox.Warning)
        wrongFiletype.setStandardButtons(QMessageBox.Ok)
        wrongFiletype.exec_()
        self.fullPath = QFileDialog.getOpenFileName()[0]

    def openFile(self):

        self.filenameBox.formList["oldFilename"][1].setText(self.oldFilename + self.fileExtension)
        self.openEvince()

    def openIndividualFile(self):

        self.closeOldEvince()

        self.fullPath = QFileDialog.getOpenFileName()[0]

        while self.checkFiletype() == False:
            self.showFileTypeError()

        self.directory = os.path.dirname(self.fullPath) + "/"

        self.openFile()

    def openRandomFile(self):

        self.closeOldEvince()

        if self.directory == "":
            noDirectoryError = QMessageBox()
            noDirectoryError.setWindowTitle("Fehler")
            noDirectoryError.setText("Es wurde noch kein Verzeichnis ausgewählt.")
            noDirectoryError.setIcon(QMessageBox.Warning)
            noDirectoryError.setStandardButtons(QMessageBox.Ok)
            noDirectoryError.exec_()
            self.setDirectory()

        self.fullPath = self.directory + random.choice(os.listdir(self.directory))

        while self.checkFiletype() == False:
            self.fullPath = self.directory + random.choice(os.listdir(self.directory))

        self.openFile()

    ### handling of evince-preview

    def openEvince(self):

        self.evincePreview = subprocess.Popen(["evince", self.fullPath])  # , preexec_fn=os.setsid)
        time.sleep(0.75)
        subprocess.Popen(["xdotool", "keydown", "Super"]),
        time.sleep(0.1)
        subprocess.Popen(["xdotool", "key", "Right"])
        time.sleep(0.1)
        subprocess.Popen(["xdotool", "keyup", "Super"]),
        #time.sleep(0.1)
        #subprocess.Popen(["xdotool", "key", "F9"])
        #time.sleep(0.2)
        #subprocess.Popen(["xdotool", "key", "Alt+Tab"])
        #subprocess.Popen(["xdotool", "keydown", "Alt", "key", "Tab"])
        #time.sleep(0.2)
        #subprocess.Popen(["xdotool", "keyup", "Alt"])

        self.evinceRunning = True

    def closeEvince(self):

        self.evincePreview.terminate()

    def closeOldEvince(self):
        if self.evinceRunning:
            self.closeEvince()

    ### handling of newFilename

    def preview(self):
        author = self.bibBox.formList["author"][1].text()
        author = author + "_"

        year = self.bibBox.formList["year"][1].text()
        year = year + "_"

        title = self.bibBox.formList["title"][1].text()

        subtitle = self.bibBox.formList["subtitle"][1].text()
        if not subtitle == "":
            subtitle = "_" + subtitle

        addition = self.bibBox.formList["addition"][1].text()
        if not addition == "":
            addition = "_" + addition

        self.newFilename = author + year + title + subtitle + addition
        self.newFilename = normpfn(self.newFilename)

        self.newFilename = self.newFilename + self.fileExtension
        self.filenameBox.formList["newFilename"][1].setText(self.newFilename)

    def normalizeOldFilename(self):

        self.newFilename = normpfn(self.oldFilename)
        self.filenameBox.formList["newFilename"][1].setText(self.newFilename + self.fileExtension)

    ### moving and renaming file

    def moveTo2edit(self):

        if os.path.isdir(self.directory + "2edit") == False:
            os.mkdir(self.directory + "2edit")

        os.rename(self.fullPath, self.directory + "2edit/" + self.oldFilename + self.fileExtension)

        self.clearAllFields()
        self.closeEvince()

    def moveToTrash(self):

        if os.path.isdir(self.directory + "deleted") == False:
            os.mkdir(self.directory + "deleted")

        os.rename(self.fullPath, self.directory + "deleted/" + self.oldFilename + self.fileExtension)

        self.clearAllFields()
        self.closeEvince()

    def submit(self):

        self.newFilename = self.filenameBox.formList["newFilename"][1].text()

        if os.path.isdir(self.directory + "renamed") == False:
            os.mkdir(self.directory + "renamed")

        os.rename(self.fullPath, self.directory + "renamed/" + self.newFilename)

        self.clearAllFields()
        self.closeEvince()

    def submitAndOpenRandomFile(self):

        self.submit()
        self.openRandomFile()

    ### methods creating gui

    def createMenuBar(self):

        menuBar = self.menuBar()
        self.setMenuBar(menuBar)

        fileMenu = QMenu("&Datei", self)
        menuBar.addMenu(fileMenu)

        choseFile = QAction("Öffne Datei", self)
        choseFile.triggered.connect(self.openIndividualFile)
        fileMenu.addAction(choseFile)

        choseDirectory = QAction("Wähle Verzeichnis", self)
        choseDirectory.triggered.connect(self.setDirectory)
        fileMenu.addAction(choseDirectory)

        closeProgram = QAction("&Schließen", self)
        closeProgram.triggered.connect(self.close)
        fileMenu.addAction(closeProgram)

        aboutMenu = QAction("&Über", self)
        menuBar.addAction(aboutMenu)
        aboutMenu.triggered.connect(self.showAbout)

    def showAbout(self):

        about = QMessageBox()
        about.setWindowTitle("Über Pubrename")
        about.setText("Dieses Programm erleichtert die Umbenennung\nvon Publikationen im Format von pdf.\n\n (c) Florian Jäckel (tutebatti), 2022")
        about.exec_()

    def createStatusBar(self):
        statusBar = QStatusBar()
        self.setStatusBar(statusBar)
        self.statusBarLabel = QLabel()
        statusBar.addWidget(self.statusBarLabel)

    def updateStatusBar(self, directory):

        self.statusBarLabel.setText("Aktuelles Verzeichnis: " + directory)

    def createBoxes(self):

        self.createFormBoxes()
        self.createButtonBoxes()

    def createButtonBoxes(self):

        self.filenameButtons = {
            "preview": ["&Vorschau", self.preview, (0, 0)],
            "normalizeOldFilename": ["&Alten Dateinamen normalisieren", self.normalizeOldFilename, (1, 0)],
        }

        self.fileButtons = {
            "submit": ["&Übernehmen", self.submit, (0, 0)],
            "submitAndOpenRandomFile": ["Übernehmen und &nächste zufällige Datei", self.submitAndOpenRandomFile,
                                        (0, 1)],
            "openRandomFile": ["Nächste zufällige Datei", self.openRandomFile, (1, 0)],
            "moveTo2edit": ["Verschiebe Datei nach &2edit", self.moveTo2edit, (2, 0)],

            "moveToTrash": ["Verschiebe Datei nach &deleted", self.moveToTrash, (2, 1)],
        }

        self.filenameButtonBox = buttonBox(self.filenameButtons)
        self.fileButtonBox = buttonBox(self.fileButtons)

        self.generalLayout.addLayout(self.filenameButtonBox.layout, 1, 0)
        self.generalLayout.addLayout(self.fileButtonBox.layout, 3, 0)

    def createFormBoxes(self):

        self.bibWidgets = {"author": "Autor/Hrsg.",
                           "year": "Jahr",
                           "title": "Titel",
                           "subtitle": "Untertitel (optional)",
                           "addition": "Zusatz (optional)",
                           }

        self.filenameWidgets = {"oldFilename": "Alter Dateiname",
                                "newFilename": "Neuer Dateiname",
                                }

        self.bibBox = formBox("Bibliographische Angaben", self.bibWidgets)
        self.filenameBox = formBox("Dateinamen", self.filenameWidgets)

        self.generalLayout.addLayout(self.bibBox.layout, 0, 0)
        self.generalLayout.addLayout(self.filenameBox.layout, 2, 0)


class formBox(QWidget):

    def __init__(self, boxName, formList):
        super().__init__()

        self.layout = QVBoxLayout()

        box = QGroupBox(boxName)
        boxLayout = QVBoxLayout()
        box.setLayout(boxLayout)

        self.formList = {}

        for name, description in formList.items():
            self.formList[name] = [QLabel(description + ": "), QLineEdit()]
            boxLayout.addWidget(self.formList[name][0])
            boxLayout.addWidget(self.formList[name][1])

        self.layout.addWidget(box)

    def clearFields(self):

        for widget, elements in self.formList.items():
            elements[1].clear()


class buttonBox(QWidget):
    def __init__(self, buttonList):
        super().__init__()

        self.layout = QVBoxLayout()

        box = QWidget()
        boxLayout = QGridLayout()
        box.setLayout(boxLayout)

        self.buttonList = {}

        for button, attributes in buttonList.items():
            self.buttonList[button] = QPushButton(attributes[0])
            self.buttonList[button].clicked.connect(attributes[1])
            boxLayout.addWidget(self.buttonList[button], attributes[2][0], attributes[2][1])

        self.layout.addWidget(box)


def main():
    pubrename = QApplication(sys.argv)
    view = Pubrename()
    view.show()
    # Execute the main loop
    sys.exit(pubrename.exec_())


if __name__ == '__main__':
    main()
