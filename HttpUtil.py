#!/usr/bin/python
#coding=utf8

import httplib




def doGet(domain,url):
    try:
        httpClient = httplib.HTTPConnection(domain,80,timeout=30)
        httpClient.request('GET',url)
        response = httpClient.getresponse()
        if response.status != 200:
            return false
        retData = response.read()
        #print (retData)
        return retData
    except Exception,e:
        print e
    finally:
        if httpClient:
            httpClient.close()
