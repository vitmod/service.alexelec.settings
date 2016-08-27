#!/bin/sh
################################################################################
#      This file is part of Alex@ELEC - http://www.alexelec.in.ua
#      Copyright (C) 2011-2016 Alexandr Zuyev (alex@alexelec.in.ua)
################################################################################

FILE_LIST="/tmp/dvb-dev.tmp"
DVB_NAMES='NOT FOUND!'

FRONTENDS=$(ls /sys/class/dvb/dvb?.frontend?/device/i2c-?/name 2>/dev/null)

if [ -e /dev/dvb/adapter0/frontend0 ]; then
  if [ -n "$FRONTENDS" ]; then
      rm -f $FILE_LIST
      for dev in $FRONTENDS; do
          DEVICE=$(cat $dev)
          if [ -n "$DEVICE" ]; then
              echo "<< $DEVICE >>" >> $FILE_LIST
          fi
      done
      TMP_NAMES=$(cat $FILE_LIST)
      [ -n "$TMP_NAMES" ] && DVB_NAMES=$TMP_NAMES
  fi
fi

echo $DVB_NAMES
