#!/bin/bash
#--- VladVons@gmail.com

Dev=$(ls /dev/ttyUSB*)

Speed=115200
#Speed=460800

ExecM()
{
  aExec="$1"; aMsg="$2";

  echo
  echo "$FUNCNAME, $aExec, $aMsg"
  eval "$aExec"
}


GetSrc()
{
  ls -p | egrep -v "/|_script.sh" | sort
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


EspFirmware()
{
  echo "$0->$FUNCNAME"

  # images
  # http://micropython.org/download#esp8266

  File="esp8266-20170108-v1.8.7.bin"
  ExecM "esptool.py --port $Dev erase_flash"
  ExecM "esptool.py --port $Dev --baud 460800 write_flash --flash_size=detect 0 $File"
}


EspFileList()
{
  echo "$0->$FUNCNAME"
  
  echo "List files in ESP"
  ExecM "ampy --port $Dev --baud $Speed ls"
}

EspSrcCopy()
{
  echo "$0->$FUNCNAME"

  EspFileList

  # deploy
  GetSrc |\
  while read File; do
    FileSize=$(wc -c $File | awk '{ print $1 }')
    echo "File: $File, Size: $FileSize"

    ExecM "ampy --port $Dev --baud $Speed put $File"
    sleep 1
  done
}


EspSrcDel()
{
  echo "$0->$FUNCNAME"

  echo "Delete files in ESP"

  ampy --port $Dev --baud $Speed ls | grep -v "boot.py" |\
  while read File; do
    ExecM "ampy --port $Dev --baud $Speed rm $File"
  done

  EspFileList  
}


EspRelease()
{
  echo "$0->$FUNCNAME"

  SkipFiles="boot.py,main.py,config.json"

  DirOut="Release"
  mkdir -p $DirOut

  EspSrcDel

  GetSrc |\
  while read File; do
    if [[ "$SkipFiles" == *"$File"* ]]; then
        FileOut=$File
        cp $File $DirOut
    else
        FileObj=$(echo $File | sed "s|.py|.mpy|g")
        FileOut=$DirOut/$FileObj
        mpy-cross $File -o $FileOut
    fi

    ExecM "ampy --port $Dev --baud $Speed put $FileOut"
  done

  EspFileList
}


clear
case $1 in
    Install)        "$1"       ;;
    Upgrade)        "$1"       ;;
    EspFirmware)    "$1"       ;;
    EspRelease)     "$1"       ;;
    EspSrcDel|d)    EspSrcDel  ;;
    EspSrcCopy|*)   EspSrcCopy ;;
esac
