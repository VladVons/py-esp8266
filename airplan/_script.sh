#!/bin/bash
#--- VladVons@gmail.com

Dev=$(ls /dev/ttyUSB*)


DeployCore()
{
  echo "$0->$FUNCNAME"

  esptool.py --port $Dev erase_flash
  esptool.py --port $Dev --baud 460800 write_flash --flash_size=detect 0 esp8266-20170108-v1.8.7.bin
}


DeploySrc()
{
  echo "$0->$FUNCNAME"

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
