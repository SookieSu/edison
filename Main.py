#!/usr/bin/python
#-*- coding:utf-8 -*-

import sys

import Api
#import Mraa
import Sound

def main():
    try:
        Api.syncMediaInfo('0')
        Api.getMessage('0')
        #Api.setMessage('0','foobar.amr')
        sys.exit(0)
    except:
        sys.exit(1)


if __name__ == '__main__':
    main()

