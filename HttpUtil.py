#!/usr/bin/python
#coding=utf8

import httplib
import urllib


def doGet(domain,url):
    httpClient = None
    try:
        httpClient = httplib.HTTPConnection(domain,80,timeout=30)
        httpClient.request('GET',url)
        response = httpClient.getresponse()
        if response.status != 200:
            return False
        retData = response.read()
        #print (retData)
        return retData
    except Exception,e:
        print e
    finally:
        if httpClient:
            httpClient.close()

def doPost(domain,url,body):
    httpClient = None
    try:
        headers = {
                "Content-type" : "application/x-www-form-urlencoded",
                "Accept" : "text/plain"
                }
        httpClient = httplib.HTTPConnection(domain,80,timeout=30)
        httpClient.request("POST",url,body,headers)
        
        response = httpClient.getresponse()
        if response.status != 200:
            return False
        print response.read()
        #print response.getheaders()
    except Exception,e:
        print e
    finally:
        if httpClient:
            httpClient.close()

