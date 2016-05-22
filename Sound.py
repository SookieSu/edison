#!/usr/bin/python

import os
import sys
import time
import subprocess

import FileOperate
import Api

path_record = r"/home/root/sookie/record"
path_song = r"/home/root/sookie/song"
path_voice = r"/home/root/sookie/voice"


def playVoice():
    print('playVoice')
    fileName = FileOperate.getCurrentVoiceName(path_voice)
    FileOperate.getNextVoiceName(path_voice)
    print(fileName)
    #playMp3(path_voice,fileName)

def playLatestVoice():
    print('playLatestVoice')
    fileName = FileOperate.getLatestVoiceName(path_voice)
    FileOperate.getNextVoiceName(path_voice)
    print(fileName)
    #playMp3(path_voice,fileName)


def playSong():
    print('playSong')
    fileName = FileOperate.getCurrentSongName(path_song)
    print(fileName)
    #playMp3(path_song,fileName)

def pauseSong():
    print('pauseSong')
    cmd = "sh pause.sh"
    status = subprocess.Popen(cmd,shell=True)
    retFlag = status.wait()
    return retFlag


def playNextSong():
    print('playNextSong')
    fileName = FileOperate.getNextSongName(path_song)
    print(fileName)
    #playMp3(path_song,fileName)


def record():
    print('record')
    path = path_record
    fileName = "record-"+str(time.time())+".wav"
    retFlag = recordWav(path,fileName)
    time.sleep(1)
    if retFlag == 0:
        return fileName
    else:
        return None

def stopRecord():
    #kill the process arecord
    cmd = "ps | grep arecord | awk '{print $1}' | head -n 1 | xargs kill -9 "
    status = subprocess.Popen(cmd,shell=True)
    retFlag = status.wait()
    source_filename =  FileOperate.getLatestRecordName(path_record)
    source = source_filename.split('.')
    target_filename = source[0]+".amr"
    retFlag = wavToAmr(path_record,source_filename,target_filename)
    if retFlag == 0:
        FileOperate.deleteFile(path_record,source_filename)
        Api.setMessage('0',target_filename)
        return target_filename
    else:
        return False

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
    cmd = "arecord -f cd -t wav " + fileName + " &"
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

record()
time.sleep(10)
stopRecord()

'''

