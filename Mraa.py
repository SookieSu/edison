#!/usr/bin/python
#-*- coding:utf-8 –*-


import mraa
import time
import sys
import ctypes

import Sound

'''
define the key pin 
'''
#play voice record J20-4
play_voice = 45
#record voice J20-5
record_voice = 46
#play/pause song J20-6
play_song = 47
#next song J20-7
play_next_song = 48


class Counter:
    count = 0

c = Counter()

# inside a python interrupt you cannot use 'basic' types so you'll need to use
# interrupt handle function
def haha(e):
    print(e)


def intrHandler(gpio):
    
    pinNum = 0
    try:
        pinNum = ctypes.cast(gpio,ctypes.py_object).value.getPin(True)
    except Exception as e:
        haha(e)
    
    if pinNum == play_voice:
        Sound.playVoice()
    elif pinNum == record_voice:
        if c.count % 2 == 0:
            Sound.record()
        else:
            Sound.stopRecord()
    elif pinNum == play_song:
        if c.count % 2 == 0:
            Sound.playSong()
        else:
            Sound.pauseSong()
    elif pinNum == play_next_song:
        Sound.playNextSong()
    else:
        haha('no suitable pin to handle')
    
    c.count+=1



#input pin to start ISR
'''
if (len(sys.argv) == 2):
    try:
        pin = int(sys.argv[1], 10)
    except ValueError:
        printf("Invalid pin " + sys.argv[1])
'''

#interrupt exec
try:
    pv = mraa.Gpio(play_voice)
    rv = mraa.Gpio(record_voice)
    ps = mraa.Gpio(play_song)
    pns = mraa.Gpio(play_next_song)
    
    print("Starting ISR for pin " + repr(play_voice) + ',' + repr(record_voice) + ',' + repr(play_song) + ',' + repr(play_next_song))
	
    pv.dir(mraa.DIR_IN)
    rv.dir(mraa.DIR_IN)
    ps.dir(mraa.DIR_IN)
    pns.dir(mraa.DIR_IN)


    pv.isr(mraa.EDGE_RISING, intrHandler, pv)
    rv.isr(mraa.EDGE_RISING, intrHandler, rv)
    ps.isr(mraa.EDGE_RISING, intrHandler, ps)
    pns.isr(mraa.EDGE_RISING, intrHandler, pns)
    
    while True:
        pass
    #var = raw_input("Press ENTER to stop")
    #x.isrExit()
except ValueError as e:
    print(e)



