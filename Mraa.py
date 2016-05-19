#!/usr/bin/python
#-*- coding:utf-8 –*-


import mraa
import time
import sys

import Sound

'''
define the key pin 
'''
#play voice record
play_voice = 45
#record voice
record_voice = 46
#play/pause song
play_song = 47
#next song
play_next_song = 48


class Counter:
  count = 0

c = Counter()

# inside a python interrupt you cannot use 'basic' types so you'll need to use
# interrupt handle function
def intrHandler(gpio):
  print("pin " + repr(gpio.getPin(True)) + " = " + repr(gpio.read()))
  pinNum = 45
  if pinNum == play_voice:
    Sound.playRecord()
  elif pinNum == record_voice:
    Sound.record()
  elif pinNum == play_song:
    Sound.playSong()
  elif pinNum == play_next_song:
    Sound.playNextSong()
  else:
    print('no suitable pin to handle')
  
  c.count+=1

pin = play_voice;

#test for read gpio 
print (mraa.getVersion())
x = mraa.Gpio(play_voice)
x.dir(mraa.DIR_IN)
print(str(x.read()))

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

	pv.isr(mraa.EDGE_BOTH, intrHandler, pv)
  rv.isr(mraa.EDGE_BOTH, intrHandler, sv)
  ps.isr(mraa.EDGE_BOTH, intrHandler, ps)
  pns.isr(mraa.EDGE_BOTH, intrHandler, pns)

	var = raw_input("Press ENTER to stop")
	#x.isrExit()
except ValueError as e:
    print(e)