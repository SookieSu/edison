#!/usr/bin/python

import os
import sys
import time


def playRecord():
	print('playRecord')

def playSong():
	print('playSong')

def playNextSong():
	print('playNextSong')

def record():
	print('record')

def play():
	print('play')

'''
import mraa as m
import random as rand


dev = m.Spi(0)

for x in range(0,10):
    txbuf = bytearray(4)
    for y in range(0,4):
        txbuf[y] = rand.randrange(0,256)
    rxbuf = dev.write(txbuf)
    if rxbuf != txbuf:
        print("we have an error captain!")
        break
        exit(1)
'''

