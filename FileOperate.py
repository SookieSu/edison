#!/usr/bin/python
#coding=utf8

import os
import json

def writeFile(path,filename,data):
    path_this = os.getcwd()
    os.chdir(path)
    try: 
        mediaFile = open(filename,'w')
        mediaFile.write(data)
        mediaFile.close()
    except Exception,e:
        e = sys.exc_info()[0]  #Get exception info (optional)
        print 'ERROR:',e  #Print exception info (optional)
    finally:
        os.chdir(path_this)

def writeSongName(path,songName,songID):
    path_this = os.getcwd()
    os.chdir(path)
    try:
        songNameFile = open('songName','r+')
        data = songNameFile.read()
        if data == '':
            songNameDict = {}
            songNameDict[songID] = songName
            json.dump(songNameDict,songNameFile,indent=2)
            return True
        else:
            songNameDict = json.loads(data)
            print (songNameDict)
            if songID in songNameDict:
                print ('already in list!')
                return False
            else:
                songNameDict[songID] = songName
                songNameFile.close()
                songNameFile = open('songName','w')
                json.dump(songNameDict,songNameFile,indent=2)
                return True
    except Exception,e:
        print e
    finally:
        os.chdir(path_this)

