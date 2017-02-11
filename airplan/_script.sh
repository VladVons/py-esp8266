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

Links()
{
  echo "$0->$FUNCNAME"

  # http://micropython.org/download#esp8266
  # http://www.schatenseite.de/en/2016/04/22/esp8266-witty-cloud-module/
  # https://esp8266.ru/esp8266-gpio-registers/
  # https://docs.micropython.org/en/latest/esp8266/esp8266/quickref.html
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
  find -type f -name '*.py' | sort | \
  while read File; do
    FileSize=$(wc -c $File | awk '{ print $1 }')
    echo "File: $File, Size: $FileSize"

    ExecM "ampy --port $Dev --baud 115200 put $File"
    sleep 1
  done
}

Purge()
{
  ampy --port $Dev --baud 115200 ls |\
  while read File; do
    ExecM "ampy --port $Dev --baud 115200 rm $File"
  done
}


clear
#DeployCore
DeploySrc
#Purge
