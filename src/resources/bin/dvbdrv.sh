#!/bin/sh
################################################################################
#      This file is part of Alex@ELEC - http://www.alexelec.in.ua
#      Copyright (C) 2011-2016 Alexandr Zuyev (alex@alexelec.in.ua)
################################################################################

DRV_LIST=`ls /lib/modules | grep $(uname -r)-`
FILE_LIST="/tmp/dvb-drv.tmp"

rm -f $FILE_LIST

for DVB_DRV in $DRV_LIST; do
  echo $DVB_DRV
  case "$DVB_DRV" in
    *-tbs)               # TBS-Open drivers
        DRIVER="TBS"
     ;;
    *-mb)                # Media_Build drivers
        DRIVER="MEDIA"
     ;;
    *-s2)                # s2-liplianin drivers
        DRIVER="S2"
     ;;
    *-core)              # Default Linux drivers
        DRIVER="CORE"
     ;;
  esac
  echo $DRIVER >> $FILE_LIST
done

exit 0
