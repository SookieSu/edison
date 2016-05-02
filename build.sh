#!/bin/bash

python main.py

if [ $? == 0 ];
then
    exit
else
    echo "success"
fi
