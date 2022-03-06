#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

def evaluate_string(string):

    elements = ["  ","\n","\r"]

    if any elements in string:
        print("not clean")
    else:
        print("clean")

def main():
    evaluate_string(sys.argv[1])

if __name__ == '__main__':
    main()
