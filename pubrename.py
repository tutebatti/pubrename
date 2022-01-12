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
#     - improve normalizing of filenames

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
        self.setGeometry(50, 500, 900, 600)
        self.move(50, 50)
        
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
    
    def closeEvent(self, event):
        
        self._closeEvince()
        
    def _createWidgets(self):
        
        self._createFileWidgets()
        self._createFilenameWidgets()
        self._createBibWidgets()
        self._createButtons()
        self._createFileButtons()
        
    def _createFileWidgets(self):

        self.fileWidgets = {}
        fileWidgetsLayout = QGridLayout()
        row = 0
        
        fileWidgets ={"currentDirectory": "Aktueller Pfad",
                      "currentFile": "Aktuelle Datei",
                      }
        
        for fileWidget, description in fileWidgets.items():
            self.fileWidgets[fileWidget] = [QLabel(description + ": "), QLineEdit()]
            fileWidgetsLayout.addWidget(self.fileWidgets[fileWidget][0], row, 0)
            fileWidgetsLayout.addWidget(self.fileWidgets[fileWidget][1], row, 1)
            row += 1
        
        self.generalLayout.addLayout(fileWidgetsLayout, 7, 0)
        
    def _createFilenameWidgets(self):

        self.filenameWidgets = {}
        filenameWidgetsLayout = QGridLayout()
        row = 0
        
        filenameWidgets ={"oldFilename": "Alter Dateiname",
                      "newFilename": "Neuer Dateiname",
                      }
           
        for filenameWidget, description in filenameWidgets.items():
            self.filenameWidgets[filenameWidget] = [QLabel(description + ": "), QLineEdit()]
            filenameWidgetsLayout.addWidget(self.filenameWidgets[filenameWidget][0], row, 0)
            filenameWidgetsLayout.addWidget(self.filenameWidgets[filenameWidget][1], row, 1)
            row += 1
        
        self.generalLayout.addLayout(filenameWidgetsLayout, 0, 0)        
                      
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
        
        self.generalLayout.addLayout(bibWidgetsLayout, 2, 0)

    def _createButtons(self):
        
        self.buttons = {}
        buttonsLayout = QGridLayout()
        
        buttons = {"preview": ["&Vorschau", self._preview, (0,0)],
                      "submit" : ["&Übernehmen", self._submit, (0,1)],
                      "submitAndOpenRandomFile" : ["Übernehmen und &nächste zufällige Datei", self._submitAndOpenRandomFile, (1,1)],
                      "normalizeOldFilename": ["&Alten Dateinamen normalisieren", self._normalizeOldFilename, (2,1)]}
        
        for button, attributes in buttons.items():
            self.buttons[button] = QPushButton(attributes[0])
            self.buttons[button].clicked.connect(attributes[1])
            buttonsLayout.addWidget(self.buttons[button], attributes[2][0], attributes[2][1])
        
        self.generalLayout.addLayout(buttonsLayout, 1, 0)
        
    def _createFileButtons(self):
        
        self.fileButtons = {}
        fileButtonsLayout = QGridLayout()
        
        fileButtons = {"choseDirectory" : ["Verzeichnis wählen", self._setPath, (0,0)],
                      "openRandomFile": ["Öffne &zufällige Datei", self._openRandomFile, (0,1)],
                      "openFile": ["Öffne bestimmte Datei", self._openFile, (1,1)],
                      "moveTo2edit": ["Verschiebe Datei nach &2edit", self._moveTo2edit, (2,1)],
                      }
        
        for fileButton, attributes in fileButtons.items():
            self.fileButtons[fileButton] = QPushButton(attributes[0])
            self.fileButtons[fileButton].clicked.connect(attributes[1])
            fileButtonsLayout.addWidget(self.fileButtons[fileButton], attributes[2][0], attributes[2][1])
        
        self.generalLayout.addLayout(fileButtonsLayout, 6, 0)
  
    def _clearFields(self):
        
        self._clearFilenameFields()
        self._clearBibFields()
  
    def _clearFilenameFields(self):
    
        for widget, elements in self.filenameWidgets.items():
            elements[1].clear()
  
    def _clearBibFields(self):
        
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
        
        self.file = self.directory + random.choice(os.listdir(self.directory))
        
        while self._checkFiletype() == False:
            self.file = self.directory + random.choice(os.listdir(self.directory))
        
        self.oldFilename = os.path.basename(self.file)
            
        self.fileWidgets["currentFile"][1].setText(self.file)
        self.filenameWidgets["oldFilename"][1].setText(self.oldFilename)
            
        self._openEvince()
    
    def _openFile(self):
        
        self.file = QFileDialog.getOpenFileName()[0]
        
        self.oldFilename = os.path.basename(self.file)
            
        self.fileWidgets["currentFile"][1].setText(self.file)
        self.filenameWidgets["oldFilename"][1].setText(self.oldFilename)
        
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
        
        self.newFilename = author + year + title + subtitle + addition + ".pdf"
    
        self.normalizeFilename()
        
        self.filenameWidgets["newFilename"][1].setText(self.newFilename)
        
    def _normalizeOldFilename(self):
        
        self.newFilename = self.oldFilename
        
        self.normalizeFilename()
        
        self.filenameWidgets["newFilename"][1].setText(self.newFilename)
    
    def normalizeFilename(self):
        
        replacementTable = [("-\n",""),
                            ("\n"," "),
                            (":"," "),
                            ("  "," "),
                            (" ","-"),
                            ("'","-"),
                            (",",""),
                            ("\"",""),
                            ]
        for pair in replacementTable:
            self.newFilename = self.newFilename.replace(pair[0], pair[1])
        
        self.newFilename = self.newFilename.casefold()
        
        self.newFilename = unidecode.unidecode(self.newFilename)
    
    def _moveTo2edit(self):
        
        if os.path.isdir(self.directory+"/2edit") == False:
            os.mkdir(self.directory+"/2edit")
            
        os.rename(self.file, self.directory+"/2edit/"+self.oldFilename)
        
        self._clearFields()
        
        self._closeEvince()
    
    def _submit(self):
        
        self.newFilename = self.filenameWidgets["newFilename"][1].text()
        
        if os.path.isdir(self.directory+"/renamed") == False:
            os.mkdir(self.directory+"/renamed")
        
        os.rename(self.file, self.directory+"/renamed/"+self.newFilename)
        
        self._clearFields()
        
        self._closeEvince()
        
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