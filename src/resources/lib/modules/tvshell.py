################################################################################
#      This file is part of Alex@ELEC - http://www.alexelec.in.ua
#      Copyright (C) 2011-2016 Alexandr Zuyev (alex@alexelec.in.ua)
################################################################################
# -*- coding: utf-8 -*-

import os
import re
import glob
import time
import xbmc
import xbmcgui
import oeWindows
import threading
import subprocess

class tvshell:

    ENABLED = False
    D_VDR_SHELL = None
    D_VDR_DEBUG = None
    D_VDR_VIDEO_DIR = None

    D_VDR_DVBAPI = None
    D_VDR_IPTV = None
    D_VDR_IPTV_DEVICES = None
    D_VDR_SATIP = None
    D_VDR_EPGSEARCH = None
    D_VDR_STREAMDEV_SERVER = None
    D_VDR_STREAMDEV_CLIENT = None
    D_VDR_CHSCAN = None
    D_VDR_FEMON = None
    D_VDR_SYSINFO = None
    D_VDR_SLEEP = None
    D_VDR_PVR = None
    D_VDR_TVSCRAPER = None
    D_VDR_SKIN_NOPACITY = None
    D_VDR_WEATHER = None
    D_VDR_SKIN_DESIGNER = None
    D_VDR_TVGUIDENG = None
    D_VDR_ZAPHISTORY = None
    D_VDR_LIVE = None
    D_VDR_LCDPROC = None

    URL_LOGOS_FILE = None
    RUN_LOGOS = None
    GET_LOGO_COUNT = None
    GET_MISS_COUNT = None
    LOGO_GET_LOG = None
    KILL_LOGO_SH = None
    D_LOGOS_DIR = None
    D_LOGOS_CLEAR = None
    D_LOGOS_BG_COLOR = None
    D_LOGOS_FG_COLOR = None
    D_LOGOS_TEXT_COLOR = None

    menu = {'91': {
        'name': 38000,
        'menuLoader': 'load_menu',
        'listTyp': 'list',
        'InfoText': 3800,
        }}

    def __init__(self, oeMain):
        try:
            oeMain.dbg_log('tvshell::__init__', 'enter_function', 0)
            self.struct = {
                'vdr': {
                    'order': 1,
                    'name': 38010,
                    'not_supported': [],
                    'settings': {
                        'enable_vdr': {
                            'order': 1,
                            'name': 38011,
                            'value': '0',
                            'action': 'initialize_vdr',
                            'type': 'bool',
                            'InfoText': 3811,
                        },
                        'vdr_shell': {
                            'order': 2,
                            'name': 38012,
                            'value': '0',
                            'action': 'initialize_vdr',
                            'type': 'bool',
                            'parent': {'entry': 'enable_vdr','value': ['1']},
                            'InfoText': 3812,
                        },
                        'vdr_debug': {
                            'order': 3,
                            'name': 38013,
                            'value': '0',
                            'action': 'initialize_vdr',
                            'type': 'bool',
                            'parent': {'entry': 'enable_vdr','value': ['1']},
                            'InfoText': 3813,
                        },
                        'vdr_video_dir': {
                            'order': 4,
                            'name': 38014,
                            'value': None,
                            'action': 'initialize_vdr',
                            'type': 'folder',
                            'parent': {'entry': 'enable_vdr','value': ['1']},
                            'InfoText': 3814,
                        },
                        'vdr_dvbapi': {
                            'order': 5,
                            'name': 38015,
                            'value': '1',
                            'action': 'initialize_vdr',
                            'type': 'bool',
                            'parent': {'entry': 'enable_vdr','value': ['1']},
                            'InfoText': 3815,
                        },
                        'vdr_iptv': {
                            'order': 6,
                            'name': 38016,
                            'value': '0',
                            'action': 'initialize_vdr',
                            'type': 'bool',
                            'parent': {'entry': 'enable_vdr','value': ['1']},
                            'InfoText': 3816,
                        },
                        'vdr_iptv_devices': {
                            'order': 7,
                            'name': 38017,
                            'value': '1',
                            'values': ['1', '2', '3', '4'],
                            'action': 'initialize_vdr',
                            'type': 'multivalue',
                            'InfoText': 3817,
                        },
                        'vdr_satip': {
                            'order': 8,
                            'name': 38018,
                            'value': '0',
                            'action': 'initialize_vdr',
                            'type': 'bool',
                            'parent': {'entry': 'enable_vdr','value': ['1']},
                            'InfoText': 3818,
                        },
                        'vdr_epgsearch': {
                            'order': 9,
                            'name': 38019,
                            'value': '1',
                            'action': 'initialize_vdr',
                            'type': 'bool',
                            'parent': {'entry': 'enable_vdr','value': ['1']},
                            'InfoText': 3819,
                        },
                        'vdr_streamdev_server': {
                            'order': 10,
                            'name': 38020,
                            'value': '0',
                            'action': 'initialize_vdr',
                            'type': 'bool',
                            'parent': {'entry': 'enable_vdr','value': ['1']},
                            'InfoText': 3820,
                        },
                        'vdr_streamdev_client': {
                            'order': 11,
                            'name': 38021,
                            'value': '0',
                            'action': 'initialize_vdr',
                            'type': 'bool',
                            'parent': {'entry': 'enable_vdr','value': ['1']},
                            'InfoText': 3821,
                        },
                        'vdr_chscan': {
                            'order': 12,
                            'name': 38022,
                            'value': '0',
                            'action': 'initialize_vdr',
                            'type': 'bool',
                            'parent': {'entry': 'enable_vdr','value': ['1']},
                            'InfoText': 3822,
                        },
                        'vdr_femon': {
                            'order': 13,
                            'name': 38023,
                            'value': '1',
                            'action': 'initialize_vdr',
                            'type': 'bool',
                            'parent': {'entry': 'enable_vdr','value': ['1']},
                            'InfoText': 3823,
                        },
                        'vdr_sysinfo': {
                            'order': 14,
                            'name': 38024,
                            'value': '1',
                            'action': 'initialize_vdr',
                            'type': 'bool',
                            'parent': {'entry': 'enable_vdr','value': ['1']},
                            'InfoText': 3824,
                        },
                        'vdr_sleep': {
                            'order': 15,
                            'name': 38025,
                            'value': '0',
                            'action': 'initialize_vdr',
                            'type': 'bool',
                            'parent': {'entry': 'enable_vdr','value': ['1']},
                            'InfoText': 3825,
                        },
                        'vdr_pvr': {
                            'order': 16,
                            'name': 38026,
                            'value': 'none',
                            'values': ['none', 'xvdr', 'vnsiserver'],
                            'action': 'initialize_vdr',
                            'type': 'multivalue',
                            'parent': {'entry': 'enable_vdr','value': ['1']},
                            'InfoText': 3826,
                        },
                        'vdr_tvscraper': {
                            'order': 17,
                            'name': 38027,
                            'value': '0',
                            'action': 'initialize_vdr',
                            'type': 'bool',
                            'parent': {'entry': 'enable_vdr','value': ['1']},
                            'InfoText': 3827,
                        },
                        'vdr_skin_nopacity': {
                            'order': 18,
                            'name': 38028,
                            'value': '0',
                            'action': 'initialize_vdr',
                            'type': 'bool',
                            'parent': {'entry': 'enable_vdr','value': ['1']},
                            'InfoText': 3828,
                        },
                        'vdr_weather': {
                            'order': 19,
                            'name': 38029,
                            'value': '0',
                            'action': 'initialize_vdr',
                            'type': 'bool',
                            'parent': {'entry': 'enable_vdr','value': ['1']},
                            'InfoText': 3829,
                        },
                        'vdr_skin_designer': {
                            'order': 20,
                            'name': 38030,
                            'value': '0',
                            'action': 'initialize_vdr',
                            'type': 'bool',
                            'parent': {'entry': 'enable_vdr','value': ['1']},
                            'InfoText': 3830,
                        },
                        'vdr_tvguideng': {
                            'order': 21,
                            'name': 38031,
                            'value': '0',
                            'action': 'initialize_vdr',
                            'type': 'bool',
                            'parent': {'entry': 'enable_vdr','value': ['1']},
                            'InfoText': 3831,
                        },
                        'vdr_zaphistory': {
                            'order': 22,
                            'name': 38032,
                            'value': '0',
                            'action': 'initialize_vdr',
                            'type': 'bool',
                            'parent': {'entry': 'enable_vdr','value': ['1']},
                            'InfoText': 3832,
                        },
                        'vdr_live': {
                            'order': 23,
                            'name': 38033,
                            'value': '0',
                            'action': 'initialize_vdr',
                            'type': 'bool',
                            'parent': {'entry': 'enable_vdr','value': ['1']},
                            'InfoText': 3833,
                        },
                        'vdr_lcdproc': {
                            'order': 24,
                            'name': 38034,
                            'value': '0',
                            'action': 'initialize_vdr',
                            'type': 'bool',
                            'parent': {'entry': 'enable_vdr','value': ['1']},
                            'InfoText': 3834,
                        },
                    },
                },
                'logos': {
                    'order': 2,
                    'name': 38050,
                    'not_supported': [],
                    'settings': {
                        'logos_dir': {
                            'order': 1,
                            'name': 38051,
                            'value': None,
                            'action': 'initialize_logos',
                            'type': 'folder',
                            'InfoText': 3851,
                        },
                        'logos_clear': {
                            'order': 2,
                            'name': 38052,
                            'value': '0',
                            'action': 'initialize_logos',
                            'type': 'bool',
                            'InfoText': 3852,
                        },
                        'logos_bg_color': {
                            'order': 3,
                            'name': 38053,
                            'value': 'White',
                            'values': ['Black', 'Blue', 'Green', 'GreyBlue', 'Purple', 'Red', 'Vinous', 'White'],
                            'action': 'initialize_logos',
                            'type': 'multivalue',
                            'InfoText': 3853,
                        },
                        'logos_fg_color': {
                            'order': 4,
                            'name': 38054,
                            'value': '4',
                            'values': ['1', '2', '3', '4', '5'],
                            'action': 'initialize_logos',
                            'type': 'multivalue',
                            'InfoText': 3854,
                        },
                        'logos_text_color': {
                            'order': 5,
                            'name': 38055,
                            'value': 'black',
                            'values': ['white', 'black', 'red', 'blue', 'green', 'yellow'],
                            'action': 'initialize_logos',
                            'type': 'multivalue',
                            'InfoText': 3855,
                        },
                        'logos_create': {
                            'order': 6,
                            'name': 38056,
                            'value': '0',
                            'action': 'execute_logos',
                            'type': 'button',
                            'InfoText': 3856,
                        },
                    },
                },
            }

            self.oe = oeMain
            oeMain.dbg_log('tvshell::__init__', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('tvshell::__init__', 'ERROR: (%s)' % repr(e))

    def start_service(self):
        try:
            self.oe.dbg_log('tvshell::start_service', 'enter_function', 0)
            self.load_values()
            self.initialize_vdr
            self.initialize_logos()
            self.oe.dbg_log('tvshell::start_service', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('tvshell::start_service', 'ERROR: (%s)' % repr(e))

    def stop_service(self):
        try:
            self.oe.dbg_log('tvshell::stop_service', 'enter_function', 0)
            self.oe.dbg_log('tvshell::stop_service', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('tvshell::stop_service', 'ERROR: (' + repr(e) + ')')

    def do_init(self):
        try:
            self.oe.dbg_log('tvshell::do_init', 'exit_function', 0)
            self.load_values()
            self.oe.dbg_log('tvshell::do_init', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('tvshell::do_init', 'ERROR: (%s)' % repr(e))

    def set_value(self, listItem):
        try:
            self.oe.dbg_log('tvshell::set_value', 'enter_function', 0)
            self.struct[listItem.getProperty('category')]['settings'
                    ][listItem.getProperty('entry')]['value'] = \
                listItem.getProperty('value')
            self.oe.dbg_log('tvshell::set_value', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('tvshell::set_value', 'ERROR: (' + repr(e) + ')')
            
    def load_menu(self, focusItem):
        try:
            self.oe.dbg_log('tvshell::load_menu', 'enter_function', 0)
            self.oe.winOeMain.build_menu(self.struct)
            self.oe.dbg_log('tvshell::load_menu', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('tvshell::load_menu', 'ERROR: (%s)' % repr(e))

    def load_values(self):
        try:
            self.oe.dbg_log('tvshell::load_values', 'enter_function', 0)

            # VDR Frontend
            vdrenabled = self.oe.get_service_state('vdr')
            self.struct['vdr']['settings']['vdr_iptv_devices']['hidden'] = 'true'
            if vdrenabled == '1':
                if self.struct['vdr']['settings']['vdr_iptv']['value'] == '1':
                    if 'hidden' in self.struct['vdr']['settings']['vdr_iptv_devices']:
                        del self.struct['vdr']['settings']['vdr_iptv_devices']['hidden']

            self.struct['vdr']['settings']['enable_vdr']['value'] = vdrenabled

            self.struct['vdr']['settings']['vdr_shell']['value'] = \
                self.oe.get_service_option('vdr', 'VDR_SHELL', self.D_VDR_SHELL).replace('"', '')

            self.struct['vdr']['settings']['vdr_debug']['value'] = \
                self.oe.get_service_option('vdr', 'VDR_DEBUG', self.D_VDR_DEBUG).replace('"', '')

            self.struct['vdr']['settings']['vdr_video_dir']['value'] = \
                self.oe.get_service_option('vdr', 'VDR_VIDEO_DIR', self.D_VDR_VIDEO_DIR).replace('"', '')

            self.struct['vdr']['settings']['vdr_dvbapi']['value'] = \
                self.oe.get_service_option('vdr', 'VDR_DVBAPI', self.D_VDR_DVBAPI).replace('"', '')

            self.struct['vdr']['settings']['vdr_iptv']['value'] = \
                self.oe.get_service_option('vdr', 'VDR_IPTV', self.D_VDR_IPTV).replace('"', '')

            self.struct['vdr']['settings']['vdr_iptv_devices']['value'] = \
                self.oe.get_service_option('vdr', 'VDR_IPTV_DEVICES', self.D_VDR_IPTV_DEVICES).replace('"', '')

            self.struct['vdr']['settings']['vdr_satip']['value'] = \
                self.oe.get_service_option('vdr', 'VDR_SATIP', self.D_VDR_SATIP).replace('"', '')

            self.struct['vdr']['settings']['vdr_epgsearch']['value'] = \
                self.oe.get_service_option('vdr', 'VDR_EPGSEARCH', self.D_VDR_EPGSEARCH).replace('"', '')

            self.struct['vdr']['settings']['vdr_streamdev_server']['value'] = \
                self.oe.get_service_option('vdr', 'VDR_STREAMDEV_SERVER', self.D_VDR_STREAMDEV_SERVER).replace('"', '')

            self.struct['vdr']['settings']['vdr_streamdev_client']['value'] = \
                self.oe.get_service_option('vdr', 'VDR_STREAMDEV_CLIENT', self.D_VDR_STREAMDEV_CLIENT).replace('"', '')

            self.struct['vdr']['settings']['vdr_chscan']['value'] = \
                self.oe.get_service_option('vdr', 'VDR_CHSCAN', self.D_VDR_CHSCAN).replace('"', '')

            self.struct['vdr']['settings']['vdr_femon']['value'] = \
                self.oe.get_service_option('vdr', 'VDR_FEMON', self.D_VDR_FEMON).replace('"', '')

            self.struct['vdr']['settings']['vdr_sysinfo']['value'] = \
                self.oe.get_service_option('vdr', 'VDR_SYSINFO', self.D_VDR_SYSINFO).replace('"', '')

            self.struct['vdr']['settings']['vdr_sleep']['value'] = \
                self.oe.get_service_option('vdr', 'VDR_SLEEP', self.D_VDR_SLEEP).replace('"', '')

            self.struct['vdr']['settings']['vdr_pvr']['value'] = \
                self.oe.get_service_option('vdr', 'VDR_PVR', self.D_VDR_PVR).replace('"', '')

            self.struct['vdr']['settings']['vdr_tvscraper']['value'] = \
                self.oe.get_service_option('vdr', 'VDR_TVSCRAPER', self.D_VDR_TVSCRAPER).replace('"', '')

            self.struct['vdr']['settings']['vdr_skin_nopacity']['value'] = \
                self.oe.get_service_option('vdr', 'VDR_SKIN_NOPACITY', self.D_VDR_SKIN_NOPACITY).replace('"', '')

            self.struct['vdr']['settings']['vdr_weather']['value'] = \
                self.oe.get_service_option('vdr', 'VDR_WEATHER', self.D_VDR_WEATHER).replace('"', '')

            self.struct['vdr']['settings']['vdr_skin_designer']['value'] = \
                self.oe.get_service_option('vdr', 'VDR_SKIN_DESIGNER', self.D_VDR_SKIN_DESIGNER).replace('"', '')

            self.struct['vdr']['settings']['vdr_tvguideng']['value'] = \
                self.oe.get_service_option('vdr', 'VDR_TVGUIDENG', self.D_VDR_TVGUIDENG).replace('"', '')

            self.struct['vdr']['settings']['vdr_zaphistory']['value'] = \
                self.oe.get_service_option('vdr', 'VDR_ZAPHISTORY', self.D_VDR_ZAPHISTORY).replace('"', '')

            self.struct['vdr']['settings']['vdr_live']['value'] = \
                self.oe.get_service_option('vdr', 'VDR_LIVE', self.D_VDR_LIVE).replace('"', '')

            self.struct['vdr']['settings']['vdr_lcdproc']['value'] = \
                self.oe.get_service_option('vdr', 'VDR_LCDPROC', self.D_VDR_LCDPROC).replace('"', '')

            # Logos
            self.struct['logos']['settings']['logos_dir']['value'] = \
                self.oe.get_service_option('logos', 'LOGOS_DIR', self.D_LOGOS_DIR).replace('"', '')

            self.struct['logos']['settings']['logos_clear']['value'] = \
                self.oe.get_service_option('logos', 'LOGOS_CLEAR', self.D_LOGOS_CLEAR).replace('"', '')

            self.struct['logos']['settings']['logos_bg_color']['value'] = \
                self.oe.get_service_option('logos', 'LOGOS_BG_COLOR', self.D_LOGOS_BG_COLOR).replace('"', '')

            self.struct['logos']['settings']['logos_fg_color']['value'] = \
                self.oe.get_service_option('logos', 'LOGOS_FG_COLOR', self.D_LOGOS_FG_COLOR).replace('"', '')

            self.struct['logos']['settings']['logos_text_color']['value'] = \
                self.oe.get_service_option('logos', 'LOGOS_TEXT_COLOR', self.D_LOGOS_TEXT_COLOR).replace('"', '')

            self.oe.dbg_log('tvshell::load_values', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('tvshell::load_values', 'ERROR: (%s)' % repr(e))

    def initialize_vdr(self, **kwargs):
        try:
            self.oe.dbg_log('tvshell::initialize_vdr', 'enter_function', 0)
            self.oe.set_busy(1)
            if 'listItem' in kwargs:
                self.set_value(kwargs['listItem'])
            options = {}
            state = 0
            self.struct['vdr']['settings']['vdr_iptv_devices']['hidden'] = 'true'
            if self.struct['vdr']['settings']['enable_vdr']['value'] == '1':
                if self.struct['vdr']['settings']['vdr_iptv']['value'] == '1':
                    if 'hidden' in self.struct['vdr']['settings']['vdr_iptv_devices']:
                        del self.struct['vdr']['settings']['vdr_iptv_devices']['hidden']
                state = 1
                options['VDR_SHELL'] = '"%s"' % self.struct['vdr']['settings']['vdr_shell']['value']
                options['VDR_DEBUG'] = '"%s"' % self.struct['vdr']['settings']['vdr_debug']['value']
                options['VDR_VIDEO_DIR'] = '"%s"' % self.struct['vdr']['settings']['vdr_video_dir']['value']
                options['VDR_DVBAPI'] = '"%s"' % self.struct['vdr']['settings']['vdr_dvbapi']['value']
                options['VDR_IPTV'] = '"%s"' % self.struct['vdr']['settings']['vdr_iptv']['value']
                options['VDR_IPTV_DEVICES'] = '"%s"' % self.struct['vdr']['settings']['vdr_iptv_devices']['value']
                options['VDR_SATIP'] = '"%s"' % self.struct['vdr']['settings']['vdr_satip']['value']
                options['VDR_EPGSEARCH'] = '"%s"' % self.struct['vdr']['settings']['vdr_epgsearch']['value']
                options['VDR_STREAMDEV_SERVER'] = '"%s"' % self.struct['vdr']['settings']['vdr_streamdev_server']['value']
                options['VDR_STREAMDEV_CLIENT'] = '"%s"' % self.struct['vdr']['settings']['vdr_streamdev_client']['value']
                options['VDR_CHSCAN'] = '"%s"' % self.struct['vdr']['settings']['vdr_chscan']['value']
                options['VDR_FEMON'] = '"%s"' % self.struct['vdr']['settings']['vdr_femon']['value']
                options['VDR_SYSINFO'] = '"%s"' % self.struct['vdr']['settings']['vdr_sysinfo']['value']
                options['VDR_SLEEP'] = '"%s"' % self.struct['vdr']['settings']['vdr_sleep']['value']
                options['VDR_PVR'] = '"%s"' % self.struct['vdr']['settings']['vdr_pvr']['value']
                options['VDR_TVSCRAPER'] = '"%s"' % self.struct['vdr']['settings']['vdr_tvscraper']['value']
                options['VDR_SKIN_NOPACITY'] = '"%s"' % self.struct['vdr']['settings']['vdr_skin_nopacity']['value']
                options['VDR_WEATHER'] = '"%s"' % self.struct['vdr']['settings']['vdr_weather']['value']
                options['VDR_SKIN_DESIGNER'] = '"%s"' % self.struct['vdr']['settings']['vdr_skin_designer']['value']
                options['VDR_TVGUIDENG'] = '"%s"' % self.struct['vdr']['settings']['vdr_tvguideng']['value']
                options['VDR_ZAPHISTORY'] = '"%s"' % self.struct['vdr']['settings']['vdr_zaphistory']['value']
                options['VDR_LIVE'] = '"%s"' % self.struct['vdr']['settings']['vdr_live']['value']
                options['VDR_LCDPROC'] = '"%s"' % self.struct['vdr']['settings']['vdr_lcdproc']['value']
            self.oe.set_service('vdr', options, state)
            self.oe.set_busy(0)
            self.oe.dbg_log('vdr::initialize_vdr', 'exit_function', 0)
        except Exception, e:
            self.oe.set_busy(0)
            self.oe.dbg_log('vdr::initialize_vdr', 'ERROR: (%s)' % repr(e), 4)

    def initialize_logos(self, **kwargs):
        try:
            self.oe.dbg_log('tvshell::initialize_logos', 'enter_function', 0)
            self.oe.set_busy(1)
            if 'listItem' in kwargs:
                self.set_value(kwargs['listItem'])
            options = {}
            state = 1
            options['LOGOS_DIR'] = '"%s"' % self.struct['logos']['settings']['logos_dir']['value']
            options['LOGOS_CLEAR'] = '"%s"' % self.struct['logos']['settings']['logos_clear']['value']
            options['LOGOS_BG_COLOR'] = '"%s"' % self.struct['logos']['settings']['logos_bg_color']['value']
            options['LOGOS_FG_COLOR'] = '"%s"' % self.struct['logos']['settings']['logos_fg_color']['value']
            options['LOGOS_TEXT_COLOR'] = '"%s"' % self.struct['logos']['settings']['logos_text_color']['value']
            self.oe.set_service('logos', options, state)
            self.oe.set_busy(0)
            self.oe.dbg_log('tvshell::initialize_logos', 'exit_function', 0)
        except Exception, e:
            self.oe.set_busy(0)
            self.oe.dbg_log('tvshell::initialize_logos', 'ERROR: (%s)' % repr(e), 4)

    def execute_logos(self, listItem=None, silent=False):
        try:
            self.oe.dbg_log('tvshell::execute_logos', 'enter_function', 0)
            self.download_file = self.URL_LOGOS_FILE
            if hasattr(self, 'download_file'):
                downloaded = self.oe.download_file(self.download_file, self.oe.TEMP + self.download_file.split('/')[-1], silent)
                if not downloaded is None:
                    self.oe.notify(self.oe._(32363), 'Unpack logos...')
                    self.oe.set_busy(1)
                    self.oe.execute(self.RUN_LOGOS + ' unpack', 0)
                    self.oe.set_busy(0)

                    self.oe.execute(self.RUN_LOGOS + ' list', 0)
                    logo_count = self.oe.execute(self.GET_LOGO_COUNT, 1).strip()
                    logo_count = int(logo_count)

                    self.oe.notify(self.oe._(32363), 'Conversion logos...')
                    subprocess.Popen(self.RUN_LOGOS + ' convert',
                                        shell=True, 
                                        close_fds=True,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.STDOUT)

                    xbmcDialog = xbmcgui.DialogProgress()
                    xbmcDialog.create('Conversion logos', "",
                                'Number logos in list:  %d' % logo_count)

                    message = self.oe.execute(self.LOGO_GET_LOG, 1).strip()
                    message_tmp = message
                    i = 0
                    max_count = logo_count + 1
                    while not 'Conversion logos completed.' in message:
                        percent = int((i / float(logo_count)) * 100)
                        message = self.oe.execute(self.LOGO_GET_LOG, 1).strip()
                        if message_tmp != message:
                            message_tmp = message
                            if i < max_count:
                                i = i + 1
                        xbmcDialog.update(percent, "", "", message)
                        xbmc.sleep(500)
                        if xbmcDialog.iscanceled():
                            self.oe.execute(self.KILL_LOGO_SH, 0)
                            break

                    xbmc.sleep(1000)
                    xbmcDialog.close()

                    self.oe.notify(self.oe._(32363), 'Create missing logos...')
                    self.oe.set_busy(1)
                    self.oe.execute(self.RUN_LOGOS + ' misslist', 0)
                    logo_count = self.oe.execute(self.GET_MISS_COUNT, 1).strip()
                    logo_count = int(logo_count)
                    self.oe.set_busy(0)

                    subprocess.Popen(self.RUN_LOGOS + ' missing',
                                        shell=True, 
                                        close_fds=True,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.STDOUT)

                    xbmcDialog = xbmcgui.DialogProgress()
                    xbmcDialog.create('Create missing logos', "",
                                'Number logos in list:  %d' % logo_count)

                    message = self.oe.execute(self.LOGO_GET_LOG, 1).strip()
                    message_tmp = message
                    i = 0
                    max_count = logo_count + 1
                    while not 'Create logos completed.' in message:
                        percent = int((i / float(logo_count)) * 100)
                        message = self.oe.execute(self.LOGO_GET_LOG, 1).strip()
                        if message_tmp != message:
                            message_tmp = message
                            if i < max_count:
                                i = i + 1
                        xbmcDialog.update(percent, "", "", message)
                        xbmc.sleep(500)
                        if xbmcDialog.iscanceled():
                            self.oe.execute(self.KILL_LOGO_SH, 0)
                            break

                    xbmc.sleep(3000)
                    xbmcDialog.close()

            self.oe.dbg_log('tvshell::execute_logos', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('tvshell::execute_logos', 'ERROR: (' + repr(e) + ')')

    def exit(self):
        try:
            self.oe.dbg_log('tvshell::exit', 'enter_function', 0)
            self.oe.dbg_log('tvshell::exit', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('tvshell::exit', 'ERROR: (%s)' % repr(e), 4)
