#!/bin/sh
################################################################################
#      This file is part of Alex@ELEC - http://www.alexelec.in.ua
#      Copyright (C) 2011-2016 Alexandr Zuyev (alex@alexelec.in.ua)
################################################################################

. /storage/.cache/services/scan.conf

SERVICE_DIR="/storage/.cache/services"

VDR_CH_FILE="/storage/.config/vdr/channels.conf"
VDR_CH_TEMP="/storage/.config/vdr/channels.conf.tmp"
LOG_FILE="/tmp/scan-s2.log"
SS2_FILE="/storage/.config/scan-s2/$S2_FILE"

DVB_CUR=$(echo $S2_TUNER | awk '{print $1}')
DVB_NUM=$(echo $DVB_CUR | awk -F'-' '{print $1}')
FRT_NUM=$(echo $DVB_CUR | awk -F'-' '{print $2}')
DVB_DEV="/dev/dvb/adapter$DVB_NUM/frontend$FRT_NUM"

  if [ ! -e "$DVB_DEV" ]; then
      MSG_TEXT="DVB device not found!"
      echo $MSG_TEXT > $LOG_FILE
      exit
  fi

if [ ! "$(pidof scan-s2)" ] ; then

  [ -f "$SERVICE_DIR/tvheadend.conf" ] && systemctl stop tvheadend.service
  [ -f "$SERVICE_DIR/vdr-backend.conf" ] && systemctl stop vdr-backend.service

  if [ "$S2_SERVICE" == "All" ]; then
      SERVICE="-t 7"
  else
      SERVICE="-t 5"
  fi

  if [ "$S2_FTA" == "All" ]; then
      FTA="-x -2"
  else
      FTA="-x 0"
  fi

  if [ "$S2_SPEED" == "Fast" ]; then
      SPEED="-I 5"
  elif [ "$S2_SPEED" == "Slow" ]; then
      SPEED="-I 15"
  else
      SPEED="-I 10"
  fi

  SS2_LNB=$(expr $S2_LNB - 1 )
  SS2_SAT=$(echo $S2_SAT | awk '{print $1}')

  if [ "$S2_TYPE" == "S2" ]; then

      if [ "$S2_POLAR" == "Circular" ]; then
          CIRCULAR="-l 10750,10750,10750"
      else
          CIRCULAR=""
      fi

      /usr/bin/scan-s2 -G -a $DVB_NUM -f $FRT_NUM -s $SS2_LNB $FTA $SERVICE $SPEED -O $SS2_SAT -o vdr $CIRCULAR $SS2_FILE > $VDR_CH_TEMP 2>$LOG_FILE
  else
      /usr/bin/scan-s2 -G -a $DVB_NUM -f $FRT_NUM $FTA $SERVICE $SPEED -o vdr $SS2_FILE > $VDR_CH_TEMP 2>$LOG_FILE
  fi

  SS2_DONE=$(grep 'Found service' $LOG_FILE | awk -F\: '{print $2}' |  awk '{print $1}' | sed 's/^[ \t]*//;s/[ \t]*$//')

  if [ ! -z "$SS2_DONE" ] && [ "$SS2_DONE" != "0" ]; then
      BUKLET=`basename $SS2_FILE .cfg`

      if [ "$S2_UPDATE" == "1" ]; then
          echo ":$BUKLET" >> $VDR_CH_FILE
      else
          echo ":$BUKLET" > $VDR_CH_FILE
      fi

      if [ "$S2_SORT" == "1" ]; then
          sort -k1 $VDR_CH_TEMP >> $VDR_CH_FILE
      else
          cat $VDR_CH_TEMP >> $VDR_CH_FILE
      fi
  fi

  rm -f $VDR_CH_TEMP
  [ -f "$SERVICE_DIR/tvheadend.conf" ] && systemctl start tvheadend.service
  [ -f "$SERVICE_DIR/vdr-backend.conf" ] && systemctl start vdr-backend.service
  exit

else
  MSG_TEXT="Scan-S2 runing..."
  echo $MSG_TEXT > $LOG_FILE
  exit
fi
