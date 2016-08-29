#!/bin/sh
################################################################################
#      This file is part of Alex@ELEC - http://www.alexelec.in.ua
#      Copyright (C) 2011-2016 Alexandr Zuyev (alex@alexelec.in.ua)
################################################################################

. /storage/.cache/services/diseqc.conf

BIN_DIR=$(echo $0 | sed 's/\/diseqc.sh//')
DISEQC_FILE="/storage/.config/vdr/diseqc.conf"
DISEQC_BIN="$BIN_DIR/diseqccalc.sh"

IS_SAT="false"
if [ "$SAT1" != "none" -o "$SAT2" != "none" -o "$SAT3" != "none" -o "$SAT4" != "none" ]; then
  IS_SAT="true"
fi

if [ "$IS_SAT" = "true" ]; then

cat > $DISEQC_FILE <<EOF
# DiSEqC configuration for VDR
#
# Format:
#
# satellite slof polarization lof command...
#
# satellite:      one of the 'S' codes defined in sources.conf
#                 the special value 'S360E' means that this entry uses a positioner
#                 (command 'P') that can move the dish to any requested satellite
#                 position within its range
# slof:           switch frequency of LNB; the first entry with
#                 an slof greater than the actual transponder
#                 frequency will be used
# polarization:   V = vertical, H = horizontal, L = Left circular, R = Right circular
# lof:            the local oscillator frequency to subtract from
#                 the actual transponder frequency
# command:
#   t         tone off
#   T         tone on
#   F         voltage off (0V)
#   v         voltage low (13V)
#   V         voltage high (18V)
#   A         mini A
#   B         mini B
#   Pn        use positioner to move dish to satellite position n (or to the
#             satellite's orbital position, if no position number is given)
#   Sn        satellite channel routing code sequence for bank n follows
#   Wnn       wait nn milliseconds (nn may be any positive integer number)
#   [xx ...]  hex code sequence (max. 6)
#
# The 'command...' part is optional.
#
# A line containing space separated integer numbers, terminated with a ':',
# defines that any following DiSEqC sequences apply only to the given list
# of device numbers.

EOF

$DISEQC_BIN >> $DISEQC_FILE
echo "Completed!"
else
echo "Error!"
fi
