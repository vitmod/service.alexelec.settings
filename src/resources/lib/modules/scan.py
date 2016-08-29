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
import oeWindows
import threading
import subprocess

class scan:

    ENABLED = False
    RUN_SCAN = None
    KILL_SCAN = None
    TUNER_LIST = None
    TUNER_LIST_TEMP = None

    S2_SAT_NAME_FILE = None
    S2_SAT_NAME_TEMP = None
    S2_GET_SAT_NAME = None
    S2_TPL_DIR = None
    S2_GET_TPL_LIST = None
    S2_TPL_LIST_FILE = None
    S2_GET_TPL_COUNT = None
    S2_GET_LOG = None
    S2_DEL_LOG = None

    D_S2_TUNER = None
    D_S2_TYPE = None
    D_S2_LNB = None
    D_S2_SAT = None
    D_S2_POLAR = None
    D_S2_FILE = None
    D_S2_SERVICE = None
    D_S2_FTA = None
    D_S2_UPDATE = None
    D_S2_SORT = None
    D_S2_SPEED = None
    
    menu = {'93': {
        'name': 48000,
        'menuLoader': 'load_menu',
        'listTyp': 'list',
        'InfoText': 4800,
        }}

    def __init__(self, oeMain):
        try:
            oeMain.dbg_log('scan::__init__', 'enter_function', 0)
            self.struct = {
                'scan': {
                    'order': 1,
                    'name': 48001,
                    'not_supported': [],
                    'settings': {
                        's2_tuner': {
                            'order': 1,
                            'name': 48011,
                            'value': 'none',
                            'values': [],
                            'action': 'initialize_scan',
                            'type': 'multivalue',
                            'InfoText': 4811,
                        },
                        's2_type': {
                            'order': 2,
                            'name': 48012,
                            'value': 'S2',
                            'values': ['S2', 'T2'],
                            'action': 'initialize_scan',
                            'type': 'multivalue',
                            'InfoText': 4812,
                        },
                        's2_lnb': {
                            'order': 3,
                            'name': 48013,
                            'value': '1',
                            'values': ['1', '2', '3', '4'],
                            'action': 'initialize_scan',
                            'type': 'multivalue',
                            'parent': {'entry': 's2_type','value': ['S2']},
                            'InfoText': 4813,
                        },
                        's2_sat': {
                            'order': 4,
                            'name': 48014,
                            'value': 'S36.0E  Eutelsat W4/W7',
                            'values': [],
                            'action': 'initialize_scan',
                            'type': 'multivalue',
                            'parent': {'entry': 's2_type','value': ['S2']},
                            'InfoText': 4814,
                        },
                        's2_polar': {
                            'order': 5,
                            'name': 48015,
                            'value': 'Circular',
                            'values': ['Circular', 'Linear'],
                            'action': 'initialize_scan',
                            'type': 'multivalue',
                            'parent': {'entry': 's2_type','value': ['S2']},
                            'InfoText': 4815,
                        },
                        's2_file': {
                            'order': 6,
                            'name': 48016,
                            'value': 'S36.0E-HTB.cfg',
                            'values': [],
                            'action': 'initialize_scan',
                            'type': 'multivalue',
                            'InfoText': 4816,
                        },
                        's2_service': {
                            'order': 7,
                            'name': 48017,
                            'value': 'All',
                            'values': ['All', 'TV'],
                            'action': 'initialize_scan',
                            'type': 'multivalue',
                            'InfoText': 4817,
                        },
                        's2_fta': {
                            'order': 8,
                            'name': 48018,
                            'value': 'All',
                            'values': ['All', 'FTA'],
                            'action': 'initialize_scan',
                            'type': 'multivalue',
                            'InfoText': 4818,
                        },
                        's2_update': {
                            'order': 9,
                            'name': 48019,
                            'value': '0',
                            'action': 'initialize_scan',
                            'type': 'bool',
                            'InfoText': 4819,
                        },
                        's2_sort': {
                            'order': 10,
                            'name': 48020,
                            'value': '1',
                            'action': 'initialize_scan',
                            'type': 'bool',
                            'InfoText': 4820,
                        },
                        's2_speed': {
                            'order': 11,
                            'name': 48021,
                            'value': 'Default',
                            'values': ['Default', 'Fast', 'Slow'],
                            'action': 'initialize_scan',
                            'type': 'multivalue',
                            'InfoText': 4821,
                        },
                    },
                },
                'scan-run': {
                    'order': 2,
                    'name': 48030,
                    'not_supported': [],
                    'settings': {
                        'scan_run': {
                            'order': 1,
                            'name': 48031,
                            'value': '0',
                            'action': 'execute_scan',
                            'type': 'button',
                            'InfoText': 4831,
                        },
                    },
                },
            }

            self.oe = oeMain
            oeMain.dbg_log('scan::__init__', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('scan::__init__', 'ERROR: (%s)' % repr(e))

    def start_service(self):
        try:
            self.oe.dbg_log('scan::start_service', 'enter_function' , 0)
            self.load_values()
            self.initialize_scan(service=1)
            self.oe.dbg_log('scan::start_service', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('scan::start_service', 'ERROR: (%s)' % repr(e))

    def stop_service(self):
        try:
            self.oe.dbg_log('scan::stop_service', 'enter_function', 0)
            self.oe.dbg_log('scan::stop_service', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('scan::stop_service', 'ERROR: (' + repr(e) + ')')

    def do_init(self):
        try:
            self.oe.dbg_log('scan::do_init', 'exit_function', 0)
            self.load_values()
            self.oe.dbg_log('scan::do_init', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('scan::do_init', 'ERROR: (%s)' % repr(e))

    def set_value(self, listItem):
        try:
            self.oe.dbg_log('scan::set_value', 'enter_function', 0)
            self.struct[listItem.getProperty('category')]['settings'
                    ][listItem.getProperty('entry')]['value'] = \
                listItem.getProperty('value')
            self.oe.dbg_log('scan::set_value', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('scan::set_value', 'ERROR: (' + repr(e) + ')')

    def load_menu(self, focusItem):
        try:
            self.oe.dbg_log('scan::load_menu', 'enter_function', 0)
            self.oe.winOeMain.build_menu(self.struct)
            self.oe.dbg_log('scan::load_menu', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('scan::load_menu', 'ERROR: (%s)' % repr(e))

    def load_values(self):
        try:
            self.oe.dbg_log('scan::load_values', 'enter_function', 0)

            if os.path.exists('/dev/dvb/adapter0/frontend0'):
                if 'hidden' in self.struct['scan']:
                    del self.struct['scan']['hidden']
                if 'hidden' in self.struct['scan-run']:
                    del self.struct['scan-run']['hidden']

                # DVB Device
                arrS2tuner = self.get_tuner_list()
                self.struct['scan']['settings']['s2_tuner']['values'] = arrS2tuner

                # Load Sat-list
                arrSatList = self.get_s2_sat_list()
                self.struct['scan']['settings']['s2_sat']['values'] = arrSatList

                # Load TPL-list file
                arrTplList = self.get_s2_config_file()
                self.struct['scan']['settings']['s2_file']['values'] = arrTplList

                self.struct['scan']['settings']['s2_tuner']['value'] = \
                self.oe.get_service_option('scan', 'S2_TUNER', self.D_S2_TUNER).replace('"', '')
                self.struct['scan']['settings']['s2_type']['value'] = \
                self.oe.get_service_option('scan', 'S2_TYPE', self.D_S2_TYPE).replace('"', '')
                self.struct['scan']['settings']['s2_lnb']['value'] = \
                self.oe.get_service_option('scan', 'S2_LNB', self.D_S2_LNB).replace('"', '')
                self.struct['scan']['settings']['s2_sat']['value'] = \
                self.oe.get_service_option('scan', 'S2_SAT', self.D_S2_SAT).replace('"', '')
                self.struct['scan']['settings']['s2_polar']['value'] = \
                self.oe.get_service_option('scan', 'S2_POLAR', self.D_S2_POLAR).replace('"', '')
                self.struct['scan']['settings']['s2_file']['value'] = \
                self.oe.get_service_option('scan', 'S2_FILE', self.D_S2_FILE).replace('"', '')
                self.struct['scan']['settings']['s2_service']['value'] = \
                self.oe.get_service_option('scan', 'S2_SERVICE', self.D_S2_SERVICE).replace('"', '')
                self.struct['scan']['settings']['s2_fta']['value'] = \
                self.oe.get_service_option('scan', 'S2_FTA', self.D_S2_FTA).replace('"', '')
                self.struct['scan']['settings']['s2_update']['value'] = \
                self.oe.get_service_option('scan', 'S2_UPDATE', self.D_S2_UPDATE).replace('"', '')
                self.struct['scan']['settings']['s2_sort']['value'] = \
                self.oe.get_service_option('scan', 'S2_SORT', self.D_S2_SORT).replace('"', '')
                self.struct['scan']['settings']['s2_speed']['value'] = \
                self.oe.get_service_option('scan', 'S2_SPEED', self.D_S2_SPEED).replace('"', '')

                if self.struct['scan']['settings']['s2_sat']['value'] == 'none' \
                      or self.struct['scan']['settings']['s2_file']['value'] == 'none' \
                      or self.struct['scan']['settings']['s2_tuner']['value'] == 'none':
                    self.struct['scan-run']['hidden'] = True
                else:
                    if 'hidden' in self.struct['scan-run']:
                        del self.struct['scan-run']['hidden']

            else:
                self.struct['scan']['hidden'] = True
                self.struct['scan-run']['hidden'] = True

            self.oe.dbg_log('scan::load_values', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('scan::load_values', 'ERROR: (%s)' % repr(e))

    def initialize_scan(self, **kwargs):
        try:
            self.oe.dbg_log('scan::initialize_scan', 'enter_function', 0)
            self.oe.set_busy(1)
            if 'listItem' in kwargs:
                self.set_value(kwargs['listItem'])
            options = {}
            state = 1

            if self.struct['scan']['settings']['s2_sat']['value'] == 'none' \
                  or self.struct['scan']['settings']['s2_file']['value'] == 'none' \
                  or self.struct['scan']['settings']['s2_tuner']['value'] == 'none':
                self.struct['scan-run']['hidden'] = True
            else:
                if 'hidden' in self.struct['scan-run']:
                    del self.struct['scan-run']['hidden']

            options['S2_TUNER']    = '"%s"' % self.struct['scan']['settings']['s2_tuner']['value']
            options['S2_TYPE']     = '"%s"' % self.struct['scan']['settings']['s2_type']['value']
            options['S2_LNB']      = '"%s"' % self.struct['scan']['settings']['s2_lnb']['value']
            options['S2_SAT']      = '"%s"' % self.struct['scan']['settings']['s2_sat']['value']
            options['S2_POLAR']    = '"%s"' % self.struct['scan']['settings']['s2_polar']['value']
            options['S2_FILE']     = '"%s"' % self.struct['scan']['settings']['s2_file']['value']
            options['S2_SERVICE']  = '"%s"' % self.struct['scan']['settings']['s2_service']['value']
            options['S2_FTA']      = '"%s"' % self.struct['scan']['settings']['s2_fta']['value']
            options['S2_UPDATE']   = '"%s"' % self.struct['scan']['settings']['s2_update']['value']
            options['S2_SORT']     = '"%s"' % self.struct['scan']['settings']['s2_sort']['value']
            options['S2_SPEED']    = '"%s"' % self.struct['scan']['settings']['s2_speed']['value']

            self.oe.set_service('scan', options, state)
            self.oe.set_busy(0)
            self.oe.dbg_log('scan::initialize_scan', 'exit_function', 0)
        except Exception, e:
            self.oe.set_busy(0)
            self.oe.dbg_log('scan::initialize_scan', 'ERROR: (%s)' % repr(e), 4)

    def get_s2_sat_list(self): 
        try:
            self.oe.dbg_log('scan::get_s2_sat_list', 'enter_function', 0)
            arrSat = ['none']
            if os.path.exists(self.S2_SAT_NAME_FILE):
                self.oe.execute(self.S2_GET_SAT_NAME, 0)
                for satellite in open(self.S2_SAT_NAME_TEMP).readlines():
                    arrSat.append(satellite.strip())
            self.oe.dbg_log('scan::get_s2_sat_list', 'exit_function', 0)
            return arrSat
        except Exception, e:
            self.oe.dbg_log('scan::get_s2_sat_list', 'ERROR: (' + repr(e) + ')')

    def get_s2_config_file(self): 
        try:
            self.oe.dbg_log('scan::get_s2_config_file', 'enter_function', 0)
            arrTpl = ['none']
            if os.path.exists(self.S2_TPL_DIR):
                self.oe.execute(self.S2_GET_TPL_LIST, 0)
                for tpl in open(self.S2_TPL_LIST_FILE).readlines():
                    arrTpl.append(os.path.basename(tpl.strip()))
            self.oe.dbg_log('scan::get_s2_config_file', 'exit_function', 0)
            return arrTpl
        except Exception, e:
            self.oe.dbg_log('scan::get_s2_config_file', 'ERROR: (' + repr(e) + ')')

    def execute_scan(self, listItem=None):
        try:
            self.oe.dbg_log('scan::execute_scan', 'enter_function', 0)

            if os.path.exists(self.RUN_SCAN):
                self.oe.execute(self.S2_DEL_LOG, 0)
                tpl_count = self.oe.execute(self.S2_GET_TPL_COUNT, 1).strip()
                tpl_count = int(tpl_count)
                subprocess.Popen(self.RUN_SCAN,
                                    shell=True, 
                                    close_fds=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)

                xbmcDialog = xbmcgui.DialogProgress()
                xbmcDialog.create('VDR channel Scan',
                            "",
                            'Number transponders in list:  %d' % tpl_count)

                message = self.oe.execute(self.S2_GET_LOG, 1).strip()
                message_tmp = message
                i = 0
                max_count = tpl_count + 1
                while not 'Found service' in message:
                    percent = int((i / float(tpl_count)) * 100)
                    message = self.oe.execute(self.S2_GET_LOG, 1).strip()
                    if message_tmp != message:
                        message_tmp = message
                        if i < max_count:
                            i = i + 1
                    xbmcDialog.update(percent, "", "", message)
                    xbmc.sleep(500)
                    if xbmcDialog.iscanceled():
                        self.oe.execute(self.KILL_SCAN, 0)
                        break

                xbmc.sleep(3000)
                xbmcDialog.close()

        except Exception, e:
            self.oe.dbg_log('scan::execute_scan', 'ERROR: (' + repr(e) + ')')

    def get_tuner_list(self):
        try:
            self.oe.dbg_log('scan::get_tuner_list', 'enter_function', 0)
            arrTunerlist = ['none']
            self.oe.execute(self.TUNER_LIST, 0)
            for dvbunit in open(self.TUNER_LIST_TEMP).readlines():
                arrTunerlist.append(dvbunit.strip())
            self.oe.dbg_log('scan::get_tuner_list', 'exit_function', 0)
            return arrTunerlist
        except Exception, e:
            self.oe.dbg_log('scan::get_tuner_list', 'ERROR: (' + repr(e) + ')')

    def exit(self):
        try:
            self.oe.dbg_log('scan::exit', 'enter_function', 0)
            self.oe.dbg_log('scan::exit', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('scan::exit', 'ERROR: (%s)' % repr(e), 4)
