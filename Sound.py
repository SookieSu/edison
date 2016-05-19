#!/usr/bin/python

import mraa as m
import random as rand
import subprocess

dev = m.Spi(0)

for x in range(0,10):
    txbuf = bytearray(4)
    for y in range(0,4):
        txbuf[y] = rand.randrange(0,256)
    rxbuf = dev.write(txbuf)
    if rxbuf != txbuf:
        print("we have an error captain!")
        break
        exit(1)

def amrToMp3(path,source,target):
    path_this = os.getcwd()
    os.chdir(path)
    cmd = "/usr/bin/ffmpeg -i " + source + " -ab 64k " + target
    subprocess.call(cmd,shell=True)
    os.chdir(path_this)
    return True

def wavToAmr(path,source,target):
    path_this = os.getcwd()
    os.chdir(path)
    cmd = "/usr/bin/ffmpeg -i " + source + " -ab 12.2k -ar 8000 -ac 1 "  + target
    subprocess.call(cmd,shell=True)
    os.chdir(path_this)
    return True

def playMp3(path,fileName):
    path_this = os.getcwd()
    os.chdir(path)
    cmd = "mpg123 " + fileName
    subprocess.call(cmd,shell=True)
    os.chdir(path_this)
    return True 

def recordWav(path,fileName):
    path_this = os.getcwd()
    os.chdir(path)
    cmd = "arecord -f cd -t wav " + fileName
    subprocess.call(cmd,shell=True)
    os.chdir(path_this)
    return True 


