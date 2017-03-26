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

  sudo pip install esptool       --upgrade
  sudo pip install adafruit-ampy --upgrade 
  #sudo pip install picocom       --upgrade
}


Make_mpy_cross()
{
  https://github.com/micropython/micropython.git
  #https://github.com/micropython/micropython/tree/master/mpy-cross
}


Install()
{
  echo "$0->$FUNCNAME"

  sudo su

  apt-get install git
  # git clone https://github.com/VladVons/py-esp8266.git

  apt-get install python-pip

  pip install esptool
  pip install adafruit-ampy
  pip install picocom

  Upgrade

  usermod -a -G dialout linux
  # logout

  #Make_mpy_cross

  # byte code cross compiler. py to mpy
  # https://github.com/micropython/micropython/tree/master/mpy-cross
}


EspFirmware()
{
  echo "$0->$FUNCNAME"

  # images
  # http://micropython.org/download#esp8266

  Dir="/mnt/hdd/ntfs/Python/image"
  #FileName="esp8266-20170108-v1.8.7.bin"
  FileName="esp8266-ota-20170326-v1.8.7-491-g3f810da.bin" 

  File=$Dir/$FileName
  if [ -f $File ] ; then
    ExecM "esptool.py --port $Dev erase_flash"
    ExecM "esptool.py --port $Dev --baud 460800 write_flash --flash_size=detect 0 $File"

    EspFileList
  else
    echo "File not found $File"  
  fi;
}


EspFileList()
{
  echo "$0->$FUNCNAME"
  
  echo "List files in ESP"
  ExecM "ampy --port $Dev --baud $Speed ls"
}


EspSrcFile()
{
  aFile="$1"

  FileSize=$(wc -c $aFile | awk '{ print $1 }')
  echo "File: $aFile, Size: $FileSize"
  ExecM "ampy --port $Dev --baud $Speed put $aFile"
}

EspSrcCopy()
{
  echo "$0->$FUNCNAME"

  EspFileList

  # deploy
  GetSrc |\
  while read File; do
    EspSrcFile $File
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
    Install)        "$1"        ;;
    Upgrade)        "$1"        ;;
    EspFirmware)    "$1"        ;;
    EspRelease)     "$1"        ;;
    EspFileList|l)  EspFileList ;;
    EspSrcDel|d)    EspSrcDel   ;;
    EspSrcFile|f)   EspSrcFile  $2 ;;
    EspSrcCopy|c)   EspSrcCopy  ;;
esac
