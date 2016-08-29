#!/bin/sh
################################################################################
#      This file is part of Alex@ELEC - http://www.alexelec.in.ua
#      Copyright (C) 2011-2016 Alexandr Zuyev (alex@alexelec.in.ua)
################################################################################

. /storage/.cache/services/scan.conf

TPL_FILE="/storage/.config/scan-s2/$S2_FILE"

ret=$(grep '^[ST]' $TPL_FILE | awk 'END { print NR }')
echo $ret
