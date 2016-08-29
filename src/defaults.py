################################################################################
#      This file is part of Alex@ELEC - http://www.alexelec.in.ua
#      Copyright (C) 2011-2016 Alexandr Zuyev (alex@alexelec.in.ua)
################################################################################
# -*- coding: utf-8 -*-

import os
import xbmc
import xbmcaddon

__scriptid__ = 'service.alexelec.settings'
__addon__ = xbmcaddon.Addon(id=__scriptid__)
__cwd__ = __addon__.getAddonInfo('path')

################################################################################
# Base
################################################################################

XBMC_USER_HOME = os.environ.get('XBMC_USER_HOME', '/storage/.kodi')
CONFIG_CACHE = os.environ.get('CONFIG_CACHE', '/storage/.cache')
USER_CONFIG = os.environ.get('USER_CONFIG', '/storage/.config')

SCRIPT_DIR = '%s/resources/bin' % __cwd__

################################################################################
# Connamn Module
################################################################################

connman = {
    'CONNMAN_DAEMON': '/usr/sbin/connmand',
    'WAIT_CONF_FILE': '%s/alexelec/network_wait' % CONFIG_CACHE,
    'ENABLED': lambda : (True if os.path.exists(connman['CONNMAN_DAEMON']) else False),
    }

################################################################################
# Bluez Module
################################################################################

bluetooth = {
    'BLUETOOTH_DAEMON': '/usr/lib/bluetooth/bluetoothd',
    'OBEX_DAEMON': '/usr/lib/bluetooth/obexd',
    'ENABLED': lambda : (True if os.path.exists(bluetooth['BLUETOOTH_DAEMON']) else False),
    'D_OBEXD_ROOT': '/storage/downloads/',
    }

################################################################################
# Service Module
################################################################################

services = {
    'ENABLED': True,
    'KERNEL_CMD': '/proc/cmdline',
    'SAMBA_NMDB': '/usr/bin/nmbd',
    'SAMBA_SMDB': '/usr/bin/smbd',
    'D_SAMBA_SECURE': '0',
    'D_SAMBA_USERNAME': 'alexelec',
    'D_SAMBA_PASSWORD': 'alexelec',
    'D_SAMBA_AUTOSHARE': '1',
    'SSH_DAEMON': '/usr/sbin/sshd',
    'OPT_SSH_NOPASSWD': "-o 'PasswordAuthentication no'",
    'D_SSH_DISABLE_PW_AUTH': '0',
    'AVAHI_DAEMON': '/usr/sbin/avahi-daemon',
    'CRON_DAEMON': '/sbin/crond',
    'LCD_DRIVER_DIR': '/usr/lib/lcdproc/',
    'D_LCD_DRIVER': 'none',
    'D_RAMCLEAR_TIME': '5',
    'D_VNC_DEBUG': '0',
    'D_VNC_PORT': '5900',
    'D_VNC_PASSWORD': 'alexelec',
    }

system = {
    'ENABLED': True,
    'KERNEL_CMD': '/proc/cmdline',
    'SET_CLOCK_CMD': '/sbin/hwclock --systohc --utc',
    'GET_CPU_FLAG': "cat /proc/cpuinfo | grep -q 'flags.* lm ' && echo '1' || echo '0'",
    'KODI_RESET_FILE': '%s/reset_kodi' % CONFIG_CACHE,
    'ALEXELEC_RESET_FILE': '%s/reset_ae' % CONFIG_CACHE,
    'KEYBOARD_INFO': '/usr/share/X11/xkb/rules/base.xml',
    'UDEV_KEYBOARD_INFO': '%s/xkb/layout' % CONFIG_CACHE,
    'NOX_KEYBOARD_INFO': '/usr/lib/keymaps',
    'BACKUP_DIRS': [
        XBMC_USER_HOME,
        USER_CONFIG,
        CONFIG_CACHE,
        '/storage/.ssh',
        ],
    'BACKUP_DESTINATION': '/storage/backup/',
    'RESTORE_DIR': '/storage/.restore/',
    'D_SYS_LOCALE': 'ru_RU.utf8',
    'GET_SYS_LOCALE': "/usr/bin/locale -a > /tmp/locale.tmp",
    'SYS_LOCALE_LIST': '/tmp/locale.tmp',
    'SND_DEV_LIST': "aplay -l | grep card | awk -F'[' '{print $1,$2}' |sed 's/]//; s/://g' > /tmp/sndlist.tmp",
    'SND_LIST_TEMP': '/tmp/sndlist.tmp',
    'SND_TEST': "speaker-test -D plughw:%d,%d -c2 -t wav",
    'SND_FILE_RUN': '%s/sound.sh' % SCRIPT_DIR,
    'D_DISABLE_CURSOR': '0',
    }

about = {'ENABLED': True}

xdbus = {'ENABLED': True}

################################################################################
# AceStream & AceProxy Module
################################################################################

ace = {
    'ENABLED': True,
    #ACESTREAM
    'D_ACE_CACHE_TYPE'        : 'memory',
    'D_ACE_CACHE_LIMIT'       : '5',
    'D_ACE_LIFE_CACHE_SIZE'   : '20971520',
    'D_ACE_LIFE_BUFFER'       : '60',
    'D_ACE_CACHE_DIR'         : '/storage/.ACEStream/.acestream_cache',
    'D_ACE_CLEAN_CACHE'       : '0',
    'D_ACE_DEBUG'             : '0',
    'D_ACE_LOGIN'             : '',
    'D_ACE_PASSW'             : '',
    'D_ACE_ALWAYS'            : '0',
    #ACEPROXY
    'D_ACEPROXY_LOGIN'  : '',
    'D_ACEPROXY_PASSW'  : '',
    'D_ACEPROXY_DEBUG'  : 'INFO',
    'D_ACEPROXY_ALWAYS' : '0',
    }

################################################################################
# DVB device Module
################################################################################

dvbdev = {
    'ENABLED': True,
    'GET_DVB_FRONTEND' : "%s/frontend.sh" % SCRIPT_DIR,
    'GET_DVB_DRIVER'   : "ls -l /storage/.modules/* | awk -F\/ '{print $7}' |  awk -F\- '{print $2}'",
    'D_DVB_DRIVERS'    : 'CORE',
    'GET_DVB_DRVLIST'  : "%s/dvbdrv.sh" % SCRIPT_DIR,
    'DVB_LIST_TEMP'    : "/tmp/dvb-drv.tmp",
    #WAIT DVB FRONTEND
    'COUNT_DVB'        : "ls -1 /dev/dvb/adapter*/frontend* | wc -l",
    'D_DVB_NUMBER'     : '0',
    'D_DVB_TIME'       : '5',
    }

################################################################################
# CAMD server Module
################################################################################

camd = {
    'ENABLED'        : True,
    'D_WICARD_TYPE'  : 'TVON',
    'D_WICARD_DEBUG' : '0',
    'D_OSCAM_TYPE'   : 'TVON',
    }

################################################################################
# TV-Backend Module
################################################################################

tvbackend = {
    'ENABLED'        : True,
    #VDR BACKEND
    'D_BVDR_DEBUG'             : '0',
    'D_BVDR_VIDEO_DIR'         : '/storage/recordings/',
    'D_BVDR_DVBAPI'            : '1',
    'D_BVDR_PVR'               : 'xvdr',
    'D_BVDR_IPTV'              : '0',
    'D_BVDR_IPTV_DEVICES'      : '1',
    'D_BVDR_SATIP'             : '0',
    'D_BVDR_STREAMDEV_SERVER'  : '0',
    'D_BVDR_STREAMDEV_CLIENT'  : '0',
    'D_BVDR_CHSCAN'            : '0',
    'D_BVDR_LIVE'              : '0',
    #TVHEADEND BACKEND
    'D_TVH_DEBUG'              : '0',
    'D_TVH_BACKUP'             : '0',
    'D_TVH_BINDADDR'           : 'All',
    'D_TVH_TIMEOUT'            : '5',
    'FILE_TVH_BINDADDR'        : '/tmp/tvh-bindaddr.tmp',
    'GET_TVH_BINDADDR'         : "ifconfig | awk  '/inet addr:/ {print $2}' | sed 's/addr://' > /tmp/tvh-bindaddr.tmp",
    }

################################################################################
# VDR Frontend Module
################################################################################

tvshell = {
    'ENABLED'         : True,
    #VDR START
    'D_VDR_SHELL'     : '0',
    'D_VDR_DEBUG'     : '0',
    'D_VDR_VIDEO_DIR' : '/storage/recordings/',

    #VDR PLUGINS
    'D_VDR_DVBAPI'            : '1',
    'D_VDR_IPTV'              : '0',
    'D_VDR_IPTV_DEVICES'      : '1',
    'D_VDR_SATIP'             : '0',
    'D_VDR_EPGSEARCH'         : '1',
    'D_VDR_STREAMDEV_SERVER'  : '0',
    'D_VDR_STREAMDEV_CLIENT'  : '0',
    'D_VDR_CHSCAN'            : '0',
    'D_VDR_FEMON'             : '1',
    'D_VDR_SYSINFO'           : '1',
    'D_VDR_SLEEP'             : '0',
    'D_VDR_PVR'               : 'none',
    'D_VDR_TVSCRAPER'         : '0',
    'D_VDR_SKIN_NOPACITY'     : '0',
    'D_VDR_WEATHER'           : '0',
    'D_VDR_SKIN_DESIGNER'     : '0',
    'D_VDR_TVGUIDENG'         : '0',
    'D_VDR_ZAPHISTORY'        : '0',
    'D_VDR_LIVE'              : '0',

    #VDR LOGOS
    'URL_LOGOS_FILE'      : "http://src.alexelec.in.ua/logos/logos.tar.bz2",
    'RUN_LOGOS'           : "%s/logos.sh" % SCRIPT_DIR,
    'GET_LOGO_COUNT'      : "wc -l /storage/.kodi/temp/logos_src/src_file.tmp | awk '{print $1}'",
    'GET_MISS_COUNT'      : "wc -l /tmp/miss_logo.log | awk '{print $1}'",
    'LOGO_GET_LOG'        : "tail -n1 /tmp/logo_conv.log",
    'KILL_LOGO_SH'        : "killall -9 logos.sh",
    'D_LOGOS_DIR'         : '/storage/.config/vdr/plugins/skindesigner/logos/',
    'D_LOGOS_CLEAR'       : '0',
    'D_LOGOS_BG_COLOR'    : 'White',
    'D_LOGOS_FG_COLOR'    : '4',
    'D_LOGOS_TEXT_COLOR'  : 'black',
    }

################################################################################
# VDR Scan channels Module
################################################################################

scan = {
    'ENABLED'           : True,
    'RUN_SCAN'          : "%s/scan-s2.sh" % SCRIPT_DIR,
    'KILL_SCAN'         : "killall -2 scan-s2",
    'TUNER_LIST'        : "%s/frontend.sh" % SCRIPT_DIR,
    'TUNER_LIST_TEMP'   : '/tmp/frontend.tmp',

    'S2_SAT_NAME_FILE'  : '/storage/.config/vdr/sources.conf',
    'S2_SAT_NAME_TEMP'  : '/tmp/satlist.tmp',
    'S2_GET_SAT_NAME'   : "cat /storage/.config/vdr/sources.conf | grep '^S.*' | sed 's/[ \t]*$//' > /tmp/satlist.tmp",
    'S2_TPL_DIR'        : '/storage/.config/scan-s2',
    'S2_GET_TPL_LIST'   : "ls -l /storage/.config/scan-s2/*.cfg | awk '{print $9}' > /tmp/tplist.tmp",
    'S2_TPL_LIST_FILE'  : '/tmp/tplist.tmp',
    'S2_GET_TPL_COUNT'  : "%s/tpl-count.sh" % SCRIPT_DIR,
    'S2_GET_LOG'        : "tail -n1 /tmp/scan-s2.log",
    'S2_DEL_LOG'        : "rm -f /tmp/scan-s2.log",

    #Scan-S2 settings
    'D_S2_TUNER'      : 'none',
    'D_S2_TYPE'       : 'S2',
    'D_S2_LNB'        : '1',
    'D_S2_SAT'        : 'S36.0E  Eutelsat W4/W7',
    'D_S2_POLAR'      : 'Circular',
    'D_S2_FILE'       : 'S36.0E-HTB.cfg',
    'D_S2_SERVICE'    : 'All',
    'D_S2_FTA'        : 'All',
    'D_S2_UPDATE'     : '0',
    'D_S2_SORT'       : '1',
    'D_S2_SPEED'      : 'Default',
    }

################################################################################
# VDR DiSEqC config Module
################################################################################

swith = {
    'ENABLED'        : True,
    'SET_DISEQC'     : "%s/diseqc.sh" % SCRIPT_DIR,
    'SAT_NAME_FILE'  : '/storage/.config/vdr/sources.conf',
    'SAT_NAME_TEMP'  : '/tmp/satswith.tmp',
    'GET_SAT_NAME'   : "cat /storage/.config/vdr/sources.conf | grep '^S.*' | sed 's/[ \t]*$//' > /tmp/satswith.tmp",

    #DiSEqC LNB
    'D_LNB1'         : '1',
    'D_LNB2'         : '0',
    'D_LNB3'         : '0',
    'D_LNB4'         : '0',

    #DiSEqC SAT
    'D_SAT1'         : 'S36.0E  Eutelsat W4/W7',
    'D_SAT2'         : 'S4W     Amos 2/3',
    'D_SAT3'         : 'S4.9E   Astra 4A',
    'D_SAT4'         : 'S13E    Hotbird 6/8/9',

    #DiSEqC POLAR
    'D_POLAR1'       : 'Circular',
    'D_POLAR2'       : 'Linear',
    'D_POLAR3'       : 'Linear',
    'D_POLAR4'       : 'Linear',
    }

################################################################################
# Services
################################################################################

_services = {
    'sshd': ['sshd.service'],
    'avahi': ['avahi-daemon.service'],
    'samba': ['nmbd.service', 'smbd.service'],
    'bluez': ['bluetooth.service'],
    'obexd': ['obex.service'],
    'crond': ['cron.service'],
    'lcdd': ['lcdd.service'],
    'mysqld': ['mysqld.service'],
    'minidlna': ['minidlna.service'],
    'ramclear': ['drop-ram.service'],
    'x11vnc': ['x11vnc.service'],
    'acestream': ['acestream.service'],
    'aceproxy': ['aceproxy.service'],
    'wicard': ['wicard.service'],
    'oscam': ['oscam.service'],
    'tvheadend': ['tvheadend.service'],
    'vdr-backend': ['vdr-backend.service'],
    }
