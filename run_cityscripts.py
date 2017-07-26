#!/usr/bin/env python
#coding=utf-8

import sys
import os
import subprocess


print "starting scraping scripts"

#path for location of city scripts
path = sys.argv[1]

#run all of the python files in this directory so that the csv's are up to date
    py_file = os.path.join(path, py_file)
    if "city.py" in py_file:
        os.system("python '{0}'".format(py_file))
        print py_file


