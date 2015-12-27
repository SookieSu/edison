#!/usr/bin/python
#coding=utf8

import mraa
import json
import os
import sys
import urllib

import HttpUtil
import FileOperate

reload(sys)
sys.setdefaultencoding("utf-8")
path_voice = r"../voice"
path_song = r"../song"
path_story = r"../story"


def getMessage(deviceID):
    domain = '2.sookiesu.sinaapp.com'
    url = '/api/deviceApi.php?method=getData&deviceID='+deviceID
    retData = HttpUtil.doGet(domain,url)
    jsonData = json.loads(retData)
    data = jsonData['data']
    #print(data)
    #test
    
    record = data[2]
    msgtype = record['msgtype']
    if msgtype == 'voice':
        addVoice(record['data'])
    if msgtype == 'song_add':
        addSong(record['id'],record['data'])
    if msgtype == 'story_add':
        addStory(record['id'],record['data'])
    if msgtype == 'song_delete':
        deleteSong(record['id'],record['data'])
    if msgtype == 'story_delete':
        deleteStory(record['id'],record['data'])
    '''
    for record in data:
        msgtype = record['msgtype']
        if msgtype == 'voice':
            addVoice(record['data'])
        if msgtype == 'song_add':
            addSong(record['data'])
        if msgtype == 'story_add':
            addStory(record['data'])
        if msgtype == 'song_delete':
            deleteSong(record['data'])
        if msgtype == 'story_delete':
            deleteStory(record['data'])
    '''

def setMessage(deviceID,data):
    domain = '2.sookiesu.sinaapp.com'
    url = '/api/deviceApi.php'
    body = {
            "method" : "postData",
            "deviceID" : "",
            "data" : ""
            }
    body['deviceID'] = deviceID
    body['data'] = data
    realbody = urllib.urlencode(body)
    retData = HttpUtil.doPost(domain,url,realbody)

def addVoice(data):
    urlArray = data.split('/')
    print (urlArray)
    retDomain = urlArray[2]
    retUrl = urlArray[3]
    retData = HttpUtil.doGet(retDomain,'/'+retUrl)
    filename = retUrl
    FileOperate.writeFile(path_voice,filename,retData)
    #print(retData)

def addSong(songID,data):
    if data == "":
        return False
    print(data)
    filename = 'song-'+songID
    jsonData = json.loads(data)
    songName = jsonData['name']
    songUrl = str(jsonData['url'])
    print (songUrl)
    urlArray = songUrl.split('/')
    retDomain = urlArray[2]
    retUrl = urlArray[3:]
    url = "/".join(retUrl)
    retData = HttpUtil.doGet(retDomain,'/'+url)
    flag = FileOperate.writeSongName(path_song,songName,songID)
    if flag == True:
        FileOperate.writeFile(path_song,filename,retData)
        return True
    else:
        return False

def addStory(storyID,data):
    if data == "":
        return False
    jsonData = json.loads(data)
    storyName = jsonData['name']
    storyUrl = jsonData['url']



#getMessage('0')
filetest = open('../voice/voice-1450681665.amr','r')
voicedata = filetest.read()
#voicedata = "testtesttest"
setMessage('0',voicedata)
print (mraa.getVersion())
print (mraa.getPlatformName())
print (mraa.getPlatformType())
print (mraa.getPinName(30))

x = mraa.Gpio(20)
print (x.read())
#print ("%.5f" % x.readFloat())
#print (mraa.pinModeTest())
