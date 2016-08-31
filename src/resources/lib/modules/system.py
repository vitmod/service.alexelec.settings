################################################################################
#      This file is part of Alex@ELEC - http://www.alexelec.in.ua
#      Copyright (C) 2011-2016 Alexandr Zuyev (alex@alexelec.in.ua)
################################################################################
# -*- coding: utf-8 -*-

import os
import re
import glob
import time
import json
import xbmc
import xbmcgui
import xbmcaddon
import tarfile
import oeWindows
import threading
import subprocess
from xml.dom import minidom


class system:

    ENABLED = False
    KERNEL_CMD = None
    KODI_RESET_FILE = None
    ALEXELEC_RESET_FILE = None
    KEYBOARD_INFO = None
    UDEV_KEYBOARD_INFO = None
    NOX_KEYBOARD_INFO = None
    BACKUP_DIRS = None
    BACKUP_DESTINATION = None
    RESTORE_DIR = None
    GET_CPU_FLAG = None
    SET_CLOCK_CMD = None
    D_SYS_LOCALE = None
    GET_SYS_LOCALE = None
    SYS_LOCALE_LIST = None
    SND_DEV_LIST = None
    SND_LIST_TEMP = None
    SND_TEST = None
    SND_FILE_RUN = None
    D_DISABLE_CURSOR = None
    D_UNCLUTTER_TIME = None

    menu = {'1': {
        'name': 32002,
        'menuLoader': 'load_menu',
        'listTyp': 'list',
        'InfoText': 700,
        }}

    def __init__(self, oeMain):
        try:
            oeMain.dbg_log('system::__init__', 'enter_function', 0)
            self.oe = oeMain
            self.struct = {
                'ident': {
                    'order': 1,
                    'name': 32189,
                    'settings': {'hostname': {
                        'order': 1,
                        'name': 32190,
                        'value': '',
                        'action': 'set_hostname',
                        'type': 'text',
                        'validate': '^([a-zA-Z0-9](?:[a-zA-Z0-9-\.]*[a-zA-Z0-9]))$',
                        'InfoText': 710,
                        }},
                    },
                'keyboard': {
                    'order': 2,
                    'name': 32009,
                    'settings': {
                        'KeyboardLayout1': {
                            'order': 1,
                            'name': 32010,
                            'value': 'us',
                            'action': 'set_keyboard_layout',
                            'type': 'multivalue',
                            'values': [],
                            'InfoText': 711,
                            },
                        'KeyboardVariant1': {
                            'order': 2,
                            'name': 32386,
                            'value': '',
                            'action': 'set_keyboard_layout',
                            'type': 'multivalue',
                            'values': [],
                            'InfoText': 753,
                            },
                        'KeyboardLayout2': {
                            'order': 3,
                            'name': 32010,
                            'value': 'ru',
                            'action': 'set_keyboard_layout',
                            'type': 'multivalue',
                            'values': [],
                            'InfoText': 712,
                            },
                        'KeyboardVariant2': {
                            'order': 4,
                            'name': 32387,
                            'value': '',
                            'action': 'set_keyboard_layout',
                            'type': 'multivalue',
                            'values': [],
                            'InfoText': 754,
                            },
                        'KeyboardType': {
                            'order': 5,
                            'name': 32330,
                            'value': 'pc105',
                            'action': 'set_keyboard_layout',
                            'type': 'multivalue',
                            'values': [],
                            'InfoText': 713,
                            },
                        },
                    },
                'locale': {
                    'order': 3,
                    'name': 33010,
                    'settings': {
                        'sys_locale': {
                            'order': 1,
                            'name': 33011,
                            'value': 'ru_RU.utf8',
                            'values': [],
                            'action': 'initialize_locale',
                            'type': 'multivalue',
                            'InfoText': 3311,
                            },
                        },
                    },
                'sound': {
                    'order': 4,
                    'name': 33020,
                    'settings': {
                        'snd-dev': {
                            'order': 1,
                            'name': 33021,
                            'value': 'none',
                            'action': 'initialize_sound',
                            'type': 'multivalue',
                            'values': [],
                            'InfoText': 3321,
                            },
                        'snd-test': {
                            'order': 2,
                            'name': 33022,
                            'value': '0',
                            'action': 'test_sound',
                            'type': 'button',
                            'InfoText': 3322,
                            },
                        'snd-file': {
                            'order': 3,
                            'name': 33023,
                            'value': '0',
                            'action': 'file_sound',
                            'type': 'button',
                            'InfoText': 3323,
                            },
                        },
                    },
                'xorg': {
                    'order': 5,
                    'name': 33030,
                    'settings': {
                        'cursor': {
                            'order': 1,
                            'name': 33031,
                            'value': '0',
                            'action': 'initialize_xorg',
                            'type': 'bool',
                            'InfoText': 3331,
                            },
                        },
                    },
                'unclutter': {
                    'order': 6,
                    'name': 33040,
                    'settings': {
                        'unclutter_enable': {
                            'order': 1,
                            'name': 33041,
                            'value': '0',
                            'action': 'initialize_unclutter',
                            'type': 'bool',
                            'InfoText': 3341,
                            },
                        'unclutter_time': {
                            'order': 2,
                            'name': 33042,
                            'value': '2',
                            'values': ['1', '2', '3', '4', '5', '8', '10'],
                            'action': 'initialize_unclutter',
                            'type': 'multivalue',
                            'parent': {
                                'entry': 'unclutter_enable',
                                'value': ['1'],
                                },
                            'InfoText': 3342,
                            },
                        },
                    },
                'backup': {
                    'order': 7,
                    'name': 32371,
                    'settings': {
                        'backup': {
                            'name': 32372,
                            'value': '0',
                            'action': 'do_backup',
                            'type': 'button',
                            'InfoText': 722,
                            'order': 1,
                            },
                        'restore': {
                            'name': 32373,
                            'value': '0',
                            'action': 'do_restore',
                            'type': 'button',
                            'InfoText': 723,
                            'order': 2,
                            },
                        },
                    },
                'reset': {
                    'order': 8,
                    'name': 32323,
                    'settings': {
                        'kodi_reset': {
                            'name': 32324,
                            'value': '0',
                            'action': 'reset_kodi',
                            'type': 'button',
                            'InfoText': 724,
                            'order': 1,
                            },
                        'ae_reset': {
                            'name': 32325,
                            'value': '0',
                            'action': 'reset_ae',
                            'type': 'button',
                            'InfoText': 725,
                            'order': 2,
                            },
                        },
                    },
                }

            self.keyboard_layouts = False
            self.nox_keyboard_layouts = False
            self.arrVariants = {}
            self.oe.dbg_log('system::__init__', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('system::__init__', 'ERROR: (' + repr(e) + ')')

    def start_service(self):
        try:
            self.oe.dbg_log('system::start_service', 'enter_function', 0)
            self.is_service = True
            self.load_values()
            self.set_hostname()
            self.set_keyboard_layout()
            self.set_hw_clock()
            self.initialize_locale(service=1)
            self.initialize_sound()
            self.initialize_xorg(service=1)
            self.initialize_unclutter(service=1)
            del self.is_service
            self.oe.dbg_log('system::start_service', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('system::start_service', 'ERROR: (' + repr(e) + ')')

    def stop_service(self):
        try:
            self.oe.dbg_log('system::stop_service', 'enter_function', 0)
            if hasattr(self, 'update_thread'):
                self.update_thread.stop()
            self.oe.dbg_log('system::stop_service', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('system::stop_service', 'ERROR: (' + repr(e) + ')')

    def do_init(self):
        try:
            self.oe.dbg_log('system::do_init', 'enter_function', 0)
            self.oe.dbg_log('system::do_init', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('system::do_init', 'ERROR: (' + repr(e) + ')')

    def exit(self):
        self.oe.dbg_log('system::exit', 'enter_function', 0)
        self.oe.dbg_log('system::exit', 'exit_function', 0)
        pass

    def load_values(self):
        try:
            self.oe.dbg_log('system::load_values', 'enter_function', 0)

            # CPU x64 flag

            self.cpu_lm_flag = self.oe.execute(self.GET_CPU_FLAG, 1)

            # Keyboard Layout

            (
                arrLayouts,
                arrTypes,
                self.arrVariants,
                ) = self.get_keyboard_layouts()
            if not arrTypes is None:
                self.struct['keyboard']['settings']['KeyboardType']['values'] = arrTypes
                value = self.oe.read_setting('system', 'KeyboardType')
                if not value is None:
                    self.struct['keyboard']['settings']['KeyboardType']['value'] = value
            if not arrLayouts is None:
                self.struct['keyboard']['settings']['KeyboardLayout1']['values'] = arrLayouts
                self.struct['keyboard']['settings']['KeyboardLayout2']['values'] = arrLayouts
                value = self.oe.read_setting('system', 'KeyboardLayout1')
                if not value is None:
                    self.struct['keyboard']['settings']['KeyboardLayout1']['value'] = value
                value = self.oe.read_setting('system', 'KeyboardVariant1')
                if not value is None:
                    self.struct['keyboard']['settings']['KeyboardVariant1']['value'] = value
                value = self.oe.read_setting('system', 'KeyboardLayout2')
                if not value is None:
                    self.struct['keyboard']['settings']['KeyboardLayout2']['value'] = value
                value = self.oe.read_setting('system', 'KeyboardVariant2')
                if not value is None:
                    self.struct['keyboard']['settings']['KeyboardVariant2']['value'] = value
                if not arrTypes == None:
                    self.keyboard_layouts = True

            if not os.path.exists('/usr/bin/setxkbmap'):
                self.struct['keyboard']['settings']['KeyboardLayout2']['hidden'] = 'true'
                self.struct['keyboard']['settings']['KeyboardType']['hidden'] = 'true'
                self.struct['keyboard']['settings']['KeyboardVariant1']['hidden'] = 'true'
                self.struct['keyboard']['settings']['KeyboardVariant2']['hidden'] = 'true'
                self.nox_keyboard_layouts = True

            # Hostname

            value = self.oe.read_setting('system', 'hostname')
            if not value is None:
                self.struct['ident']['settings']['hostname']['value'] = value
            else:
                self.struct['ident']['settings']['hostname']['value'] = self.oe.DISTRIBUTION

            # Load system Locale list
            arrLocale = self.get_sys_locale()
            if not arrLocale is None:
                self.struct['locale']['settings']['sys_locale']['values'] = arrLocale

            self.struct['locale']['settings']['sys_locale']['value'] = \
            self.oe.get_service_option('locale', 'SYS_LOCALE', self.D_SYS_LOCALE).replace('"', '')

            # Load Sound devices list
            arrSndDev = self.get_sound_dev()
            if not arrSndDev is None:
                self.struct['sound']['settings']['snd-dev']['values'] = arrSndDev
                value = self.oe.read_setting('system', 'snd-dev')
                if not value is None:
                    self.struct['sound']['settings']['snd-dev']['value'] = value

            # Xorg mouse cursor
            self.struct['xorg']['settings']['cursor']['value'] = \
            self.oe.get_service_option('xorg', 'DISABLE_CURSOR', self.D_DISABLE_CURSOR).replace('"', '')

            # Unclutter
            self.struct['unclutter']['settings']['unclutter_enable']['value'] = self.oe.get_service_state('unclutter')
            self.struct['unclutter']['settings']['unclutter_time']['value'] = \
            self.oe.get_service_option('unclutter', 'UNCLUTTER_TIME', self.D_UNCLUTTER_TIME).replace('"', '')

            self.oe.dbg_log('system::load_values', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('system::load_values', 'ERROR: (' + repr(e) + ')')

    def load_menu(self, focusItem):
        try:
            self.oe.dbg_log('system::load_menu', 'enter_function', 0)
            self.oe.winOeMain.build_menu(self.struct)
            self.oe.dbg_log('system::load_menu', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('system::loadSysMenu', 'ERROR: (' + repr(e) + ')')

    def set_value(self, listItem):
        try:
            self.oe.dbg_log('system::set_value', 'enter_function', 0)
            self.struct[listItem.getProperty('category')]['settings'][listItem.getProperty('entry')]['value'] = listItem.getProperty('value')
            self.oe.write_setting('system', listItem.getProperty('entry'), unicode(listItem.getProperty('value')))
            self.oe.dbg_log('system::set_value', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('system::set_value', 'ERROR: (' + repr(e) + ')')

    def set_keyboard_layout(self, listItem=None):
        try:
            self.oe.dbg_log('system::set_keyboard_layout', 'enter_function', 0)
            if not listItem == None:
                if listItem.getProperty('entry') == 'KeyboardLayout1':
                    if self.struct['keyboard']['settings']['KeyboardLayout1']['value'] != listItem.getProperty('value'):
                        self.struct['keyboard']['settings']['KeyboardVariant1']['value'] = ''
                if listItem.getProperty('entry') == 'KeyboardLayout2':
                    if self.struct['keyboard']['settings']['KeyboardLayout2']['value'] != listItem.getProperty('value'):
                        self.struct['keyboard']['settings']['KeyboardVariant2']['value'] = ''
                self.set_value(listItem)
            if self.keyboard_layouts == True:
                self.struct['keyboard']['settings']['KeyboardVariant1']['values'] = self.arrVariants[self.struct['keyboard']['settings'
                        ]['KeyboardLayout1']['value']]
                self.struct['keyboard']['settings']['KeyboardVariant2']['values'] = self.arrVariants[self.struct['keyboard']['settings'
                        ]['KeyboardLayout2']['value']]
                self.oe.dbg_log('system::set_keyboard_layout', unicode(self.struct['keyboard']['settings']['KeyboardLayout1']['value']) + ','
                                + unicode(self.struct['keyboard']['settings']['KeyboardLayout2']['value']) + ' ' + '-model '
                                + unicode(self.struct['keyboard']['settings']['KeyboardType']['value']), 1)
                if not os.path.exists(os.path.dirname(self.UDEV_KEYBOARD_INFO)):
                    os.makedirs(os.path.dirname(self.UDEV_KEYBOARD_INFO))
                config_file = open(self.UDEV_KEYBOARD_INFO, 'w')
                config_file.write('XKBMODEL="' + self.struct['keyboard']['settings']['KeyboardType']['value'] + '"\n')
                config_file.write('XKBVARIANT="%s,%s"\n' % (self.struct['keyboard']['settings']['KeyboardVariant1']['value'],
                                  self.struct['keyboard']['settings']['KeyboardVariant2']['value']))
                config_file.write('XKBLAYOUT="' + self.struct['keyboard']['settings']['KeyboardLayout1']['value'] + ',' + self.struct['keyboard'
                                  ]['settings']['KeyboardLayout2']['value'] + '"\n')
                config_file.write('XKBOPTIONS="grp:alt_shift_toggle"\n')
                config_file.close()
                parameters = [
                    '-display ' + os.environ['DISPLAY'],
                    '-layout ' + self.struct['keyboard']['settings']['KeyboardLayout1']['value'] + ',' + self.struct['keyboard']['settings'
                            ]['KeyboardLayout2']['value'],
                    '-variant ' + self.struct['keyboard']['settings']['KeyboardVariant1']['value'] + ',' + self.struct['keyboard']['settings'
                            ]['KeyboardVariant2']['value'],
                    '-model ' + unicode(self.struct['keyboard']['settings']['KeyboardType']['value']),
                    '-option "grp:alt_shift_toggle"',
                    ]
                self.oe.execute('setxkbmap ' + ' '.join(parameters))
            elif self.nox_keyboard_layouts == True:
                self.oe.dbg_log('system::set_keyboard_layout', unicode(self.struct['keyboard']['settings']['KeyboardLayout1']['value']), 1)
                parameter = self.struct['keyboard']['settings']['KeyboardLayout1']['value']
                command = 'loadkmap < `ls -1 %s/*/%s.bmap`' % (self.NOX_KEYBOARD_INFO, parameter)
                self.oe.dbg_log('system::set_keyboard_layout', command, 1)
                self.oe.execute(command)
            self.oe.dbg_log('system::set_keyboard_layout', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('system::set_keyboard_layout', 'ERROR: (' + repr(e) + ')')

    def set_hostname(self, listItem=None):
        try:
            self.oe.dbg_log('system::set_hostname', 'enter_function', 0)
            self.oe.set_busy(1)
            if not listItem == None:
                self.set_value(listItem)
            if not self.struct['ident']['settings']['hostname']['value'] is None and not self.struct['ident']['settings']['hostname']['value'] \
                == '':
                self.oe.dbg_log('system::set_hostname', self.struct['ident']['settings']['hostname']['value'], 1)
                hostname = open('/proc/sys/kernel/hostname', 'w')
                hostname.write(self.struct['ident']['settings']['hostname']['value'])
                hostname.close()
                hostname = open('%s/hostname' % self.oe.CONFIG_CACHE, 'w')
                hostname.write(self.struct['ident']['settings']['hostname']['value'])
                hostname.close()
                hosts = open('/etc/hosts', 'w')
                user_hosts_file = os.environ['HOME'] + '/.config/hosts.conf'
                if os.path.isfile(user_hosts_file):
                    user_hosts = open(user_hosts_file, 'r')
                    hosts.write(user_hosts.read())
                    user_hosts.close()
                hosts.write('127.0.0.1\tlocalhost %s\n' % self.struct['ident']['settings']['hostname']['value'])
                hosts.write('::1\tlocalhost ip6-localhost ip6-loopback %s\n' % self.struct['ident']['settings']['hostname']['value'])
                hosts.close()
            else:
                self.oe.dbg_log('system::set_hostname', 'is empty', 1)
            self.oe.set_busy(0)
            self.oe.dbg_log('system::set_hostname', 'exit_function', 0)
        except Exception, e:
            self.oe.set_busy(0)
            self.oe.dbg_log('system::set_hostname', 'ERROR: (' + repr(e) + ')')

    def get_keyboard_layouts(self):
        try:
            self.oe.dbg_log('system::get_keyboard_layouts', 'enter_function', 0)
            arrLayouts = []
            arrVariants = {}
            arrTypes = []
            if os.path.exists(self.KEYBOARD_INFO):
                objXmlFile = open(self.KEYBOARD_INFO, 'r')
                strXmlText = objXmlFile.read()
                objXmlFile.close()
                xml_conf = minidom.parseString(strXmlText)
                for xml_layout in xml_conf.getElementsByTagName('layout'):
                    for subnode_1 in xml_layout.childNodes:
                        if subnode_1.nodeName == 'configItem':
                            for subnode_2 in subnode_1.childNodes:
                                if subnode_2.nodeName == 'name':
                                    if hasattr(subnode_2.firstChild, 'nodeValue'):
                                        value = subnode_2.firstChild.nodeValue
                                if subnode_2.nodeName == 'description':
                                    if hasattr(subnode_2.firstChild, 'nodeValue'):
                                        arrLayouts.append(subnode_2.firstChild.nodeValue + ':' + value)
                        if subnode_1.nodeName == 'variantList':
                            arrVariants[value] = [':']
                            for subnode_vl in subnode_1.childNodes:
                                if subnode_vl.nodeName == 'variant':
                                    for subnode_v in subnode_vl.childNodes:
                                        if subnode_v.nodeName == 'configItem':
                                            for subnode_ci in subnode_v.childNodes:
                                                if subnode_ci.nodeName == 'name':
                                                    if hasattr(subnode_ci.firstChild, 'nodeValue'):
                                                        vvalue = subnode_ci.firstChild.nodeValue.replace(',', '')
                                                if subnode_ci.nodeName == 'description':
                                                    if hasattr(subnode_ci.firstChild, 'nodeValue'):
                                                        try:
                                                            arrVariants[value].append(subnode_ci.firstChild.nodeValue + ':' + vvalue)
                                                        except:
                                                            pass
                for xml_layout in xml_conf.getElementsByTagName('model'):
                    for subnode_1 in xml_layout.childNodes:
                        if subnode_1.nodeName == 'configItem':
                            for subnode_2 in subnode_1.childNodes:
                                if subnode_2.nodeName == 'name':
                                    if hasattr(subnode_2.firstChild, 'nodeValue'):
                                        value = subnode_2.firstChild.nodeValue
                                if subnode_2.nodeName == 'description':
                                    if hasattr(subnode_2.firstChild, 'nodeValue'):
                                        arrTypes.append(subnode_2.firstChild.nodeValue + ':' + value)
                arrLayouts.sort()
                arrTypes.sort()
            elif os.path.exists(self.NOX_KEYBOARD_INFO):
                for layout in glob.glob(self.NOX_KEYBOARD_INFO + '/*/*.bmap'):
                    if os.path.isfile(layout):
                        arrLayouts.append(layout.split('/')[-1].split('.')[0])
                arrLayouts.sort()
                arrTypes = None
            else:
                self.oe.dbg_log('system::get_keyboard_layouts', 'exit_function (no keyboard layouts found)', 0)
                return (None, None)
            self.oe.dbg_log('system::get_keyboard_layouts', 'exit_function', 0)
            return (
                arrLayouts,
                arrTypes,
                arrVariants,
                )
        except Exception, e:
            self.oe.dbg_log('system::get_keyboard_layouts', 'ERROR: (' + repr(e) + ')')

    def set_hw_clock(self):
        try:
            self.oe.dbg_log('system::set_hw_clock', 'enter_function', 0)
            self.oe.execute(self.SET_CLOCK_CMD)
            self.oe.dbg_log('system::set_hw_clock', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('system::set_hw_clock', 'ERROR: (' + repr(e) + ')', 4)

    def reset_kodi(self, listItem=None):
        try:
            self.oe.dbg_log('system::reset_kodi', 'enter_function', 0)
            if self.ask_sure_reset('KODI') == 1:
                self.oe.set_busy(1)
                reset_file = open(self.KODI_RESET_FILE, 'w')
                reset_file.write('reset')
                reset_file.close()
                self.oe.winOeMain.close()
                time.sleep(1)
                xbmc.executebuiltin('Reboot')
            self.oe.set_busy(0)
            self.oe.dbg_log('system::reset_kodi', 'exit_function', 0)
        except Exception, e:
            self.oe.set_busy(0)
            self.oe.dbg_log('system::reset_kodi', 'ERROR: (' + repr(e) + ')', 4)

    def reset_ae(self, listItem=None):
        try:
            self.oe.dbg_log('system::reset_ae', 'enter_function', 0)
            if self.ask_sure_reset('AlexELEC') == 1:
                self.oe.set_busy(1)
                reset_file = open(self.ALEXELEC_RESET_FILE, 'w')
                reset_file.write('reset')
                reset_file.close()
                self.oe.winOeMain.close()
                time.sleep(1)
                xbmc.executebuiltin('Reboot')
                self.oe.set_busy(0)
            self.oe.dbg_log('system::reset_ae', 'exit_function', 0)
        except Exception, e:
            self.oe.set_busy(0)
            self.oe.dbg_log('system::reset_ae', 'ERROR: (' + repr(e) + ')', 4)

    def ask_sure_reset(self, part):
        try:
            self.oe.dbg_log('system::ask_sure_reset', 'enter_function', 0)
            xbmcDialog = xbmcgui.Dialog()
            answer = xbmcDialog.yesno(part + ' reset', self.oe._(32326).encode('utf-8'), self.oe._(32328).encode('utf-8'))
            if answer == 1:
                if self.oe.reboot_counter(30, self.oe._(32323)) == 1:
                    return 1
                else:
                    return 0
            self.oe.dbg_log('system::reset_oeask_sure_reset', 'exit_function', 0)
        except Exception, e:
            self.oe.set_busy(0)
            self.oe.dbg_log('system::ask_sure_reset', 'ERROR: (' + repr(e) + ')', 4)

    def do_backup(self, listItem=None):
        try:
            self.oe.dbg_log('system::do_backup', 'enter_function', 0)
            self.total_backup_size = 1
            self.done_backup_size = 1

            try:
                self.oe.set_busy(1)
                for directory in self.BACKUP_DIRS:
                    self.get_folder_size(directory)
                self.oe.set_busy(0)
            except:
                self.oe.set_busy(0)

            xbmcDialog = xbmcgui.Dialog()
            bckDir = xbmcDialog.browse( 0, 
                                        self.oe._(32392).encode('utf-8'), 
                                        'files', 
                                        '', 
                                        False, 
                                        False, 
                                        self.BACKUP_DESTINATION )

            if bckDir and os.path.exists(bckDir): 
                # free space check
                try:
                    folder_stat = os.statvfs("/storage")
                    free_space = folder_stat.f_bsize * folder_stat.f_bavail
                    if self.total_backup_size > free_space:
                        txt = self.oe.split_dialog_text(self.oe._(32379).encode('utf-8'))
                        xbmcDialog = xbmcgui.Dialog()
                        answer = xbmcDialog.ok('Backup', txt[0], txt[1], txt[2])
                        return 0
                except:
                    pass
                    
                self.backup_dlg = xbmcgui.DialogProgress()
                self.backup_dlg.create('LibreELEC', self.oe._(32375).encode('utf-8'), ' ', ' ')
                if not os.path.exists(self.BACKUP_DESTINATION):
                    os.makedirs(self.BACKUP_DESTINATION)
                self.backup_file = self.oe.timestamp() + '.tar'
                tar = tarfile.open(bckDir + self.backup_file, 'w')
                for directory in self.BACKUP_DIRS:
                    self.tar_add_folder(tar, directory)
                tar.close()
                self.backup_dlg.close()
                del self.backup_dlg
            self.oe.dbg_log('system::do_backup', 'exit_function', 0)

        except Exception, e:
            self.backup_dlg.close()
            self.oe.dbg_log('system::do_backup', 'ERROR: (' + repr(e) + ')')

    def do_restore(self, listItem=None):
        try:
            self.oe.dbg_log('system::do_restore', 'enter_function', 0)
            copy_success = 0
            xbmcDialog = xbmcgui.Dialog()
            restore_file_path = xbmcDialog.browse( 1, 
                                              self.oe._(32393).encode('utf-8'), 
                                              'files', 
                                              '??????????????.tar', 
                                              False, 
                                              False, 
                                              self.BACKUP_DESTINATION )
            
            restore_file_name = restore_file_path.split('/')[-1]
            
            if not os.path.exists(self.RESTORE_DIR):
                os.makedirs(self.RESTORE_DIR)
            else:
                self.oe.execute('rm -rf %s' % self.RESTORE_DIR)
                os.makedirs(self.RESTORE_DIR)
            folder_stat = os.statvfs(self.RESTORE_DIR)
            file_size = os.path.getsize(restore_file_path)
            free_space = folder_stat.f_bsize * folder_stat.f_bavail
            if free_space > file_size * 2:
                if os.path.exists(self.RESTORE_DIR + restore_file_name):
                    os.remove(self.RESTORE_DIR + restore_file_name)
                if self.oe.copy_file(restore_file_path, self.RESTORE_DIR + restore_file_name) != None:
                    copy_success = 1
                else:
                    self.oe.execute('rm -rf %s' % self.RESTORE_DIR)
            else:
                txt = self.oe.split_dialog_text(self.oe._(32379).encode('utf-8'))
                xbmcDialog = xbmcgui.Dialog()
                answer = xbmcDialog.ok('Restore', txt[0], txt[1], txt[2])
            if copy_success == 1:
                txt = self.oe.split_dialog_text(self.oe._(32380).encode('utf-8'))
                xbmcDialog = xbmcgui.Dialog()
                answer = xbmcDialog.yesno('Restore', txt[0], txt[1], txt[2])
                if answer == 1:
                    if self.oe.reboot_counter(10, self.oe._(32371)) == 1:
                        self.oe.winOeMain.close()
                        time.sleep(1)
                        xbmc.executebuiltin('Reboot')
                else:
                    self.oe.dbg_log('system::do_restore', 'User Abort!', 0)
                    self.oe.execute('rm -rf %s' % self.RESTORE_DIR)
            self.oe.dbg_log('system::do_restore', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('system::do_restore', 'ERROR: (' + repr(e) + ')')

    def tar_add_folder(self, tar, folder):
        try:
            for item in os.listdir(folder):
                if item == self.backup_file:
                    continue
                if self.backup_dlg.iscanceled():
                    try:
                        os.remove(self.BACKUP_DESTINATION + self.backup_file)
                    except:
                        pass
                    return 0
                itempath = os.path.join(folder, item)
                if os.path.islink(itempath):
                    tar.add(itempath)
                elif os.path.ismount(itempath):
                    tar.add(itempath, recursive=False)
                elif os.path.isdir(itempath):
                    if os.listdir(itempath) == []:
                        tar.add(itempath)
                    else:
                        self.tar_add_folder(tar, itempath)
                else:
                    self.done_backup_size += os.path.getsize(itempath)
                    tar.add(itempath)
                    if hasattr(self, 'backup_dlg'):
                        progress = round(1.0 * self.done_backup_size / self.total_backup_size * 100)
                        self.backup_dlg.update(int(progress), folder, item)
        except Exception, e:
            self.backup_dlg.close()
            self.oe.dbg_log('system::tar_add_folder', 'ERROR: (' + repr(e) + ')')

    def get_folder_size(self, folder):
        for item in os.listdir(folder):
            itempath = os.path.join(folder, item)
            if os.path.isfile(itempath):
                self.total_backup_size += os.path.getsize(itempath)
            elif os.path.ismount(itempath):
                continue
            elif os.path.isdir(itempath):
                self.get_folder_size(itempath)

    def initialize_locale(self, **kwargs):
        try:
            self.oe.dbg_log('locale::initialize_locale', 'enter_function', 0)
            self.oe.set_busy(1)
            if 'listItem' in kwargs:
                self.set_value(kwargs['listItem'])
            options = {}
            state = 1
            options['SYS_LOCALE'] = '"%s"' % self.struct['locale']['settings']['sys_locale']['value']

            self.oe.set_service('locale', options, state)
            self.oe.set_busy(0)
            self.oe.dbg_log('locale::initialize_locale', 'exit_function', 0)
        except Exception, e:
            self.oe.set_busy(0)
            self.oe.dbg_log('locale::initialize_locale', 'ERROR: (' + repr(e) + ')')

    def get_sys_locale(self):
        try:
            self.oe.dbg_log('locale::get_sys_locale', 'enter_function', 0)

            arrSysLocale = []

            self.oe.execute(self.GET_SYS_LOCALE, 0)
            for langs in open(self.SYS_LOCALE_LIST).readlines():
                arrSysLocale.append(langs.strip())

            arrSysLocale.sort()
            self.oe.dbg_log('locale::get_sys_locale', 'exit_function', 0)

            return arrSysLocale
        except Exception, e:
            self.oe.dbg_log('locale::get_sys_locale', 'ERROR: (' + repr(e) + ')')

    def initialize_sound(self, listItem=None):
        try:
            self.oe.dbg_log('sound::initialize_sound', 'enter_function', 0)
            if not listItem == None:
                if listItem.getProperty('entry') == 'snd-dev':
                    if self.struct['sound']['settings']['snd-dev']['value'] != listItem.getProperty('value'):
                        self.struct['sound']['settings']['snd-dev']['value'] = ''
                self.set_value(listItem)

            if 'hidden' in self.struct['sound']:
                del self.struct['sound']['hidden']

            if self.struct['sound']['settings']['snd-dev']['value'] != 'none':
                if 'hidden' in self.struct['sound']['settings']['snd-test']:
                    del self.struct['sound']['settings']['snd-test']['hidden']
                if 'hidden' in self.struct['sound']['settings']['snd-file']:
                    del self.struct['sound']['settings']['snd-file']['hidden']
            else:
                self.struct['sound']['settings']['snd-test']['hidden'] = True
                self.struct['sound']['settings']['snd-file']['hidden'] = True

            self.oe.dbg_log('sound::initialize_sound', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('sound::initialize_sound', 'ERROR: (' + repr(e) + ')')

    def get_sound_dev(self):
        try:
            self.oe.dbg_log('sound::get_sound_dev', 'enter_function', 0)

            arrSound = ['none']
            self.oe.execute(self.SND_DEV_LIST, 0)
            for snddev in open(self.SND_LIST_TEMP).readlines():
                arrSound.append(snddev.strip())

            arrSound.sort()
            self.oe.dbg_log('sound::get_sound_dev', 'exit_function', 0)

            return arrSound
        except Exception, e:
            self.oe.dbg_log('sound::get_sound_dev', 'ERROR: (' + repr(e) + ')')

    def test_sound(self, listItem=None):
        try:
            self.oe.dbg_log('sound::test_sound', 'enter_function', 0)

            str_sound_dev = self.oe.read_setting('system', 'snd-dev')
            if str_sound_dev != 'none':
                xbmc.executebuiltin('PlayerControl(Stop)')
                xbmc.audioSuspend()
                xbmc.enableNavSounds(False)
                time.sleep(2)
                snd_card = re.search('card ([\d]+)', str_sound_dev).group(1)
                snd_dev = re.search('device ([\d]+)', str_sound_dev).group(1)
                subprocess.Popen(self.SND_TEST % (int(snd_card), int(snd_dev)),
                                    shell=True, 
                                    close_fds=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)

                xbmcDialog = xbmcgui.Dialog()
                answer = xbmcDialog.ok('Test Sound', ' ', 'Device: %s' % str_sound_dev)

                self.oe.execute('killall -9 speaker-test', 0)
                time.sleep(1)
                xbmc.audioResume()
                xbmc.enableNavSounds(True)

        except Exception, e:
            self.oe.dbg_log('sound::test_sound', 'ERROR: (' + repr(e) + ')')

    def file_sound(self, listItem=None):
        try:
            self.oe.dbg_log('sound::file_sound', 'enter_function', 0)

            str_sound_dev = self.oe.read_setting('system', 'snd-dev')
            snd_card = re.search('card ([\d]+)', str_sound_dev).group(1)
            snd_dev = re.search('device ([\d]+)', str_sound_dev).group(1)
            if os.path.exists(self.SND_FILE_RUN):
                info_sound = self.oe.execute(self.SND_FILE_RUN + ' %d %d' % (int(snd_card), int(snd_dev)), 1)
                xbmcDialog = xbmcgui.Dialog()
                answer = xbmcDialog.ok('Sound file', ' ',
                            'Create asound.conf file:  %s' % info_sound)

        except Exception, e:
            self.oe.dbg_log('sound::file_sound', 'ERROR: (' + repr(e) + ')')

    def initialize_xorg(self, **kwargs):
        try:
            self.oe.dbg_log('xorg::initialize_xorg', 'enter_function', 0)
            self.oe.set_busy(1)
            if 'listItem' in kwargs:
                self.set_value(kwargs['listItem'])
            options = {}
            state = 1
            options['DISABLE_CURSOR'] = '"%s"' % self.struct['xorg']['settings']['cursor']['value']

            self.oe.set_service('xorg', options, state)
            self.oe.set_busy(0)
            self.oe.dbg_log('xorg::initialize_xorg', 'exit_function', 0)
        except Exception, e:
            self.oe.set_busy(0)
            self.oe.dbg_log('xorg::initialize_xorg', 'ERROR: (' + repr(e) + ')')

    def initialize_unclutter(self, **kwargs):
        try:
            self.oe.dbg_log('services::initialize_unclutter', 'enter_function', 0)
            self.oe.set_busy(1)
            if 'listItem' in kwargs:
                self.set_value(kwargs['listItem'])
            state = 0
            options = {}
            if self.struct['unclutter']['settings']['unclutter_enable']['value'] == '1':
                state = 1
                options['UNCLUTTER_TIME']  = '"%s"' % self.struct['unclutter']['settings']['unclutter_time']['value']
            self.oe.set_service('unclutter', options, state)   
            self.oe.set_busy(0)
            self.oe.dbg_log('services::initialize_unclutter', 'exit_function', 0)
        except Exception, e:
            self.oe.set_busy(0)
            self.oe.dbg_log('services::initialize_unclutter', 'ERROR: (' + repr(e) + ')', 4)
