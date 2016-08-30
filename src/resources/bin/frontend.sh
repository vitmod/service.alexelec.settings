#!/bin/sh
################################################################################
#      This file is part of Alex@ELEC - http://www.alexelec.in.ua
#      Copyright (C) 2011-2016 Alexandr Zuyev (alex@alexelec.in.ua)
################################################################################

DVB_NAMES='NOT FOUND!'

if [ -e /dev/dvb/adapter0/frontend0 ]; then
  DVB_LIST="/tmp/frontend.tmp"
  DVB_DEV=$(ls /dev/dvb/adapter?/frontend? 2>/dev/null)
  if [ -n "$DVB_DEV" ]; then
      rm -f $DVB_LIST
      for dev in $DVB_DEV; do
          DVB_NUM=$(echo $dev | awk -F'/' '{print $4}' | sed 's/adapter//')
          FRT_NUM=$(echo $dev | awk -F'/' '{print $5}' | sed 's/frontend//')
          DEV_NAME=$(cat /sys/class/dvb/dvb$DVB_NUM.frontend$FRT_NUM/device/i2c-*/name 2>/dev/null)
          [ -z "$DEV_NAME" ] && DEV_NAME='Unknown'
          echo "$DVB_NUM-$FRT_NUM << $DEV_NAME >>" >> $DVB_LIST
      done
      TMP_NAMES=$(cat $DVB_LIST | sed 's/.-.//')
      [ -n "$TMP_NAMES" ] && DVB_NAMES=$TMP_NAMES
  fi
fi

echo $DVB_NAMES
