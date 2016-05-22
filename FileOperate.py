#!/usr/bin/python
#coding=utf8

import os
import subprocess
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
            songNameDict['songIDList'] = []
            songNameDict['songList'] = {}
            songNameDict['songNum'] = 0
            songNameDict['currentSong'] = 0
            
            songNameDict['songIDList'].append(songID)
            songNameDict['songList'][songID] = songName
            songNameDict['songNum'] += 1
            json.dump(songNameDict,songNameFile,indent=2)
        else:
            songNameDict = json.loads(data)
            print (songNameDict)
            #use songID to unique a song
            if songID in songNameDict['songList']:
                print (songID + ' already in list!')
            else:
                songNameDict['songIDList'].append(songID)
                songNameDict['songList'][songID] = songName
                songNameDict['songNum'] += 1
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
            #use songID to unique a song
            if songID not in songNameDict['songList']:
                print(songID + ' not in list!')
            else:
                songNameDict['songIDList'].remove(songID)
                songName = songNameDict['songList'].pop(songID)
                songNameDict['songNum'] -= 1
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
mark "voiceList" after save the voice from wechat
@param string path
@param string fileName
@return bool
'''
def writeVoiceList(path,fileName):
    path_this = os.getcwd()
    os.chdir(path)
    try:
        voiceListFile = open('voiceList','r+')
        data = voiceListFile.read()
        if data == '':
        
            voiceListDict = {}
            voiceListDict['voiceList'] = []
            voiceListDict['voiceNum'] = 0
            voiceListDict['currentVoice'] = 0

            voiceListDict['voiceList'].append(fileName)
            voiceListDict['voiceNum'] += 1
            json.dump(voiceListDict,voiceListFile,indent=2)
        else:
        
            voiceListDict = json.loads(data)
            if fileName in voiceListDict['voiceList']:
                print(fileName + ' already in list!')
            else:
                voiceListDict['voiceList'].append(fileName)
                voiceListDict['voiceNum'] += 1
                voiceListFile.close()
                voiceListFile = open('voiceList','w')
                json.dump(voiceListDict,voiceListFile,indent=2)
    except Exception,e:
        print e
    finally:
        os.chdir(path_this)
        return True

'''
mark "voiceList" after save the voice from wechat
@param string path
@param string fileName
@return bool
'''
def deleteVoiceList(path,fileName):
    path_this = os.getcwd()
    os.chdir(path)
    try:
        voiceListFile = open('voiceList','r+')
        data = voiceListFile.read()
        if data == '':
            print('voiceList is empty')
        else:
            voiceListDict = json.loads(data)
            if fileName not in voiceListDict['voiceList']:
                print(fileName + ' not in list!')
            else:
                voiceListDict['voiceList'].remove(fileName)
                voiceListDict['voiceNum'] -= 1
                print('delete voice success : ' + fileName)
                voiceListFile.close()
                voiceListFile = open('voiceList','w')
                json.dump(voiceListDict,voiceListFile,indent=2)
    except Exception,e:
        print e
    finally:
        os.chdir(path_this)
        return True

'''
get Current songName
@param string path
@return fileName
'''
def getCurrentSongName(path):
    path_this = os.getcwd()
    os.chdir(path)
    currentSongName = None
    try:
        songNameFile = open('songName','r+')
        data = songNameFile.read()
        if data == '':
            print('songName is empty')
        else:
            songNameDict = json.loads(data)
            currentSongSeq = songNameDict['currentSong']
            currentSongID = songNameDict['songIDList'][currentSongSeq]
            currentSongName = "song-" + str(currentSongID)
        songNameFile.close()
    except Exception,e:
        print e
    finally:
        os.chdir(path_this)
        return currentSongName


'''
get Next songName
@param string path
@return fileName
'''
def getNextSongName(path):
    path_this = os.getcwd()
    os.chdir(path)
    currentSongName = None
    try:
        songNameFile = open('songName','r+')
        data = songNameFile.read()
        if data == '':
            print('songName is empty')
        else:
            songNameDict = json.loads(data)
            currentSongSeq = songNameDict['currentSong']
            currentSongID = songNameDict['songIDList'][currentSongSeq]
            if currentSongSeq == songNameDict['songNum']-1:
                songNameDict['currentSong'] = 0
                currentSongID = songNameDict['songIDList'][0]
                currentSongName = 'song-'+str(currentSongID)
            else:
                songNameDict['currentSong'] = currentSongSeq + 1
                currentSongID = songNameDict['songIDList'][currentSongSeq + 1]
                currentSongName = 'song-'+str(currentSongID)
        
        songNameFile.close()
        songNameFile = open('songName','w')
        json.dump(songNameDict,songNameFile,indent=2)

    except Exception,e:
        print e
    finally:
        os.chdir(path_this)
        return currentSongName

'''
get Current voice fileName
@param string path
@return fileName
'''
def getCurrentVoiceName(path):
    path_this = os.getcwd()
    os.chdir(path)
    currentVoiceName = None
    try:
        voiceListFile = open('voiceList','r+')
        data = voiceListFile.read()
        if data == '':
            print('voiceList is empty')
        else:
            voiceListDict = json.loads(data)
            currentVoiceSeq = voiceListDict['currentVoice']
            currentVoiceName = voiceListDict['voiceList'][currentVoiceSeq]
        voiceListFile.close()
    except Exception,e:
        print e
    finally:
        os.chdir(path_this)
        return currentVoiceName

'''
get Latest voice fileName
@param string path
@return fileName
'''
def getLatestVoiceName(path):
    path_this = os.getcwd()
    os.chdir(path)
    currentVoiceName = None
    try:
        voiceListFile = open('voiceList','r+')
        data = voiceListFile.read()
        if data == '':
            print('voiceList is empty')
        else:
            voiceListDict = json.loads(data)
            currentVoiceSeq = voiceListDict['voiceNum'] - 1
            currentVoiceName = voiceListDict['voiceList'][currentVoiceSeq]
        voiceListFile.close()
    except Exception,e:
        print e
    finally:
        os.chdir(path_this)
        return currentVoiceName



'''
get Next voice fileName
@param string path
@return fileName
'''
def getNextVoiceName(path):
    path_this = os.getcwd()
    os.chdir(path)
    currentVoiceName = None
    try:
        voiceListFile = open('voiceList','r+')
        data = voiceListFile.read()
        if data == '':
            print('voiceList is empty')
        else:
            voiceListDict = json.loads(data)
            currentVoiceSeq = voiceListDict['currentVoice']
            if currentVoiceSeq == 0:
                voiceListDict['currentVoice'] = voiceListDict['voiceNum']-1
                currentVoiceName = voiceListDict['voiceList'][voiceListDict['voiceNum']-1]
            else:
                voiceListDict['currentVoice'] = currentVoiceSeq - 1
                currentVoiceName = voiceListDict['voiceList'][currentVoiceSeq - 1]
            
            voiceListFile.close()
            voiceListFile = open('voiceList','w')
            json.dump(voiceListDict,voiceListFile,indent=2)
    except Exception,e:
        print e
    finally:
        os.chdir(path_this)
        return currentVoiceName

'''
get Latest record fileName
@param string path
@return fileName
'''
def getLatestRecordName(path):
    path_this = os.getcwd()
    os.chdir(path)
    currentVoiceName = None
    try:
       cmd = "ls -lt | awk '{print $9}' | head -n 1"
       result = subprocess.check_output(cmd,shell=True)
       currentVoiceName = result.split('\n')[0]
    except Exception,e:
        print e
    finally:
        os.chdir(path_this)
        return currentVoiceName


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



