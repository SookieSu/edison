#!/usr/bin/python
#coding=utf8

import os

def writeFile(path,filename,data):
    path_this = os.getcwd()
    os.chdir(path)
    mediaFile = open(filename,'w')
    mediaFile.write(data)
    mediaFile.close()
    os.chdir(path_this)

