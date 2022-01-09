#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 18:24:03 2021

@author: florian
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
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QFileDialog
# needed for normalizing filename
import unidecode

class Pubrename(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # set window properties
        self.setWindowTitle("Pubrename")
        self.setGeometry(200, 100, 800, 400)
        self.move(200, 100)
        
        # set general layout and central widget
        self.generalLayout = QGridLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        
        # default directory to operate in
        # 2do: implement warning
        self.directory = "./"
        
        # variables for handling of file
        self.file = ""
        self.fileExtension = ""
        self.oldFilename = ""
        self.newFilename = ""
        
        self._createWidgets()
        
    def _createWidgets(self):
        
        self._createFileWidgets()
        self._createBibWidgets()
        self._createButtons()
        
    def _createFileWidgets(self):

        self.fileWidgets = {}
        fileWidgetsLayout = QGridLayout()
        row = 0
        
        fileWidgets ={"oldFilename": "Alter Dateiname",
                      "newFilename": "Neuer Dateiname",
                      "currentDirectory": "Aktueller Pfad",
                      "currentFile": "Aktuelle Datei",
                      }
        
        
        
        for fileWidget, description in fileWidgets.items():
            self.fileWidgets[fileWidget] = [QLabel(description + ": "), QLineEdit()]
            fileWidgetsLayout.addWidget(self.fileWidgets[fileWidget][0], row, 0)
            fileWidgetsLayout.addWidget(self.fileWidgets[fileWidget][1], row, 1)
            row += 1
        
        self.generalLayout.addLayout(fileWidgetsLayout, 0, 0)
                      
    def _createBibWidgets(self):        

        self.bibWidgets = {}
        bibWidgetsLayout = QGridLayout()
        row=0
        
        bibWidgets = {"author": "Autor",
                      "year" : "Jahr",
                      "title" : "Titel",
                      "subtitle": "Untertitel (optional)",
                      "addition": "Zusatz (optional)"
                      }
        
        for bibWidget, description in bibWidgets.items():
            self.bibWidgets[bibWidget] = [QLabel(description + ": "), QLineEdit()]
            bibWidgetsLayout.addWidget(self.bibWidgets[bibWidget][0], row, 0)
            bibWidgetsLayout.addWidget(self.bibWidgets[bibWidget][1], row, 1)
            row += 1
        
        self.generalLayout.addLayout(bibWidgetsLayout, 1, 0)

    def _createButtons(self):
        
        self.buttons = {}
        buttonsLayout = QGridLayout()
        row=0
        
        buttons = {"preview": ["&Vorschau", self._preview],
                      "submit" : ["&Übernehmen", self._submit],
                      "submitAndOpenRandomFile" : ["Übernehmen und &nächste zufällige Datei", self._submitAndOpenRandomFile],
                      "choseDirectory" : ["Verzeichnis wählen", self._setPath],
                      "openRandomFile": ["Öffne zufällige Datei", self._openRandomFile],
                      "openFile": ["Öffne bestimmte Datei", self._openFile]
                      }
        
        for button, attributes in buttons.items():
            self.buttons[button] = QPushButton(attributes[0])
            self.buttons[button].clicked.connect(attributes[1])
            buttonsLayout.addWidget(self.buttons[button], row, 0)
            row += 1
        
        self.generalLayout.addLayout(buttonsLayout, 2, 0)
  
    def _clearFields(self):
        
        for widget, elements in self.fileWidgets.items():
            elements[1].clear()
        for widget, elements in self.bibWidgets.items():
            elements[1].clear()
    
    def _setPath(self):
        
        self.directory = QFileDialog.getExistingDirectory()+"/"
    
        self.fileWidgets["currentDirectory"][1].setText(self.directory)
    
    def _checkFiletype(self):
        acceptedFiletypes = [".pdf"]
        self.fileName, self.fileExtension = os.path.splitext(self.file)
        
        if (self.fileExtension in acceptedFiletypes):
            return True
        else:
            return False
        
    def _openRandomFile(self):
        
        self.File = self.directory + random.choice(os.listdir(self.directory))
        
        self.fileWidgets["currentFile"][1].setText(self.file)
        
        while self._checkFiletype() == False:
            self.file = self.directory + random.choice(os.listdir(self.directory))
            
            self.fileWidgets["currentFile"][1].setText(self.file)
            
        self.handleFile()
    
    def _openFile(self):
        
        self.file = QFileDialog.getOpenFileName()[0]
        
        self.handleFile()
    
    def handleFile(self):
        
        subprocess.Popen(["evince", self.file])
        time.sleep(0.75)
        subprocess.Popen(["xdotool", "key", "Super+Right"])
        time.sleep(0.1)
        subprocess.Popen(["xdotool", "key", "F9"])
        time.sleep(0.1)
        subprocess.Popen(["xdotool", "keydown", "Alt", "key", "Tab"])
        time.sleep(0.1)
        subprocess.Popen(["xdotool", "keyup", "Alt"])
        
        self.oldFileName, self.fileExtension = os.path.splitext(self.file)
        
        self.fileWidgets["oldFilename"][1].setText(self.file)
    
    def _preview(self):
        author = self.bibWidgets["author"][1].text()
        author = author + "_"
    
        year = self.bibWidgets["year"][1].text()
        year = year + "_"
        
        title = self.bibWidgets["title"][1].text()
        
        subtitle = self.bibWidgets["subtitle"][1].text()
    
        if not subtitle == "":
            subtitle = "_" + subtitle
    
        addition = self.bibWidgets["addition"][1].text()
        
        if not addition == "":
            addition = "_" + addition
        
        self.newFileName = author + year + title + subtitle + addition + ".pdf"
    
        replacementTable = [("-\n",""),
                            ("\n"," "),
                            (":"," "),
                            ("  "," "),
                            (" ","-"),
                            (",",""),
                            ("\"",""),
                            ]
        for pair in replacementTable:
            self.newFileName=self.newFileName.replace(pair[0], pair[1])
        
        self.newFileName=self.newFileName.casefold()
        
        self.newFileName=unidecode.unidecode(self.newFileName)
        
        self.fileWidgets["newFilename"][1].setText(self.newFileName)
        
    
    def _submit(self):
        
        self.newFileName = self.fileWidgets["newFilename"][1].text()
        
        if os.path.isdir(self.directory+"/renamed") == False:
            os.mkdir(self.directory+"/renamed")
        
        os.rename(self.file, self.directory+"/renamed/"+self.newFileName)
        
        self._clearFields()
        
    def _submitAndOpenRandomFile(self):
        
        self._submit()
        
        self._openRandomFile()
   

def main():    
    pubrename = QApplication(sys.argv)
    view = Pubrename()
    view.show()
    # Execute the main loop
    sys.exit(pubrename.exec_())

if __name__ == '__main__':
    main()