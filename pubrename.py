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
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QLineEdit, QPushButton, QGridLayout, QFileDialog

# needed for normalizing filename
import unidecode

# __version__ = "0.1"
# __author__ = "Florian Jäckel"

class pubrename(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Pubrename")
        self.setGeometry(200, 100, 800, 400)
        self.move(200, 100)
        self.layout = None
        
        # default directory to operate in
        self.directory = "./"
        # variables for handling of file
        self.file = ""
        self.oldFileName = ""
        self.fileExtension = ""
        self.newFileName = ""
        
        self._createWidgets()
        self._setLayout()
        
        self.show()

    def _createWidgets(self):
        
        self._createFileWidgets()
        self._createBibWidgets()
        self._createButtons()
        
    def _createFileWidgets(self):

        self.lbl_oldfilename = QLabel("Alter Dateiname: ", parent=self)
        self.ent_oldfilename = QLineEdit(parent=self)
        
        self.lbl_newfilename = QLabel("Neuer Dateiname: ", parent=self)
        self.ent_newfilename = QLineEdit(parent=self)
        
        self.lbl_directory = QLabel("Aktueller Pfad: ", parent=self)
        self.ent_directory = QLineEdit(parent=self)

        self.lbl_file = QLabel("Aktuelle Datei: ", parent=self)
        self.ent_file = QLineEdit(parent=self)

    def _createBibWidgets(self):        

        self.lbl_author = QLabel("Autor: ", parent=self)
        self.ent_author = QLineEdit(parent=self)

        self.lbl_year = QLabel("Jahr: ", parent=self)
        self.ent_year = QLineEdit(parent=self)

        self.lbl_title = QLabel("Titel: ", parent=self)
        self.ent_title = QLineEdit(parent=self)

        self.lbl_subtitle = QLabel("Untertitel (optional): ", parent=self)
        self.ent_subtitle = QLineEdit(parent=self)

        self.lbl_additions = QLabel("Zusatz (optional): ", parent=self)
        self.ent_additions = QLineEdit(parent=self)

    def _createButtons(self):

        self.btn_preview = QPushButton("Vorschau")
        self.btn_preview.clicked.connect(self.preview)

        self.btn_submit = QPushButton("Übernehmen")
        self.btn_submit.clicked.connect(lambda: self.submit())

        self.btn_submit_and_randomfile = QPushButton("Übernehmen und neue Datei")
        self.btn_submit_and_randomfile.clicked.connect(lambda: self.submit_and_randomfile())

        self.btn_chosedirectory = QPushButton("Verzeichnis wählen")
        self.btn_chosedirectory.clicked.connect(self.set_path)

        self.btn_randomfile = QPushButton("Öffne zufällige Datei")
        self.btn_randomfile.clicked.connect(self.open_random_file)

        self.btn_openfile = QPushButton("Öffne bestimmte Datei")
        self.btn_openfile.clicked.connect(self.open_file)        
        
    def _setLayout(self):
        
        self.layout = QGridLayout()
        
        self.layout.addWidget(self.lbl_oldfilename, 0, 0)
        self.layout.addWidget(self.ent_oldfilename, 0, 1, 1, 2)
        
        self.layout.addWidget(self.lbl_author, 1, 0)
        self.layout.addWidget(self.ent_author, 1, 1, 1, 2)
        
        self.layout.addWidget(self.lbl_year, 2, 0)
        self.layout.addWidget(self.ent_year, 2, 1, 1, 2)
        
        self.layout.addWidget(self.lbl_title, 3, 0)
        self.layout.addWidget(self.ent_title, 3, 1, 1, 2)
        
        self.layout.addWidget(self.lbl_subtitle, 4, 0)
        self.layout.addWidget(self.ent_subtitle, 4, 1, 1, 2)
        
        self.layout.addWidget(self.lbl_additions, 5, 0)
        self.layout.addWidget(self.ent_additions, 5, 1, 1, 2)
        
        self.layout.addWidget(self.btn_preview, 6, 1)
        self.layout.addWidget(self.btn_submit, 6, 2)
        
        self.layout.addWidget(self.btn_submit_and_randomfile, 7, 2)
        
        self.layout.addWidget(self.lbl_newfilename, 8, 0)
        self.layout.addWidget(self.ent_newfilename, 8, 1, 1, 2)
        
        self.layout.addWidget(self.btn_chosedirectory, 9, 1)
        self.layout.addWidget(self.btn_randomfile, 9, 2)
        self.layout.addWidget(self.btn_openfile, 10, 2)
        
        self.layout.addWidget(self.lbl_directory, 11, 0)
        self.layout.addWidget(self.ent_directory, 11, 1, 1, 2)
        
        self.layout.addWidget(self.lbl_file, 12, 0)
        self.layout.addWidget(self.ent_file, 12, 1, 1, 2)
        
    
    def clear_fields(self):
        
        self.ent_oldfilename.clear()
        self.ent_author.clear()
        self.ent_year.clear()
        self.ent_title.clear()
        self.ent_subtitle.clear()
        self.ent_additions.clear()
        self.ent_newfilename.clear()
        self.ent_file.clear()
    
    def set_path(self):
        
        self.directory = QFileDialog.getExistingDirectory()+"/"
    
        self.ent_directory.setText(self.directory)
    
    def check_filetype(self):
        """
        Check if file is pdf; returns boolean
        
        2do: Check if file is pdf, djvu, or epub; return boolean
    
        """
        accepted_filetypes = [".pdf"]#, ".djvu", ".djv", ".epub"]
        self.fileName, self.fileExtension = os.path.splitext(self.file)
        
        if (self.file_extension in accepted_filetypes):
            return True
        else:
            return False
        
    def open_random_file(self):
        
        self.file = self.directory + random.choice(os.listdir(self.directory))
        
        self.ent_file.setText(self.file)
        
        while self.check_filetype() == False:
            self.file = self.directory + random.choice(os.listdir(self.directory))
            
            self.ent_file.setText(self.file)
            
        self.handle_file()
    
    def open_file(self):
        
        self.file = QFileDialog.getOpenFileName()[0]
        
        self.handle_file()
    
    def handle_file(self):
        
        subprocess.Popen(["evince", self.file])
        time.sleep(0.75)
        subprocess.Popen(["xdotool", "key", "Super+Right"])
        time.sleep(0.1)
        subprocess.Popen(["xdotool", "key", "F9"])
        time.sleep(0.1)
        subprocess.Popen(["xdotool", "keydown", "Alt", "key", "Tab"])
        time.sleep(0.1)
        subprocess.Popen(["xdotool", "keyup", "Alt"])
        
        self.oldFileName, self.fileExtensionxtension = os.path.splitext(self.file)
        
        self.ent_oldfilename.setText(self.oldFileName)
    
    def preview(self):
        author = self.ent_author.text()
        author = author + "_"
    
        year = self.ent_year.text()
        year = year + "_"
        
        title = self.ent_title.text()
        
        subtitle = self.ent_subtitle.text()
    
        if not subtitle == "":
            subtitle = "_" + subtitle
    
        additions = self.ent_additions.text()
        
        if not additions == "":
            additions = "_" + additions
        
        self.newFileName = author + year + title + subtitle + additions + ".pdf"
    
        self.newFileName=self.newFileName.replace("-\n","")
        self.newFileName=self.newFileName.replace("\n"," ")
        self.newFileName=self.newFileName.replace(":"," ")
        self.newFileName=self.newFileName.replace("  "," ")
        self.newFileName=self.newFileName.replace(" ","-")
        self.newFileName=self.newFileName.replace(",","")
        self.newFileName=self.newFileName.replace("\"","")
        self.newFileName=self.newFileName.casefold()
        self.newFileName=unidecode.unidecode(self.newFileName)
        
        self.ent_newfilename.setText(self.newFileName)
        
    
    def submit(self):
        
        self.newFileName = self.ent_newfilename.text()
        
        if os.path.isdir(self.directory+"/renamed") == False:
            os.mkdir(self.directory+"/renamed")
        
        os.rename(self.file, self.directory+"/renamed/"+self.newFileName)
        
        self.clear_fields()
        
    def submit_and_randomfile(self):
        
        self.submit(self)
        
        self.open_random_file()
   
# Execute the main loop
def main():    
    app = QApplication(sys.argv)
    window = pubrename()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()