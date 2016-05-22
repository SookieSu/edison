#!/bin/sh
#mplayer pause
if [ -e /tmp/player.fifo ];
    then
    if [ "`ps aux |grep ' mplayer '|grep -v grep|grep "/tmp/player.fifo"| wc -l`" != 0 ];
    then
        echo pause > /tmp/player.fifo
    fi
fi
exit
