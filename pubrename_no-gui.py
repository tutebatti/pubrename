#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 18:24:03 2021

@author: florian
"""

import time
import os
import sys
import subprocess

subprocess.Popen(["evince", sys.argv[1]])
time.sleep(0.75)
subprocess.Popen(["xdotool", "key", "Super+Right"])
time.sleep(0.1)
subprocess.Popen(["xdotool", "key", "F9"])
time.sleep(0.1)
subprocess.Popen(["xdotool", "keydown", "Alt", "key", "Tab"])
time.sleep(0.1)
subprocess.Popen(["xdotool", "keyup", "Alt"])

old_file_name, file_extension = os.path.splitext(sys.argv[1])

print("Angaben werden eingelesen.")

author=input("Autor/Hrsg: ")

author=author+"_"

year=input("Jahr: ")

year=year+"_"

title=input("Titel: ")

subtitle=input("Untertitel (optional): ")

if not subtitle == "":

    subtitle="_"+subtitle

additions=input("Zusätze (optional): ")

if not additions == "":

    additions="_"+additions

new_file_name=author+year+title+subtitle+additions+file_extension

new_file_name=new_file_name.replace("-\n","")
new_file_name=new_file_name.replace("\n"," ")
new_file_name=new_file_name.replace("  "," ")
new_file_name=new_file_name.replace(" ","-")
new_file_name=new_file_name.replace(",","")
new_file_name=new_file_name.replace("\"","")

os.rename(sys.argv[1],new_file_name)

os.system("pkill evince")