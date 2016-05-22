#!/usr/bin/python
#-*- coding:utf-8 -*-

#import mraa
import json
import os
import sys
import urllib
import time
import pwd

import HttpUtil
import FileOperate
import Sound

reload(sys)
sys.setdefaultencoding("utf-8")


path_voice = r"/home/root/sookie/voice"
path_song = r"/home/root/sookie/song"
path_story = r"/home/root/sookie/story"
path_log = r"/home/root/sookie/log"
path_record = r"/home/root/sookie/record"

'''
get unread voice message,song add/delete message,story add/delete message from server
@param string deviceID
'''
def getMessage(deviceID):
    domain = '2.sookiesu.sinaapp.com'
    url = '/api/deviceApi.php?method=getData&deviceID='+deviceID
    
    retData = HttpUtil.doGet(domain,url)
    print(retData)
    jsonData = json.loads(retData)
    data = jsonData['data']
    
    result = {}
    result['errNo'] = 0
    result['errMsg'] = ""
    result['message'] = retData

    if data == None:
        result['errNo'] = 202
        result['errMsg'] = 'get new message failed from server !'
    
    else:
        for record in data:    
            msgtype = record['msgtype']
            '''
            msgtype == voice : url
            msgtype == song_add or story_add : id , name , url 
            msgtype == song_delete or story_delete : id
            '''
            retFlag = True
            if msgtype == 'voice':
                print('add voice')
                retFlag = addVoice(record['data'])
            if msgtype == 'song_add':
                songdata = json.loads(record['data'])
                songID = songdata['id']
                songName = songdata['name']
                songUrl = songdata['url']
                print(songID,songName,songUrl)
                retFlag = addSong(songID,songName,songUrl)
            if msgtype == 'story_add':
                print('add story')
            if msgtype == 'song_delete':
                retFlag = deleteSong(record['data'])
            if msgtype == 'story_delete':
                retFlag = deleteStory(record['data'])

            if retFlag == False:
                result['errNo'] = 101
                result['errMsg'] = result['errMsg'] + " update failed : " + msgtype + ':' + record['data']
    
    struct_time = time.localtime(time.time())
    log_time = time.strftime('%Y%m%d%H%M%S',struct_time)
    result['exectime'] = log_time
    print(json.dumps(result,indent=2))
    FileOperate.writeLog(path_log,json.dumps(result,indent=2))

'''
set voice message from device to wechat,post to server
@param string deviceID
@param binary data
@return retData
'''
def setMessage(deviceID,fileName):
    domain = '2.sookiesu.sinaapp.com'
    url = '/api/deviceApi.php'
    body = {
            "method" : "postData",
            "deviceID" : "",
            "data" : ""
            }
    
    result = {}
    result['errNo'] = 0
    result['errMsg'] = ""
    result['message'] = "upload record to wechat : " + fileName

    data = FileOperate.readFile(path_record,fileName)
    if data == None:
        result['errNo'] = 202
        result['errMsg'] = 'can not read file !'
    
    body['deviceID'] = deviceID
    body['data'] = data
    realbody = urllib.urlencode(body)
    retData = HttpUtil.doPost(domain,url,realbody)
    
    struct_time = time.localtime(time.time())
    log_time = time.strftime('%Y%m%d%H%M%S',struct_time)
    result['exectime'] = log_time
    print(json.dumps(result,indent=2))
    FileOperate.writeLog(path_log,json.dumps(result,indent=2))


'''
add a voice message record to device from wechat
@param string data
@return bool retFlag
'''
def addVoice(data):
    urlArray = data.split('/')
    
    #get data source domain
    retDomain = urlArray[2]
    #get data source filename
    retUrl = urlArray[3]
    #get voice source
    retData = HttpUtil.doGet(retDomain,'/'+retUrl)
    source_filename = retUrl
    
    retFlag = FileOperate.writeFile(path_voice,source_filename,retData)
    if retFlag == False:
        return False
    else:
        source = source_filename.split('.')
        target_filename = source[0] + ".mp3"
        status = Sound.amrToMp3(path_voice,source_filename,target_filename)
        if status == 0 :
            FileOperate.deleteFile(path_voice,source_filename)
            return FileOperate.writeVoiceList(path_voice,target_filename)
        else:
            print('convert amr to mp3 wrong!')
            return False

'''
add a song message record to device from wechat
@param int songID
@param string songName
@param songUrl
@return bool 
'''
def addSong(songID,songName,songUrl):
    filename = 'song-'+str(songID)
    songUrl = str(songUrl)
    urlArray = songUrl.split('/')
    retDomain = urlArray[2]
    retUrlArray = urlArray[3:]
    retUrl = "/".join(retUrlArray)
    retData = HttpUtil.doGet(retDomain,'/'+retUrl)
    
    flag = FileOperate.writeFile(path_song,filename,retData)
    
    if flag == True:
        return FileOperate.writeSongName(path_song,songName,songID)
    else:
        return False
    
'''
add a story message record to device from wechat
@param int storyID
@param string storyName
@param storyUrl
@return bool 
'''
def addStory(storyID,data):
    if data == "":
        return False
    jsonData = json.loads(data)
    storyName = jsonData['name']
    storyUrl = jsonData['url']

'''
delete the song in device at ~/sookie/song/ by songID
@param int songID
@return bool 
'''
def deleteSong(songID):
    filename = 'song-'+str(songID)
    print(filename)
    flag = FileOperate.deleteFile(path_song,filename)
    print('delete file flag : '+ str(flag))
    if flag == True:
        return FileOperate.deleteSongName(path_song,songID)
    else:
        return False

'''
sync media info between device and server , server be the host , device be the slave
@param string deviceID
@return dict result
'''
def syncMediaInfo(deviceID):
    domain = '2.sookiesu.sinaapp.com'
    url = '/api/deviceApi.php?method=syncMediaInfo&deviceID='+deviceID
    
    retData = HttpUtil.doGet(domain,url)
    #print(retData)
    jsonData = json.loads(retData)
    data = jsonData['data']
    
    result = {}
    result['errNo'] = 0
    result['errMsg'] = ""
    result['message'] = "exec syncMediaInfo "
    
    songNameData = FileOperate.readFile(path_song,'songName')
    if songNameData != '':
        songDict = json.loads(songNameData)
        songIDList_device = songDict['songList'].keys()
    else:
        songIDList_device = []
    
    songIDList_server = []
    
    #check the song ID list in server , to add new song to device
    for record in data:
        songID = record['id']
        songIDList_server.append(songID)
        if songID not in songIDList_device:
            detail = json.loads(record['data'])
            songName = detail['name']
            songURL = detail['url']
            retFlag = addSong(songID,songName,songURL)
            if retFlag == True:
                result['message'] = result['message'] + ' add song ' + songID + ' success! ' + record['data'] + '  '
            else:
                result['errNo'] = 33
                result['errMsg'] = result['errMsg'] + ' add song ' + songID + ' failed! ' + record['data'] + '  '
    
    for songID in songIDList_device:
        if songID not in songIDList_server:
            retFlag = deleteSong(songID)
            if retFlag == True:
                result['message'] = result['message'] + ' delete song ' + songID + ' success! ' + songDict['songList'][songID]  + '  '
            else:
                result['errNo'] = 33
                result['errMsg'] = result['errMsg'] + ' delete song ' + songID + ' failed! ' + songDict['songList'][songID] + '  '
    

    struct_time = time.localtime(time.time())
    log_time = time.strftime('%Y%m%d%H%M%S',struct_time)
    result['exectime'] = log_time
    print(json.dumps(result,indent=2))
    FileOperate.writeLog(path_log,json.dumps(result,indent=2))






'''
test for mraa
print (mraa.getVersion())
print (mraa.getPlatformName())
print (mraa.getPinName(30))

x = mraa.Gpio(20)
print (x.read())
#print ("%.5f" % x.readFloat())
#print (mraa.pinModeTest())
'''
