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


Upgrade()
{
  echo "$0->$FUNCNAME"

  pip install esptool       --upgrade
  pip install adafruit-ampy --upgrade 
  pip install picocom       --upgrade
}


Install()
{
  echo "$0->$FUNCNAME"

  apt-get install git
  # git clone https://github.com/VladVons/py-esp8266.git

  apt-get install python-pip

  pip install esptool
  pip install adafruit-ampy
  pip install picocom

  Upgrade

  usermod -a -G dialout linux
  # logout

  # byte code cross compiler. py to mpy
  # https://github.com/micropython/micropython/tree/master/mpy-cross
}

EspFirmw()
{
  echo "$0->$FUNCNAME"

  # images
  # http://micropython.org/download#esp8266

  File="esp8266-20170108-v1.8.7.bin"
  ExecM "esptool.py --port $Dev erase_flash"
  ExecM "esptool.py --port $Dev --baud 460800 write_flash --flash_size=detect 0 $File"
}


EspSrc()
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


EspDel()
{
  ampy --port $Dev --baud 115200 ls | grep -v "boot.py" |\
  while read File; do
    ExecM "ampy --port $Dev --baud 115200 rm $File"
  done

  ExecM "ampy --port $Dev --baud 115200 ls"
}


clear
case $1 in
    Install)     "$1"   "$2"  ;;
    Upgrade)     "$1"   "$2"  ;;
    EspFirmw)    "$1"   "$2"  ;;
    EspDel|d)    EspDel "$2"  ;;
    EspSrc|*)    EspSrc "$3"  ;;
esac
