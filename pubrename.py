#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 18:24:03 2021

@author: florian
"""

# 2do:
#     - error handling
#         - when path is not set
#         - when opening concrete file and is not pdf
#         - handling for files other than pdf
#     - oo to the max: gui-elements as objects
#     - check for bugs...
#     - implement internal pdf display
#     - write about modal window
#     - close file when opening concrete file or next random file without submitting
#     - improve normalization of filename
#     - take care of dot when normalizing old filename

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# needed for delay when opening evince
import time
# needed to start evince
import subprocess
# needed for operations concerning files and folders
import os
# needed to choose random file
import random
# needed for handling of pyqt
import sys
# needed for pyqt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QVBoxLayout, QGroupBox, QFileDialog, QStatusBar, QMenu, QAction, QMessageBox
# needed for normalizing filename
import unidecode

class Pubrename(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # set window properties
        self.setWindowTitle("Pubrename")
        self.setGeometry(50, 500, 900, 600)
        self.move(50, 50)
        
        # set general layout and central widget
        self.generalLayout = QGridLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        
        # default directory to operate in
        # 2do: implement warning
        self.directory = ""
        
        # variables for handling of file
        self.file = ""
        self.fileExtension = ""
        self.oldFilename = ""
        self.newFilename = ""
        
        self._createMenuBar()
        self._createStatusBar()
        self._createBoxes()
        
    def _createMenuBar(self):
        
        menuBar = self.menuBar()
        self.setMenuBar(menuBar)
        
        fileMenu = QMenu("&Datei", self)
        menuBar.addMenu(fileMenu)
        
        choseFile = QAction("Öffne Datei", self)
        choseFile.triggered.connect(self._choseFile)
        fileMenu.addAction(choseFile)
        
        choseDirectory = QAction("Öffne Verzeichnis", self)
        choseDirectory.triggered.connect(self._setDirectory)
        fileMenu.addAction(choseDirectory)
        
        closeProgram = QAction("&Schließen", self)
        closeProgram.triggered.connect(self.close)
        fileMenu.addAction(closeProgram)
        
        aboutMenu = QAction("&Über", self)
        menuBar.addAction(aboutMenu)
        aboutMenu.triggered.connect(self._showAbout)
        
    def _showAbout(self):
        
        about = QMessageBox()
        about.setWindowTitle("Über Pubrename")
        about.setText("Dummy-Text")
        about.exec_()
    
    def _createStatusBar(self):
        statusBar = QStatusBar()
        self.setStatusBar(statusBar)
        self.statusBarLabel = QLabel()
        statusBar.addWidget(self.statusBarLabel)
        
    def _createBoxes(self):
        
        self._createFormBoxes()
        self._createButtonBoxes()
        
    def _createButtonBoxes(self):
        
        self.filenameButtons = {"preview": ["&Vorschau", self._preview, (0,0)],
                      "normalizeOldFilename": ["&Alten Dateinamen normalisieren", self._normalizeOldFilename, (1,0)],
                      }
        
        self.fileButtons = {
                      "submit" : ["&Übernehmen", self._submit, (0,0)],
                      "submitAndOpenRandomFile" : ["Übernehmen und &nächste zufällige Datei", self._submitAndOpenRandomFile, (1,0)],
                      "openRandomFile" : ["Nächste zufällige Datei", self._openRandomFile, (0,1)],
                      "moveTo2edit": ["Verschiebe Datei nach &2edit", self._moveTo2edit, (1,1)],
                      }
        
        self.filenameButtonBox = buttonBox(self.filenameButtons)
        self.fileButtonBox = buttonBox(self.fileButtons)

        self.generalLayout.addLayout(self.filenameButtonBox.layout, 1, 0)        
        self.generalLayout.addLayout(self.fileButtonBox.layout, 3, 0)        
        
    def _createFormBoxes(self):
              
        self.bibWidgets = {"author": "Autor/Hrsg.",
                      "year" : "Jahr",
                      "title" : "Titel",
                      "subtitle": "Untertitel (optional)",
                      "addition": "Zusatz (optional)",
                      }
        
        self.filenameWidgets = {"oldFilename": "Alter Dateiname",
                      "newFilename" : "Neuer Dateiname",
                      }
        
        self.bibBox = formBox("Bibliographische Angaben", self.bibWidgets)
        self.filenameBox = formBox("Dateinamen", self.filenameWidgets)
                
        self.generalLayout.addLayout(self.bibBox.layout, 0, 0)
        self.generalLayout.addLayout(self.filenameBox.layout, 2, 0)
        
    def closeEvent(self, event):
            
        self._closeEvince()
        
    def _clearAllFields(self):
        
        self.bibBox.clearFields()
        self.filenameBox.clearFields()
    
    def _setDirectory(self):
        
        self.directory = QFileDialog.getExistingDirectory()+"/"
        
        self.statusBarLabel.setText("Aktuelles Verzeichnis: " + self.directory)
    
    def _checkFiletype(self):
        acceptedFiletypes = [".pdf"]
        self.filename, self.fileExtension = os.path.splitext(self.file)
        
        if (self.fileExtension in acceptedFiletypes):
            return True
        else:
            return False
        
    def _choseFile(self):
        
        self.file = QFileDialog.getOpenFileName()[0]
        
        self.statusBarLabel.setText("Aktuelle Datei: " + self.file)
        
        self._openFile()
    
    def _openRandomFile(self):
        
        self.file = self.directory + random.choice(os.listdir(self.directory))
        
        while self._checkFiletype() == False:
            self.file = self.directory + random.choice(os.listdir(self.directory))
        
        self._openFile()
    
    def _openFile(self):
        
        self.oldFilename = os.path.basename(self.file)
        
        self.filenameBox.formList["oldFilename"][1].setText(self.oldFilename)
        
        self._openEvince()
    
    def _openEvince(self):
        
        self.evincePreview = subprocess.Popen(["evince", self.file])#, preexec_fn=os.setsid)
        time.sleep(0.75)
        subprocess.Popen(["xdotool", "key", "Super+Right"])
        time.sleep(0.1)
        subprocess.Popen(["xdotool", "key", "F9"])
        time.sleep(0.1)
        subprocess.Popen(["xdotool", "keydown", "Alt", "key", "Tab"])
        time.sleep(0.1)
        subprocess.Popen(["xdotool", "keyup", "Alt"])
        
    def _closeEvince(self):
        
        self.evincePreview.terminate()
    
    def _preview(self):
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
    
        self.normalizeFilename()
        
        self.newFilename = self.newFilename + ".pdf"
        
        self.filenameBox.formList["newFilename"][1].setText(self.newFilename)
        
    def _normalizeOldFilename(self):
        
        self.newFilename = self.oldFilename
        
        self.normalizeFilename()
        
        self.filenameBox.formList["newFilename"][1].setText(self.newFilename)
    
    def normalizeFilename(self):
        
        self.newFilename = self.newFilename.casefold()
        
        germanUmlaute = [("ä", "ae"),
                         ("ö", "oe"),
                         ("ü", "ue"),
                         ]
        
        for pair in germanUmlaute:
            self.newFilename = self.newFilename.replace(pair[0], pair[1])
        
        deletionTable = ['"',
                         "“",
                         "”",
                         "„",
                         "«",
                         "»",
                         "‹",
                         "›",
                         ",",
                         ".",
                         "?",
                         ":",
                         ";",
                         "!",
                         "-\n",
                        ]
        
        for element in deletionTable:
            self.newFilename = self.newFilename.replace(element, "")
        
        replacementTable = [("\n"," "),
                            ("‘","'"),
                            ("’","'"),
                            ("'","-"),
                            ("--","-"),
                            ("  "," "),
                            (" ","-")
                            ]
        
        for pair in replacementTable:
            self.newFilename = self.newFilename.replace(pair[0], pair[1])
        
        self.newFilename = unidecode.unidecode(self.newFilename)
    
    def _moveTo2edit(self):
        
        if os.path.isdir(self.directory+"/2edit") == False:
            os.mkdir(self.directory+"/2edit")
            
        os.rename(self.file, self.directory+"/2edit/"+self.oldFilename)
        
        self._clearAllFields()
        
        self._closeEvince()
    
    def _submit(self):
        
        self.newFilename = self.filenameBox.formList["newFilename"][1].text()
        
        if os.path.isdir(self.directory+"/renamed") == False:
            os.mkdir(self.directory+"/renamed")
        
        os.rename(self.file, self.directory+"/renamed/"+self.newFilename)
        
        self._clearAllFields()
        
        self._closeEvince()
        
    def _submitAndOpenRandomFile(self):
        
        self._submit()
        
        self._openRandomFile()
        
class formBox(QWidget):
    
    def __init__(self, boxName, formList):
        super().__init__()
        
        self.layout = QVBoxLayout()
        
        box = QGroupBox(boxName)
        boxLayout = QVBoxLayout()
        box.setLayout(boxLayout)
        
        self.formList = {}
        
        for name, description in formList.items():
            self.formList[name] = [QLabel(description+": "), QLineEdit()]
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