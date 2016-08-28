################################################################################
#      This file is part of Alex@ELEC - http://www.alexelec.in.ua
#      Copyright (C) 2011-2016 Alexandr Zuyev (alex@alexelec.in.ua)
################################################################################
# -*- coding: utf-8 -*-

import os
import glob

class tvbackend:

    ENABLED = False
    D_BVDR_DEBUG = None
    D_BVDR_VIDEO_DIR = None
    D_BVDR_DVBAPI = None
    D_BVDR_PVR = None
    D_BVDR_IPTV = None
    D_BVDR_IPTV_DEVICES = None
    D_BVDR_SATIP = None
    D_BVDR_STREAMDEV_SERVER = None
    D_BVDR_STREAMDEV_CLIENT = None
    D_BVDR_CHSCAN = None
    D_BVDR_LIVE = None
    D_TVH_DEBUG = None
    D_TVH_BACKUP = None
    D_TVH_BINDADDR = None
    D_TVH_TIMEOUT = None
    FILE_TVH_BINDADDR = None
    GET_TVH_BINDADDR = None
    
    menu = {'9': {
        'name': 37000,
        'menuLoader': 'load_menu',
        'listTyp': 'list',
        'InfoText': 3700,
        }}

    def __init__(self, oeMain):
        try:
            oeMain.dbg_log('tvbackend::__init__', 'enter_function', 0)
            self.struct = {
                'vdr-backend': {
                    'order': 1,
                    'name': 37010,
                    'not_supported': [],
                    'settings': {
                        'enable_bvdr': {
                            'order': 1,
                            'name': 37011,
                            'value': '0',
                            'action': 'initialize_bvdr',
                            'type': 'bool',
                            'InfoText': 3711,
                        },
                        'bvdr_debug': {
                            'order': 2,
                            'name': 37012,
                            'value': '0',
                            'action': 'initialize_bvdr',
                            'type': 'bool',
                            'parent': {'entry': 'enable_bvdr','value': ['1']},
                            'InfoText': 3712,
                        },
                        'bvdr_video_dir': {
                            'order': 3,
                            'name': 37013,
                            'value': '/storage/recordings/',
                            'action': 'initialize_bvdr',
                            'type': 'folder',
                            'parent': {'entry': 'enable_bvdr','value': ['1']},
                            'InfoText': 3713,
                        },
                        'bvdr_dvbapi': {
                            'order': 4,
                            'name': 37014,
                            'value': '1',
                            'action': 'initialize_bvdr',
                            'type': 'bool',
                            'parent': {'entry': 'enable_bvdr','value': ['1']},
                            'InfoText': 3714,
                        },
                        'bvdr_pvr': {
                            'order': 5,
                            'name': 37015,
                            'value': 'xvdr',
                            'values': ['none', 'xvdr', 'vnsiserver'],
                            'action': 'initialize_bvdr',
                            'type': 'multivalue',
                            'parent': {'entry': 'enable_bvdr','value': ['1']},
                            'InfoText': 3715,
                        },
                        'bvdr_iptv': {
                            'order': 6,
                            'name': 37016,
                            'value': '0',
                            'action': 'initialize_bvdr',
                            'type': 'bool',
                            'parent': {'entry': 'enable_bvdr','value': ['1']},
                            'InfoText': 3716,
                        },
                        'bvdr_iptv_devices': {
                            'order': 7,
                            'name': 37017,
                            'value': '1',
                            'values': ['1', '2', '3', '4'],
                            'action': 'initialize_bvdr',
                            'type': 'multivalue',
                            'InfoText': 3717,
                        },
                        'bvdr_satip': {
                            'order': 8,
                            'name': 37018,
                            'value': '0',
                            'action': 'initialize_bvdr',
                            'type': 'bool',
                            'parent': {'entry': 'enable_bvdr','value': ['1']},
                            'InfoText': 3718,
                        },
                        'bvdr_stream_server': {
                            'order': 9,
                            'name': 37019,
                            'value': '1',
                            'action': 'initialize_bvdr',
                            'type': 'bool',
                            'parent': {'entry': 'enable_bvdr','value': ['1']},
                            'InfoText': 3719,
                        },
                        'bvdr_stream_client': {
                            'order': 10,
                            'name': 37020,
                            'value': '0',
                            'action': 'initialize_bvdr',
                            'type': 'bool',
                            'parent': {'entry': 'enable_bvdr','value': ['1']},
                            'InfoText': 3720,
                        },
                        'bvdr_chscan': {
                            'order': 11,
                            'name': 37021,
                            'value': '0',
                            'action': 'initialize_bvdr',
                            'type': 'bool',
                            'parent': {'entry': 'enable_bvdr','value': ['1']},
                            'InfoText': 3721,
                        },
                        'bvdr_live': {
                            'order': 12,
                            'name': 37022,
                            'value': '0',
                            'action': 'initialize_bvdr',
                            'type': 'bool',
                            'parent': {'entry': 'enable_bvdr','value': ['1']},
                            'InfoText': 3722,
                        },
                    },
                },
                'tvheadend': {
                    'order': 2,
                    'name': 37030,
                    'not_supported': [],
                    'settings': {
                        'enable_tvheadend': {
                            'order': 1,
                            'name': 37031,
                            'value': '0',
                            'action': 'initialize_tvheadend',
                            'type': 'bool',
                            'InfoText': 3731,
                        },
                        'tvh_debug': {
                            'order': 2,
                            'name': 37032,
                            'value': '0',
                            'action': 'initialize_tvheadend',
                            'type': 'bool',
                            'parent': {'entry': 'enable_tvheadend','value': ['1']},
                            'InfoText': 3732,
                        },
                        'tvh_backup': {
                            'order': 3,
                            'name': 37033,
                            'value': '0',
                            'action': 'initialize_tvheadend',
                            'type': 'bool',
                            'parent': {'entry': 'enable_tvheadend','value': ['1']},
                            'InfoText': 3733,
                        },
                        'tvh_bindaddr': {
                            'order': 4,
                            'name': 37034,
                            'value': 'All',
                            'values': [],
                            'action': 'initialize_tvheadend',
                            'type': 'multivalue',
                            'parent': {'entry': 'enable_tvheadend','value': ['1']},
                            'InfoText': 3734,
                        },
                        'tvh_timeout': {
                            'order': 5,
                            'name': 37035,
                            'value': '5',
                            'values': ['5', '8', '10', '20', '30'],
                            'action': 'initialize_tvheadend',
                            'type': 'multivalue',
                            'parent': {'entry': 'enable_tvheadend','value': ['1']},
                            'InfoText': 3735,
                        },
                    },
                },
            }

            self.oe = oeMain
            oeMain.dbg_log('tvbackend::__init__', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('tvbackend::__init__', 'ERROR: (%s)' % repr(e))

    def start_service(self):
        try:
            self.oe.dbg_log('tvbackend::start_service', 'enter_function', 0)
            self.load_values()
            self.initialize_bvdr(service=1)
            self.initialize_tvheadend(service=1)
            self.oe.dbg_log('tvbackend::start_service', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('tvbackend::start_service', 'ERROR: (%s)' % repr(e))

    def stop_service(self):
        try:
            self.oe.dbg_log('tvbackend::stop_service', 'enter_function', 0)
            self.oe.dbg_log('tvbackend::stop_service', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('tvbackend::stop_service', 'ERROR: (' + repr(e) + ')')

    def do_init(self):
        try:
            self.oe.dbg_log('tvbackend::do_init', 'exit_function', 0)
            self.load_values()
            self.oe.dbg_log('tvbackend::do_init', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('tvbackend::do_init', 'ERROR: (%s)' % repr(e))

    def set_value(self, listItem):
        try:
            self.oe.dbg_log('tvbackend::set_value', 'enter_function', 0)
            self.struct[listItem.getProperty('category')]['settings'][listItem.getProperty('entry')]['value'] = listItem.getProperty('value')
            self.oe.dbg_log('tvbackend::set_value', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('tvbackend::set_value', 'ERROR: (' + repr(e) + ')')

    def load_menu(self, focusItem):
        try:
            self.oe.dbg_log('tvbackend::load_menu', 'enter_function', 0)
            self.oe.winOeMain.build_menu(self.struct)
            self.oe.dbg_log('tvbackend::load_menu', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('tvbackend::load_menu', 'ERROR: (%s)' % repr(e))

    def load_values(self):
        try:
            self.oe.dbg_log('tvbackend::load_values', 'enter_function', 0)

            bvdrenabled = self.oe.get_service_state('vdr-backend')
            tvhenabled = self.oe.get_service_state('tvheadend')

            self.struct['vdr-backend']['settings']['bvdr_iptv_devices']['hidden'] = 'true'
            if bvdrenabled == '1':
                if self.struct['vdr-backend']['settings']['bvdr_iptv']['value'] == '1':
                    if 'hidden' in self.struct['vdr-backend']['settings']['bvdr_iptv_devices']:
                        del self.struct['vdr-backend']['settings']['bvdr_iptv_devices']['hidden']

            # VDR-BACKEND
            self.struct['vdr-backend']['settings']['enable_bvdr']['value'] = bvdrenabled

            self.struct['vdr-backend']['settings']['bvdr_debug']['value'] = \
            self.oe.get_service_option('vdr-backend', 'BVDR_DEBUG', self.D_BVDR_DEBUG).replace('"', '')

            self.struct['vdr-backend']['settings']['bvdr_video_dir']['value'] = \
            self.oe.get_service_option('vdr-backend', 'BVDR_VIDEO_DIR', self.D_BVDR_VIDEO_DIR).replace('"', '')

            self.struct['vdr-backend']['settings']['bvdr_dvbapi']['value'] = \
            self.oe.get_service_option('vdr-backend', 'BVDR_DVBAPI', self.D_BVDR_DVBAPI).replace('"', '')

            self.struct['vdr-backend']['settings']['bvdr_pvr']['value'] = \
            self.oe.get_service_option('vdr-backend', 'BVDR_PVR', self.D_BVDR_PVR).replace('"', '')

            self.struct['vdr-backend']['settings']['bvdr_iptv']['value'] = \
            self.oe.get_service_option('vdr-backend', 'BVDR_IPTV', self.D_BVDR_IPTV).replace('"', '')

            self.struct['vdr-backend']['settings']['bvdr_iptv_devices']['value'] = \
            self.oe.get_service_option('vdr-backend', 'BVDR_IPTV_DEVICES', self.D_BVDR_IPTV_DEVICES).replace('"', '')

            self.struct['vdr-backend']['settings']['bvdr_satip']['value'] = \
            self.oe.get_service_option('vdr-backend', 'BVDR_SATIP', self.D_BVDR_SATIP).replace('"', '')

            self.struct['vdr-backend']['settings']['bvdr_stream_server']['value'] = \
            self.oe.get_service_option('vdr-backend', 'BVDR_STREAMDEV_SERVER', self.D_BVDR_STREAMDEV_SERVER).replace('"', '')

            self.struct['vdr-backend']['settings']['bvdr_stream_client']['value'] = \
            self.oe.get_service_option('vdr-backend', 'BVDR_STREAMDEV_CLIENT', self.D_BVDR_STREAMDEV_CLIENT).replace('"', '')

            self.struct['vdr-backend']['settings']['bvdr_chscan']['value'] = \
            self.oe.get_service_option('vdr-backend', 'BVDR_CHSCAN', self.D_BVDR_CHSCAN).replace('"', '')

            self.struct['vdr-backend']['settings']['bvdr_live']['value'] = \
            self.oe.get_service_option('vdr-backend', 'BVDR_LIVE', self.D_BVDR_LIVE).replace('"', '')

            # TVHEADEND
            arrBindaddr = self.get_bindaddr()
            self.struct['tvheadend']['settings']['tvh_bindaddr']['values'] = arrBindaddr

            self.struct['tvheadend']['settings']['enable_tvheadend']['value'] = tvhenabled

            self.struct['tvheadend']['settings']['tvh_debug']['value'] = \
            self.oe.get_service_option('tvheadend', 'TVH_DEBUG', self.D_TVH_DEBUG).replace('"', '')

            self.struct['tvheadend']['settings']['tvh_backup']['value'] = \
            self.oe.get_service_option('tvheadend', 'TVH_BACKUP', self.D_TVH_BACKUP).replace('"', '')

            self.struct['tvheadend']['settings']['tvh_bindaddr']['value'] = \
            self.oe.get_service_option('tvheadend', 'TVH_BINDADDR', self.D_TVH_BINDADDR).replace('"', '')

            self.struct['tvheadend']['settings']['tvh_timeout']['value'] = \
            self.oe.get_service_option('tvheadend', 'TVH_TIMEOUT', self.D_TVH_TIMEOUT).replace('"', '')

            self.oe.dbg_log('tvbackend::load_values', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('tvbackend::load_values', 'ERROR: (%s)' % repr(e))

    def initialize_bvdr(self, **kwargs):
        try:
            self.oe.dbg_log('tvbackend::initialize_bvdr', 'enter_function', 0)
            self.oe.set_busy(1)
            if 'listItem' in kwargs:
                self.set_value(kwargs['listItem'])
            options = {}
            state = 0
            self.struct['vdr-backend']['settings']['bvdr_iptv_devices']['hidden'] = 'true'
            if self.struct['vdr-backend']['settings']['enable_bvdr']['value'] == '1':
                state = 1
                if self.struct['vdr-backend']['settings']['bvdr_iptv']['value'] == '1':
                    if 'hidden' in self.struct['vdr-backend']['settings']['bvdr_iptv_devices']:
                        del self.struct['vdr-backend']['settings']['bvdr_iptv_devices']['hidden']
                options['BVDR_DEBUG'] = '"%s"' % self.struct['vdr-backend']['settings']['bvdr_debug']['value']
                options['BVDR_VIDEO_DIR'] = '"%s"' % self.struct['vdr-backend']['settings']['bvdr_video_dir']['value']
                options['BVDR_DVBAPI'] = '"%s"' % self.struct['vdr-backend']['settings']['bvdr_dvbapi']['value']
                options['BVDR_PVR'] = '"%s"' % self.struct['vdr-backend']['settings']['bvdr_pvr']['value']
                options['BVDR_IPTV'] = '"%s"' % self.struct['vdr-backend']['settings']['bvdr_iptv']['value']
                options['BVDR_IPTV_DEVICES'] = '"%s"' % self.struct['vdr-backend']['settings']['bvdr_iptv_devices']['value']
                options['BVDR_SATIP'] = '"%s"' % self.struct['vdr-backend']['settings']['bvdr_satip']['value']
                options['BVDR_STREAMDEV_SERVER'] = '"%s"' % self.struct['vdr-backend']['settings']['bvdr_stream_server']['value']
                options['BVDR_STREAMDEV_CLIENT'] = '"%s"' % self.struct['vdr-backend']['settings']['bvdr_stream_client']['value']
                options['BVDR_CHSCAN'] = '"%s"' % self.struct['vdr-backend']['settings']['bvdr_chscan']['value']
                options['BVDR_LIVE'] = '"%s"' % self.struct['vdr-backend']['settings']['bvdr_live']['value']
            self.oe.set_service('vdr-backend', options, state)
            self.oe.set_busy(0)
            self.oe.dbg_log('tvbackend::initialize_bvdr', 'exit_function', 0)
        except Exception, e:
            self.oe.set_busy(0)
            self.oe.dbg_log('tvbackend::initialize_bvdr', 'ERROR: (%s)' % repr(e), 4)

    def initialize_tvheadend(self, **kwargs):
        try:
            self.oe.dbg_log('tvbackend::initialize_tvheadend', 'enter_function', 0)
            self.oe.set_busy(1)
            if 'listItem' in kwargs:
                self.set_value(kwargs['listItem'])
            options = {}
            state = 0
            if self.struct['tvheadend']['settings']['enable_tvheadend']['value'] == '1':
                state = 1
                options['TVH_DEBUG']    = '"%s"' % self.struct['tvheadend']['settings']['tvh_debug']['value']
                options['TVH_BACKUP']   = '"%s"' % self.struct['tvheadend']['settings']['tvh_backup']['value']
                options['TVH_BINDADDR'] = '"%s"' % self.struct['tvheadend']['settings']['tvh_bindaddr']['value']
                options['TVH_TIMEOUT']  = '"%s"' % self.struct['tvheadend']['settings']['tvh_timeout']['value']
            self.oe.set_service('tvheadend', options, state)
            self.oe.set_busy(0)
            self.oe.dbg_log('tvbackend::initialize_tvheadend', 'exit_function', 0)
        except Exception, e:
            self.oe.set_busy(0)
            self.oe.dbg_log('tvbackend::initialize_tvheadend', 'ERROR: (%s)' % repr(e), 4)

    def get_bindaddr(self):
        try:
            self.oe.dbg_log('tvbackend::get_bindaddr', 'enter_function', 0)
            arrIP = ['All']
            self.oe.execute(self.GET_TVH_BINDADDR, 0)
            for bindips in open(self.FILE_TVH_BINDADDR).readlines():
                arrIP.append(bindips.strip())
            arrIP.sort()
            self.oe.dbg_log('tvbackend::get_bindaddr', 'exit_function', 0)
            return arrIP
        except Exception, e:
            self.oe.dbg_log('tvbackend::get_bindaddr', 'ERROR: (' + repr(e) + ')')

    def exit(self):
        try:
            self.oe.dbg_log('tvbackend::exit', 'enter_function', 0)
            self.oe.dbg_log('tvbackend::exit', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('tvbackend::exit', 'ERROR: (%s)' % repr(e), 4)
