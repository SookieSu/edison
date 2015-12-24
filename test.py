#!/usr/bin/python
#coding=utf8

import mraa
import httplib

try:
    httpClient = httplib.HTTPConnection('2.sookiesu.sinaapp.com',80,timeout=30)
    httpClient.request('GET','/api/deviceApi.php?deviceID=0&method=getData')
    #httpClient = httplib.HTTPConnection('www.baidu.com',80,timeout=30)
    #httpClient.request('GET','/')
    response = httpClient.getresponse()
    print response.status
    print response.read()
except Exception,e:
    print e
finally:
    if httpClient:
        httpClient.close()

print (mraa.getVersion())
print (mraa.getPlatformName())
print (mraa.getPlatformType())
print (mraa.getPinName(30))

x = mraa.Gpio(20)
print (x.read())
#print ("%.5f" % x.readFloat())
#print (mraa.pinModeTest())
