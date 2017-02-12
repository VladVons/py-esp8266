#!/bin/bash
#--- VladVons@gmail.com

Dev=$(ls /dev/ttyUSB*)

ExecM()
{
  aExec="$1"; aMsg="$2";

  echo
  echo "$FUNCNAME, $aExec, $aMsg"
  eval "$aExec"
}


DeployCore()
{
  echo "$0->$FUNCNAME"

  File="esp8266-20170108-v1.8.7.bin"
  ExecM "esptool.py --port $Dev erase_flash"
  ExecM "esptool.py --port $Dev --baud 460800 write_flash --flash_size=detect 0 $File"
}


DeploySrc()
{
  echo "$0->$FUNCNAME"

  # get file list
  echo "List files in ROM"
  ExecM "ampy --port $Dev --baud 115200 ls"
  echo

  # deploy
  find -type f | grep -v ".\_" | sort | \
  while read File; do
    FileSize=$(wc -c $File | awk '{ print $1 }')
    echo "File: $File, Size: $FileSize"

    #Speed=74880
    Speed=115200
    #Speed=230400
    #Speed=460800
    ExecM "ampy --port $Dev --baud $Speed put $File"
    sleep 1
  done
}

Purge()
{
  ampy --port $Dev --baud 115200 ls | grep -v "boot.py" |\
  while read File; do
    ExecM "ampy --port $Dev --baud 115200 rm $File"
  done

  ExecM "ampy --port $Dev --baud 115200 ls"
}


clear
#DeployCore
DeploySrc
#Purge
