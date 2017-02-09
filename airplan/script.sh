#!/bin/bash
#--- VladVons@gmail.com


DeploySrc()
{
  Dev=$(ls /dev/ttyUSB*)

  # get file list
  echo "List files in ROM"
  ampy --port $Dev --baud 115200 ls
  echo

  # deploy
  find -type f -name '*.py' | sort | \
  while read File; do
    FileSize=$(wc -c $File | awk '{ print $1 }')
    echo "File: $File, Size: $FileSize"

    ampy --port $Dev --baud 115200 put $File
    sleep 1
  done
}

clear
DeploySrc
