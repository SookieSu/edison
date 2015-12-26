#!/usr/bin/python
#coding=utf8

import mraa
import json
import os
import sys

import HttpUtil
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
    '''
    record = data[-1]
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

    

def addVoice(data):
    urlArray = data.split('/')
    print (urlArray)
    retDomain = urlArray[2]
    retUrl = urlArray[3]
    retData = HttpUtil.doGet(retDomain,'/'+retUrl)
    filename = retUrl
    writeFile(path_voice,filename,retData)
    #print(retData)

def addSong(data):
    if data == "":
        return False
    print(data)
    jsonData = json.loads(data)
    songName = jsonData['name']
    songUrl = str(jsonData['url'])
    print (songUrl)
    urlArray = songUrl.split('/')
    retDomain = urlArray[2]
    retUrl = urlArray[3:]
    url = "/".join(retUrl)
    #retData = HttpUtil.doGet(retDomain,'/'+url)
    #writeFile(path_song,songName,retData)

def addStory(data):
    if data == "":
        return False
    jsonData = json.loads(data)
    storyName = jsonData['name']
    storyUrl = jsonData['url']


def writeFile(path,filename,data):
    path_this = os.getcwd()
    os.chdir(path)
    mediaFile = open(filename,'w')
    mediaFile.write(data)
    mediaFile.close()
    os.chdir(path_this)


getMessage('0')
print (mraa.getVersion())
print (mraa.getPlatformName())
print (mraa.getPlatformType())
print (mraa.getPinName(30))

x = mraa.Gpio(20)
print (x.read())
#print ("%.5f" % x.readFloat())
#print (mraa.pinModeTest())
