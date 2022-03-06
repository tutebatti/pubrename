#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 22 19:27:46 2022

@author: florian

2do: double spaces are not removed
"""

import os
import sys
import unidecode

def normalize_pubfilename(original_filename):
    
    normalized_filename = original_filename.casefold()
    
    german_umlaute = [("ä", "ae"),
                     ("ö", "oe"),
                     ("ü", "ue"),
                     ]
    
    for pair in german_umlaute:
        normalized_filename = normalized_filename.replace(pair[0], pair[1])
    
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
                     "-\r",
                    ]
    
    for element in deletionTable:
        normalized_filename = normalized_filename.replace(element, "")
    
    normalized_filename = unidecode.unidecode(normalized_filename)

    replacementTable = [("\n"," "),
                        ("\r"," "),
                        ("-et-al","+al"),
                        ("‘","'"),
                        ("’","'"),
                        ("'","-"),
                        ("--","-"),
                        ("  "," "),
                        (" ","-")
                        ]
    
    for pair in replacementTable:
        normalized_filename = normalized_filename.replace(pair[0], pair[1])
    
    return normalized_filename

def evaluate_string(string):

    elements = ["  ","\n","\r"]

    if any (element in elements for substring in string):
        print("not clean")
    else:
        print("clean")

def main():

    original_filename, file_extension = os.path.splitext(sys.argv[1])

    new_filename = normalize_pubfilename(original_filename)

    new_file = new_filename+file_extension

    os.rename(sys.argv[1], new_file)

if __name__ == '__main__':
    main()
