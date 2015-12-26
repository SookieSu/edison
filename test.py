#!/usr/bin/python
#coding=utf8

import mraa
import json
import os

import HttpUtil

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

    retUrl = getUrl(record['msgtype'],record['data'])
    print (retUrl)
    urlArray = retUrl.split('/')
    print (urlArray)
    retDomain = urlArray[2]
    retUri = urlArray[3]
    print ('%s : %s ' % (retDomain,retUri))
    '''
    for record in data:
        msgtype = record['msgtype']
        data = record['data']
        retUrl = getUrl(msgtype,data)
        print (msgtype)
        print (data)
    '''

def addVoice(data):
    urlArray = data.split('/')
    print (urlArray)
    retDomain = urlArray[2]
    retUrl = urlArray[3]
    retData = HttpUtil.doGet(retDomain,'/'+retUrl)
    filename = retUrl
    writeFile(path_voice,filename,retData)
    #print(retData)

def writeFile(path,filename,data):
    path_this = os.getcwd()
    os.chdir(path)
    mediaFile = open(filename,'w')
    mediaFile.write(data)
    mediaFile.close()
    os.chdir(path_this)

def getUrl(msgtype,data):
    print type(data)
    if msgtype == 'voice':
        return data
    if msgtype == 'song_add':
        return data['url']
    if msgtype == 'story_add':
        return data['url']

getMessage('0')
print (mraa.getVersion())
print (mraa.getPlatformName())
print (mraa.getPlatformType())
print (mraa.getPinName(30))

x = mraa.Gpio(20)
print (x.read())
#print ("%.5f" % x.readFloat())
#print (mraa.pinModeTest())
