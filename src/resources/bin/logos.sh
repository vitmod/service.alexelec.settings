#!/bin/sh
################################################################################
#      This file is part of Alex@ELEC - http://www.alexelec.in.ua
#      Copyright (C) 2011-2016 Alexandr Zuyev (alex@alexelec.in.ua)
################################################################################

. /storage/.cache/services/logos.conf

# Logos config
LOG_FILE="/tmp/logo_conv.log"
MISS_FILE="/tmp/miss_logo.log"
TEMP_DIR="/storage/.kodi/temp"
SOURCE_DIR="$TEMP_DIR/logos_src" #logo source directory / путь к логотипам с прозрачными фонами
SOURCE_DIR_LOGOS="$SOURCE_DIR/logos" #logo source directory <logos>
SOURCE_DIR_BACKG="$SOURCE_DIR/backgrounds" #logo source directory <backgrounds>
SOURCE_FILE_NAMES="$SOURCE_DIR/src_file.tmp"
VDR_CHANNELS="/storage/.config/vdr/channels.conf" #path to VDR channels.conf file / путь к файлу списка каналов VDR
OUTPUT_DIR_TEMP="$LOGOS_DIR/tmp"
BACKGROUND="$SOURCE_DIR_BACKG/bg-${LOGOS_BG_COLOR}.png" #choose your background / путь к файлу фона логотипа
FOREGROUND="$SOURCE_DIR_BACKG/fg${LOGOS_FG_COLOR}.png" #choose your foreground / путь к файлу блика логотипа

RESIZE='220x164'
EXTENT='268x200'

#################################MAIN###########################################

# Unpack Logos
if [ "$1" == "unpack" ] ; then

  rm -rf $SOURCE_DIR
  mkdir -p $SOURCE_DIR
  tar -jxf $TEMP_DIR/logos.tar.bz2 -C $SOURCE_DIR
  rm -f $TEMP_DIR/logos.tar.bz2
  echo "Unpack logos completed."

# Create logos list file
elif [ "$1" == "list" ] ; then
  rm -f $SOURCE_FILE_NAMES
  touch $SOURCE_FILE_NAMES

  cat $VDR_CHANNELS |
    while read -r CHAN_NAMES ; do
        ch_name=`echo $CHAN_NAMES | sed -e '/^:/d' | sed -e 's/;.*//g' | sed -e 's/:.*//g'`
        if [ -z "$ch_name" ]; then
          continue
        else
          IS_CHANNEL=$(find $SOURCE_DIR_LOGOS -iname "$ch_name.png")
          IS_CHANNEL_LIST=$(grep "$IS_CHANNEL" $SOURCE_FILE_NAMES)
          [ "$IS_CHANNEL" != "" -a "$IS_CHANNEL_LIST" == "" ] && echo "$IS_CHANNEL" >> $SOURCE_FILE_NAMES
        fi
    done

# Convert downloaded logos
elif [ "$1" == "convert" ] ; then
  rm -f $LOG_FILE
  touch $LOG_FILE
  mkdir -p $LOGOS_DIR
  [ "$LOGOS_CLEAR" == "1" ] && rm -rf $LOGOS_DIR/*

  cat $SOURCE_FILE_NAMES |
      while read -r FILE_NAMES ; do
          file=$(echo $FILE_NAMES)
          channel=$(basename "$file")
          echo_channel=$(echo "$channel" | sed -e 's/\.png$//')
          lcase_file=$(echo "$channel" | tr 'A-Z' 'a-z')
          target_file="$LOGOS_DIR$lcase_file"
          echo "Convertion logo: $echo_channel" > $LOG_FILE
          if [ ! -f "$target_file" ] ; then
              convert +dither -background 'transparent' -resize $RESIZE -extent $EXTENT -gravity 'center' "$file" png:- 2> /dev/null | \
              composite - $BACKGROUND png:- 2> /dev/null | \
              composite -compose screen -blend 50x100 $FOREGROUND - "$target_file" 2> /dev/null
          fi
     done
  echo "Conversion logos completed." > $LOG_FILE

# Missing logos count
elif [ "$1" == "misslist" ] ; then
  rm -f $MISS_FILE
  cat $VDR_CHANNELS |
    while read -r CHAN_NAMES ; do
        ch_name=`echo $CHAN_NAMES | sed -e '/^:/d' | sed -e 's/;.*//g' | sed -e 's/:.*//g'`
        if [ -z "$ch_name" ]; then
          continue
        else
          lcase_name=$(echo "$ch_name" | tr 'A-Z' 'a-z' | sed 's/\// /')
          target_file="$LOGOS_DIR$lcase_name.png"

          if [ ! -f "$target_file" ] ; then
              echo "$target_file" >> $MISS_FILE
          fi
        fi
    done

# Generating the missing logos
elif [ "$1" == "missing" ] ; then
  rm -f $LOG_FILE
  touch $LOG_FILE
  rm -rf $OUTPUT_DIR_TEMP
  mkdir -p $OUTPUT_DIR_TEMP

  cat $VDR_CHANNELS |
    while read -r CHAN_NAMES ; do
      ch_name=`echo $CHAN_NAMES | sed -e '/^:/d' | sed -e 's/;.*//g' | sed -e 's/:.*//g'`
      if [ -z "$ch_name" ]; then
          continue
      else
          lcase_name=$(echo "$ch_name" | tr 'A-Z' 'a-z' | sed 's/\// /')
          target_file="$LOGOS_DIR$lcase_name.png"
          tmp_file="$OUTPUT_DIR_TEMP/$lcase_name.png"
          ch_text=$(echo "$ch_name" | sed 's/[ \t]*$//;s/ /\\n/g')

          if [ ! -f "$target_file" ] ; then
              echo "Create missing logo: $ch_name" > $LOG_FILE
              montage \
                  -size 268x200 \
                  -background none \
                  -gravity center \
                  -fill $LOGOS_TEXT_COLOR \
                  -font Open-Sans \
                  label:"$ch_text" +set label \
                  -shadow \
                  -background transparent \
                  -geometry +5+5 \
                  "$tmp_file" 2> /dev/null

              convert +dither -background 'transparent' -resize $RESIZE -extent $EXTENT -gravity 'center' "$tmp_file" png:- 2> /dev/null | \
              composite - $BACKGROUND png:- 2> /dev/null | \
              composite -compose screen -blend 50x100 $FOREGROUND - "$target_file" 2> /dev/null
          fi
      fi
    done
    rm -rf $OUTPUT_DIR_TEMP
    rm -rf $SOURCE_DIR
    echo "Create logos completed." > $LOG_FILE
fi

exit 0
