#!/usr/bin/python
#coding=utf8

import os
import json

'''
write file 
@param string path
@param string filename
@param binary data
'''
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
        return True

'''
read file 
@param string path
@param string filename
@return string data
'''
def readFile(path,filename):
    path_this = os.getcwd()
    os.chdir(path)
    data = None
    try: 
        mediaFile = open(filename,'r')
        data = mediaFile.read()
        mediaFile.close()
    except Exception,e:
        e = sys.exc_info()[0]  #Get exception info (optional)
        print 'ERROR:',e  #Print exception info (optional)
    finally:
        os.chdir(path_this)
        return data

'''
delete file 
@param string path
@param string filename
@return bool
'''
def deleteFile(path,filename):
    try:
        if os.path.exists(path + '/' + filename):
            os.remove(path + '/' + filename)
            return True
        else:
            return False
    except Exception,e:
        print e

'''
mark song name after write song file
@param string path
@param string songName
@param int songID
'''
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
        else:
            songNameDict = json.loads(data)
            print (songNameDict)
            #use songID to unique a song
            if songID in songNameDict:
                print (songID + ' already in list!')
            else:
                songNameDict[songID] = songName
                songNameFile.close()
                songNameFile = open('songName','w')
                json.dump(songNameDict,songNameFile,indent=2)
    except Exception,e:
        print e
    finally:
        os.chdir(path_this)
        return True

'''
update file "songName"
@param string path
@param string songID
@return bool
'''
def deleteSongName(path,songID):
    path_this = os.getcwd()
    os.chdir(path)
    try:
        songNameFile = open('songName','r+')
        data = songNameFile.read()
        if data == '':
            print('songName is empty')
        else:
            songNameDict = json.loads(data)
            #print (songNameDict)
            #use songID to unique a song
            if songID not in songNameDict:
                print(songID + ' not in list!')
            else:
                songName = songNameDict.pop(songID)
                print('delete song success : ' + songID)
                songNameFile.close()
                songNameFile = open('songName','w')
                json.dump(songNameDict,songNameFile,indent=2)
    except Exception,e:
        print e
    finally:
        os.chdir(path_this)
        return True

'''
write log
@param string path
@param string data
@return bool
'''
def writeLog(path,data):
    path_this = os.getcwd()
    os.chdir(path)
    filename = 'sookiesu.log'
    ret = True
    try:
        logFile = open(filename,'a+')
        logFile.write(data)
        logFile.write('\n')
        logFile.close()
    except Exception,e:
        e = sys.exc_info()[0]  #Get exception info (optional)
        print 'ERROR:',e  #Print exception info (optional)
        ret = False
    finally:
        os.chdir(path_this)
        return ret


