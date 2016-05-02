#!/usr/bin/python
#-*- coding:utf-8 –*-

#import mraa
import json
import os
import sys
import urllib
import time
import pwd

import HttpUtil
import FileOperate

reload(sys)
sys.setdefaultencoding("utf-8")
path_voice = r"/home/root/sookie/voice"
path_song = r"/home/root/sookie/song"
path_story = r"/home/root/sookie/story"
path_log = r"/home/root/sookie/log"

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
    return retData

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
    filename = retUrl
    
    retFlag = FileOperate.writeFile(path_voice,filename,retData)
    return retFlag

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
delete the story in device at ~/sookie/story/ by storyID
@param int storyID
@return bool 
'''
def deleteStory(storyID):
    return True

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
    result['message'] = "exec syncMediaInfo \n"

    songNameData = FileOperate.readFile(path_song,'songName')
    songDict = json.loads(songNameData)
    songIDList_device = songDict.keys()
    songIDList_server = []
    
    #check the song ID list in server , to add new song to device
    for record in data:
        songID = record['id']
        songIDList_server.append(songID)
        #print(songID)
        if songID not in songIDList_device:
            detail = json.loads(record['data'])
            songName = detail['name']
            songURL = detail['url']
            #print(songName,songURL)
            retFlag = addSong(songID,songName,songURL)
            if retFlag == True:
                result['message'] = result['message'] + ' add song ' + songID + ' success! ' + record['data'] + '\n'
            else:
                result['errNo'] = 33
                result['errMsg'] = result['errMsg'] + ' add song ' + songID + ' failed! ' + record['data'] + '\n'
    
    for songID in songIDList_device:
        if songID not in songIDList_server:
            retFlag = deleteSong(songID)
            if retFlag == True:
                result['message'] = result['message'] + ' delete song ' + songID + ' success! ' + songDict[songID]  + '\n'
            else:
                result['errNo'] = 33
                result['errMsg'] = result['errMsg'] + ' delete song ' + songID + ' failed! ' + songDict[songID] + '\n'
    

    struct_time = time.localtime(time.time())
    log_time = time.strftime('%Y%m%d%H%M%S',struct_time)
    result['exectime'] = log_time
    print(json.dumps(result,indent=2))
    FileOperate.writeLog(path_log,json.dumps(result,indent=2))



def main():
    try:
        syncMediaInfo('0')
        getMessage('0')
        #setMessage('0',os.geteuid())
        sys.exit(0)
    except:
        sys.exit(1)


if __name__ == '__main__':
    main()


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
