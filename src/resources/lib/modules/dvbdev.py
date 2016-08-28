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

class dvbdev:

    ENABLED=False
    GET_DVB_FRONTEND = None
    GET_DVB_DRIVER = None
    D_DVB_DRIVERS = None
    GET_DVB_DRVLIST = None
    DVB_LIST_TEMP = None
    COUNT_DVB = None
    D_DVB_NUMBER = None
    D_DVB_TIME = None

    menu = {'7': {
        'name': 35000,
        'menuLoader': 'load_menu',
        'listTyp': 'list',
        'InfoText': 3500,
        }}

    def __init__(self, oeMain):
        try:
            oeMain.dbg_log('dvbdev::__init__', 'enter_function', 0)
            self.struct = {
                'dvb-driver': {
                    'order': 1,
                    'name': 35010,
                    'not_supported': [],
                    'settings': {
                        'dvb_driver': {
                            'order': 1,
                            'name': 35011,
                            'value': None,
                            'values': [],
                            'action': 'initialize_dvb',
                            'type': 'multivalue',
                            'InfoText': 3511,
                        },
                        'view_driver': {
                            'order': 2,
                            'name': 35012,
                            'value': None,
                            'action': 'get_dvb_driver',
                            'type': 'button',
                            'InfoText': 3512,
                        },
                    },
                },
                'dvb-wait': {
                    'order': 2,
                    'name': 35020,
                    'not_supported': [],
                    'settings': {
                        'enable_wait': {
                            'order': 1,
                            'name': 35021,
                            'value': '0',
                            'action': 'initialize_waitdvb',
                            'type': 'bool',
                            'InfoText': 3521,
                        },
                        'dvb_number': {
                            'order': 2,
                            'name': 35022,
                            'value': '0',
                            'values': [],
                            'action': 'initialize_waitdvb',
                            'type': 'multivalue',
                            'parent': {'entry': 'enable_wait','value': ['1']},
                            'InfoText': 3522,
                        },
                        'wait_time': {
                            'order': 3,
                            'name': 35023,
                            'value': '5',
                            'values': ['5', '10', '15', '20', '30', '40', '50', '60'],
                            'action': 'initialize_waitdvb',
                            'type': 'multivalue',
                            'parent': {'entry': 'enable_wait','value': ['1']},
                            'InfoText': 3523,
                        },
                    },
                },
            }

            self.oe = oeMain
            oeMain.dbg_log('dvbdev::__init__', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('dvbdev::__init__', 'ERROR: (%s)' % repr(e))

    def start_service(self):
        try:
            self.oe.dbg_log('dvbdev::start_service', 'enter_function', 0)
            self.load_values()
            self.initialize_dvb(service=1)
            self.initialize_waitdvb(service=1)
            self.oe.dbg_log('dvbdev::start_service', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('dvbdev::start_service', 'ERROR: (%s)' % repr(e))

    def stop_service(self):
        try:
            self.oe.dbg_log('dvbdev::stop_service', 'enter_function', 0)
            self.oe.dbg_log('dvbdev::stop_service', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('dvbdev::stop_service', 'ERROR: (' + repr(e) + ')')

    def do_init(self):
        try:
            self.oe.dbg_log('dvbdev::do_init', 'exit_function', 0)
            self.load_values()
            self.oe.dbg_log('dvbdev::do_init', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('dvbdev::do_init', 'ERROR: (%s)' % repr(e))

    def set_value(self, listItem):
        try:
            self.oe.dbg_log('dvbdev::set_value', 'enter_function', 0)

            self.struct[listItem.getProperty('category')]['settings'
                    ][listItem.getProperty('entry')]['value'] = \
                listItem.getProperty('value')

            self.oe.dbg_log('dvbdev::set_value', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('dvbdev::set_value', 'ERROR: (' + repr(e) + ')')

    def load_menu(self, focusItem):
        try:
            self.oe.dbg_log('dvbdev::load_menu', 'enter_function', 0)
            self.oe.winOeMain.build_menu(self.struct)
            self.oe.dbg_log('dvbdev::load_menu', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('dvbdev::load_menu', 'ERROR: (%s)' % repr(e))

    def load_values(self):
        try:
            self.oe.dbg_log('dvbdev::load_values', 'enter_function', 0)

            # DVB_DRIVERS
            arrDVBdrv = self.get_dvb_list()
            self.struct['dvb-driver']['settings']['dvb_driver']['values'] = arrDVBdrv
            self.struct['dvb-driver']['settings']['dvb_driver']['value'] = \
            self.oe.get_service_option('dvb-driver', 'DVB_DRIVERS', self.D_DVB_DRIVERS).replace('"', '')

            # WAIT DVB FRONTEND
            self.struct['dvb-wait']['settings']['enable_wait']['value'] = self.oe.get_service_state('dvb-wait')
            if os.path.exists('/dev/dvb/adapter0/frontend0'):
                if 'hidden' in self.struct['dvb-wait']:
                    del self.struct['dvb-wait']['hidden']
                arrDvbCount = self.get_dvb_count()
                if not arrDvbCount is None:
                    self.struct['dvb-wait']['settings']['dvb_number']['values'] = arrDvbCount
                self.struct['dvb-wait']['settings']['dvb_number']['value'] = \
                self.oe.get_service_option('dvb-wait', 'DVB_NUMBER', self.D_DVB_NUMBER).replace('"', '')
                self.struct['dvb-wait']['settings']['wait_time']['value'] = \
                self.oe.get_service_option('dvb-wait', 'DVB_TIME', self.D_DVB_TIME).replace('"', '')
            else:
                self.struct['dvb-wait']['hidden'] = 'true'

            self.oe.dbg_log('dvbdev::load_values', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('dvbdev::load_values', 'ERROR: (%s)' % repr(e))

    def initialize_dvb(self, **kwargs):
        try:
            self.oe.dbg_log('dvbdev::initialize_dvb', 'enter_function', 0)
            self.oe.set_busy(1)
            if 'listItem' in kwargs:
                self.set_value(kwargs['listItem'])
            options = {}
            state = 1
            options['DVB_DRIVERS']  = '"%s"' % self.struct['dvb-driver']['settings']['dvb_driver']['value']
            self.oe.set_service('dvb-driver', options, state)
            self.oe.set_busy(0)
            self.oe.dbg_log('dvbdev::initialize_dvb', 'exit_function', 0)
        except Exception, e:
            self.oe.set_busy(0)
            self.oe.dbg_log('dvbdev::initialize_dvb', 'ERROR: (%s)' % repr(e))

    def get_dvb_driver(self, listItem=None):
        try:
            self.oe.dbg_log('dvbdev::get_dvb_driver', 'enter_function', 0)
            #GET_DVB_FRONTEND
            txt_device = self.oe.execute(self.GET_DVB_FRONTEND, 1)
            #GET_DVB_DRIVER
            info_driver = self.oe.execute(self.GET_DVB_DRIVER, 1).strip()

            if info_driver == 'mb':
                txt_driver = 'MEDIA (media_build)'
            elif info_driver == 'tbs':
                txt_driver = 'TBS (CrazyCat)'
            elif info_driver == 'core':
                txt_driver = 'CORE (Linux kernel)'
            else:
                txt_driver = 'Unknown...'

            xbmcDialog = xbmcgui.Dialog()
            answer = xbmcDialog.ok('DVB Info',
                            'Curent DVB drivers:  %s' % txt_driver, ' ',
                            'DVB device: %s' % txt_device)

        except Exception, e:
            self.oe.dbg_log('dvbdev::get_dvb_driver', 'ERROR: (%s)' % repr(e))

    def get_dvb_list(self):
        try:
            self.oe.dbg_log('dvbdev::get_dvb_list', 'enter_function', 0)
            arrListDvb = []
            self.oe.execute(self.GET_DVB_DRVLIST, 0)
            for drvlist in open(self.DVB_LIST_TEMP).readlines():
                arrListDvb.append(drvlist.strip())
            arrListDvb.sort()
            self.oe.dbg_log('scan::get_dvb_list', 'exit_function', 0)
            return arrListDvb
        except Exception, e:
            self.oe.dbg_log('dvbdev::get_dvb_list', 'ERROR: (%s)' % repr(e))

    def initialize_waitdvb(self, **kwargs):
        try:
            self.oe.dbg_log('dvbdev::initialize_waitdvb', 'enter_function', 0)
            self.oe.set_busy(1)
            if 'listItem' in kwargs:
                self.set_value(kwargs['listItem'])
            options = {}
            state = 0
            if self.struct['dvb-wait']['settings']['enable_wait']['value'] == '1':
                state = 1
                options['DVB_NUMBER'] = '"%s"' % self.struct['dvb-wait']['settings']['dvb_number']['value']
                options['DVB_TIME']  = '"%s"' % self.struct['dvb-wait']['settings']['wait_time']['value']
            self.oe.set_service('dvb-wait', options, state)
            self.oe.set_busy(0)
            self.oe.dbg_log('dvbdev::initialize_waitdvb', 'exit_function', 0)
        except Exception, e:
            self.oe.set_busy(0)
            self.oe.dbg_log('dvbdev::initialize_waitdvb', 'ERROR: (%s)' % repr(e))

    def get_dvb_count(self):
        try:
            self.oe.dbg_log('dvb-wait::get_dvb_count', 'enter_function', 0)
            arrCnt = []
            cnt = 0
            cntdvb = self.oe.execute(self.COUNT_DVB, 1)
            while cnt < int(cntdvb):
                arrCnt.append(str(cnt))
                cnt += 1
            arrCnt.sort()
            self.oe.dbg_log('dvb-wait::get_dvb_count', 'exit_function', 0)
            return arrCnt
        except Exception, e:
            self.oe.dbg_log('dvb-wait::get_dvb_count', 'ERROR: (%s)' % repr(e))

    def exit(self):
        try:
            self.oe.dbg_log('dvbdev::exit', 'enter_function', 0)
            self.oe.dbg_log('dvbdev::exit', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('dvbdev::exit', 'ERROR: (%s)' % repr(e))
