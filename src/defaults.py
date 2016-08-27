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

about = {'ENABLED': True}

xdbus = {'ENABLED': True}

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
    'acestream' : ['acestream.service'],
    'aceproxy' : ['aceproxy.service'],
    }
