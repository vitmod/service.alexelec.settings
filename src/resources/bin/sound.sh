#!/bin/sh
################################################################################
#      This file is part of Alex@ELEC - http://www.alexelec.in.ua
#      Copyright (C) 2011-2015 Alexandr Zuyev (alex@alexelec.in.ua)
################################################################################

card=$1
device=$2
SOUND_FILE="/storage/.config/asound.conf/asound.conf"

if [ "$card" -a "$device" ]; then

cat > $SOUND_FILE <<EOF
# Audio output device: Defaults (ALSA)

pcm.!default {
    type hw
    card $card
    device $device
}
EOF

echo "Completed!"
else
echo "Error!"
fi
