#!/usr/bin/python

import os
import sys
import time
import subprocess

import FileOperate

path_record = r"/home/root/sookie/record"

def playRecord():
    print('playRecord')

def playSong():
    print('playSong')

def playNextSong():
    print('playNextSong')

def record():
    print('record')
    path = path_record
    fileName = "record-"+time.time()+".wav"
    retFlag = recordWav(path,fileName)
    if retFlag == 0:
        return fileName
    else:
        return None


def amrToMp3(path,source,target):
    path_this = os.getcwd()
    os.chdir(path)
    cmd = "/usr/bin/ffmpeg -i " + source + " -ab 64k " + target
    status = subprocess.Popen(cmd,shell=True)
    retFlag = status.wait()
    os.chdir(path_this)
    return retFlag

def wavToAmr(path,source,target):
    path_this = os.getcwd()
    os.chdir(path)
    cmd = "/usr/bin/ffmpeg -i " + source + " -ab 12.2k -ar 8000 -ac 1 "  + target
    status = subprocess.Popen(cmd,shell=True)
    retFlag = status.wait()
    os.chdir(path_this)
    return retFlag

def playMp3(path,fileName):
    path_this = os.getcwd()
    os.chdir(path)
    cmd = "mpg123 " + fileName
    status = subprocess.Popen(cmd,shell=True)
    retFlag = status.wait()
    time.sleep(2)
    os.chdir(path_this)
    return retFlag

def recordWav(path,fileName):
    path_this = os.getcwd()
    os.chdir(path)
    cmd = "arecord -f cd -t wav " + fileName
    status = subprocess.Popen(cmd,shell=True)
    retFlag = status.wait()
    time.sleep(2)
    os.chdir(path_this)
    return retFlag 


'''
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
'''

