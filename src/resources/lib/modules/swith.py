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

class swith:

    ENABLED = False
    SET_DISEQC = None
    SAT_NAME_FILE = None
    SAT_NAME_TEMP = None
    GET_SAT_NAME = None

    D_LNB1 = None
    D_LNB2 = None
    D_LNB3 = None
    D_LNB4 = None

    D_SAT1 = None
    D_SAT2 = None
    D_SAT3 = None
    D_SAT4 = None

    D_POLAR1 = None
    D_POLAR2 = None
    D_POLAR3 = None
    D_POLAR4 = None

    menu = {'92': {
        'name': 47000,
        'menuLoader': 'load_menu',
        'listTyp': 'list',
        'InfoText': 4700,
        }}

    def __init__(self, oeMain):
        try:
            oeMain.dbg_log('diseqc::__init__', 'enter_function', 0)
            self.struct = {
                'diseqc': {
                    'order': 1,
                    'name': 47001,
                    'not_supported': [],
                    'settings': {
                        'lnb1': {
                            'order': 1,
                            'name': 47011,
                            'value': '1',
                            'action': 'initialize_diseqc',
                            'type': 'bool',
                            'InfoText': 4711,
                        },
                        'sat1': {
                            'order': 2,
                            'name': 47012,
                            'value': 'S36.0E  Eutelsat W4/W7',
                            'values': [],
                            'action': 'initialize_diseqc',
                            'type': 'multivalue',
                            'parent': {'entry': 'lnb1','value': ['1']},
                            'InfoText': 4712,
                        },
                        'polar1': {
                            'order': 3,
                            'name': 47013,
                            'value': 'Circular',
                            'values': ['Circular', 'Linear'],
                            'action': 'initialize_diseqc',
                            'type': 'multivalue',
                            'parent': {'entry': 'lnb1','value': ['1']},
                            'InfoText': 4713,
                        },
                        'lnb2': {
                            'order': 4,
                            'name': 47014,
                            'value': '0',
                            'action': 'initialize_diseqc',
                            'type': 'bool',
                            'InfoText': 4711,
                        },
                        'sat2': {
                            'order': 5,
                            'name': 47012,
                            'value': 'S4W     Amos 2/3',
                            'values': [],
                            'action': 'initialize_diseqc',
                            'type': 'multivalue',
                            'parent': {'entry': 'lnb2','value': ['1']},
                            'InfoText': 4712,
                        },
                        'polar2': {
                            'order': 5,
                            'name': 47013,
                            'value': 'Circular',
                            'values': ['Circular', 'Linear'],
                            'action': 'initialize_diseqc',
                            'type': 'multivalue',
                            'parent': {'entry': 'lnb2','value': ['1']},
                            'InfoText': 4713,
                        },
                        'lnb3': {
                            'order': 6,
                            'name': 47015,
                            'value': '0',
                            'action': 'initialize_diseqc',
                            'type': 'bool',
                            'InfoText': 4711,
                        },
                        'sat3': {
                            'order': 7,
                            'name': 47012,
                            'value': 'S4.9E   Astra 4A',
                            'values': [],
                            'action': 'initialize_diseqc',
                            'type': 'multivalue',
                            'parent': {'entry': 'lnb3','value': ['1']},
                            'InfoText': 4712,
                        },
                        'polar3': {
                            'order': 8,
                            'name': 47013,
                            'value': 'Circular',
                            'values': ['Circular', 'Linear'],
                            'action': 'initialize_diseqc',
                            'type': 'multivalue',
                            'parent': {'entry': 'lnb3','value': ['1']},
                            'InfoText': 4713,
                        },
                        'lnb4': {
                            'order': 9,
                            'name': 47016,
                            'value': '0',
                            'action': 'initialize_diseqc',
                            'type': 'bool',
                            'InfoText': 4711,
                        },
                        'sat4': {
                            'order': 10,
                            'name': 47012,
                            'value': 'S13E    Hotbird 6/8/9',
                            'values': [],
                            'action': 'initialize_diseqc',
                            'type': 'multivalue',
                            'parent': {'entry': 'lnb4','value': ['1']},
                            'InfoText': 4712,
                        },
                        'polar4': {
                            'order': 11,
                            'name': 47013,
                            'value': 'Circular',
                            'values': ['Circular', 'Linear'],
                            'action': 'initialize_diseqc',
                            'type': 'multivalue',
                            'parent': {'entry': 'lnb4','value': ['1']},
                            'InfoText': 4713,
                        },
                    },
                },
                'diseqc-set': {
                    'order': 2,
                    'name': 47020,
                    'not_supported': [],
                    'settings': {
                        'set_diseqc': {
                            'order': 1,
                            'name': 47021,
                            'value': '0',
                            'action': 'setup_diseqc',
                            'type': 'button',
                            'InfoText': 4721,
                        },
                    },
                },
            }

            self.oe = oeMain
            oeMain.dbg_log('diseqc::__init__', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('diseqc::__init__', 'ERROR: (%s)' % repr(e))

    def start_service(self):
        try:
            self.oe.dbg_log('diseqc::start_service', 'enter_function', 0)
            self.load_values()
            self.initialize_diseqc(service=1)
            self.oe.dbg_log('diseqc::start_service', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('diseqc::start_service', 'ERROR: (%s)' % repr(e))

    def stop_service(self):
        try:
            self.oe.dbg_log('diseqc::stop_service', 'enter_function', 0)
            self.oe.dbg_log('diseqc::stop_service', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('diseqc::stop_service', 'ERROR: (' + repr(e) + ')')

    def do_init(self):
        try:
            self.oe.dbg_log('diseqc::do_init', 'exit_function', 0)
            self.load_values()
            self.oe.dbg_log('diseqc::do_init', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('diseqc::do_init', 'ERROR: (%s)' % repr(e))

    def set_value(self, listItem):
        try:
            self.oe.dbg_log('diseqc::set_value', 'enter_function', 0)
            self.struct[listItem.getProperty('category')]['settings'
                    ][listItem.getProperty('entry')]['value'] = \
                listItem.getProperty('value')
            self.oe.dbg_log('diseqc::set_value', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('diseqc::set_value', 'ERROR: (' + repr(e) + ')')

    def load_menu(self, focusItem):
        try:
            self.oe.dbg_log('diseqc::load_menu', 'enter_function', 0)
            self.oe.winOeMain.build_menu(self.struct)
            self.oe.dbg_log('diseqc::load_menu', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('diseqc::load_menu', 'ERROR: (%s)' % repr(e))

    def load_values(self):
        try:
            self.oe.dbg_log('diseqc::load_values', 'enter_function', 0)

            if os.path.exists('/dev/dvb/adapter0/frontend0'):
                if 'hidden' in self.struct['diseqc']:
                    del self.struct['diseqc']['hidden']

                # Load Sat-list
                arrSatList = self.get_sat_list()
                self.struct['diseqc']['settings']['sat1']['values'] = arrSatList
                self.struct['diseqc']['settings']['sat2']['values'] = arrSatList
                self.struct['diseqc']['settings']['sat3']['values'] = arrSatList
                self.struct['diseqc']['settings']['sat4']['values'] = arrSatList

                self.struct['diseqc']['settings']['lnb1']['value'] = \
                self.oe.get_service_option('diseqc', 'LNB1', self.D_LNB1).replace('"', '')
                self.struct['diseqc']['settings']['sat1']['value'] = \
                self.oe.get_service_option('diseqc', 'SAT1', self.D_SAT1).replace('"', '')
                self.struct['diseqc']['settings']['polar1']['value'] = \
                self.oe.get_service_option('diseqc', 'POLAR1', self.D_POLAR1).replace('"', '')

                self.struct['diseqc']['settings']['lnb2']['value'] = \
                self.oe.get_service_option('diseqc', 'LNB2', self.D_LNB2).replace('"', '')
                self.struct['diseqc']['settings']['sat2']['value'] = \
                self.oe.get_service_option('diseqc', 'SAT2', self.D_SAT2).replace('"', '')
                self.struct['diseqc']['settings']['polar2']['value'] = \
                self.oe.get_service_option('diseqc', 'POLAR2', self.D_POLAR2).replace('"', '')

                self.struct['diseqc']['settings']['lnb3']['value'] = \
                self.oe.get_service_option('diseqc', 'LNB3', self.D_LNB3).replace('"', '')
                self.struct['diseqc']['settings']['sat3']['value'] = \
                self.oe.get_service_option('diseqc', 'SAT3', self.D_SAT3).replace('"', '')
                self.struct['diseqc']['settings']['polar3']['value'] = \
                self.oe.get_service_option('diseqc', 'POLAR3', self.D_POLAR3).replace('"', '')

                self.struct['diseqc']['settings']['lnb4']['value'] = \
                self.oe.get_service_option('diseqc', 'LNB4', self.D_LNB4).replace('"', '')
                self.struct['diseqc']['settings']['sat4']['value'] = \
                self.oe.get_service_option('diseqc', 'SAT4', self.D_SAT4).replace('"', '')
                self.struct['diseqc']['settings']['polar4']['value'] = \
                self.oe.get_service_option('diseqc', 'POLAR4', self.D_POLAR4).replace('"', '')

                if self.struct['diseqc']['settings']['lnb1']['value'] == '1' \
                        or self.struct['diseqc']['settings']['lnb2']['value'] == '1' \
                        or self.struct['diseqc']['settings']['lnb3']['value'] == '1' \
                        or self.struct['diseqc']['settings']['lnb4']['value'] == '1':
                    if 'hidden' in self.struct['diseqc-set']:
                        del self.struct['diseqc-set']['hidden']
                else:
                    self.struct['diseqc-set']['hidden'] = True

            else:
                self.struct['diseqc']['hidden'] = True
                self.struct['diseqc-set']['hidden'] = True

            self.oe.dbg_log('diseqc::load_values', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('diseqc::load_values', 'ERROR: (%s)' % repr(e))

    def initialize_diseqc(self, **kwargs):
        try:
            self.oe.dbg_log('diseqc::initialize_diseqc', 'enter_function', 0)
            self.oe.set_busy(1)
            if 'listItem' in kwargs:
                self.set_value(kwargs['listItem'])
            options = {}
            state = 0
            if os.path.exists('/dev/dvb/adapter0/frontend0'):
                state = 1

                if self.struct['diseqc']['settings']['lnb1']['value'] == '1' \
                      or self.struct['diseqc']['settings']['lnb2']['value'] == '1' \
                      or self.struct['diseqc']['settings']['lnb3']['value'] == '1' \
                      or self.struct['diseqc']['settings']['lnb4']['value'] == '1':
                    if 'hidden' in self.struct['diseqc-set']:
                        del self.struct['diseqc-set']['hidden']
                else:
                    self.struct['diseqc-set']['hidden'] = True

                options['LNB1']   = '"%s"' % self.struct['diseqc']['settings']['lnb1']['value']
                options['SAT1']   = '"%s"' % self.struct['diseqc']['settings']['sat1']['value']
                options['POLAR1'] = '"%s"' % self.struct['diseqc']['settings']['polar1']['value']

                options['LNB2']   = '"%s"' % self.struct['diseqc']['settings']['lnb2']['value']
                options['SAT2']   = '"%s"' % self.struct['diseqc']['settings']['sat2']['value']
                options['POLAR2'] = '"%s"' % self.struct['diseqc']['settings']['polar2']['value']

                options['LNB3']   = '"%s"' % self.struct['diseqc']['settings']['lnb3']['value']
                options['SAT3']   = '"%s"' % self.struct['diseqc']['settings']['sat3']['value']
                options['POLAR3'] = '"%s"' % self.struct['diseqc']['settings']['polar3']['value']

                options['LNB4']   = '"%s"' % self.struct['diseqc']['settings']['lnb4']['value']
                options['SAT4']   = '"%s"' % self.struct['diseqc']['settings']['sat4']['value']
                options['POLAR4'] = '"%s"' % self.struct['diseqc']['settings']['polar4']['value']

            self.oe.set_service('diseqc', options, state)
            self.oe.set_busy(0)
            self.oe.dbg_log('diseqc::initialize_diseqc', 'exit_function', 0)
        except Exception, e:
            self.oe.set_busy(0)
            self.oe.dbg_log('diseqc::initialize_diseqc', 'ERROR: (%s)' % repr(e), 4)

    def get_sat_list(self): 
        try:
            self.oe.dbg_log('diseqc::get_sat_list', 'enter_function', 0)
            arrSat = ['none']
            if os.path.exists(self.SAT_NAME_FILE):
                self.oe.execute(self.GET_SAT_NAME, 0)
                for satellite in open(self.SAT_NAME_TEMP).readlines():
                    arrSat.append(satellite.strip())
            self.oe.dbg_log('diseqc::get_sat_list', 'exit_function', 0)
            return arrSat
        except Exception, e:
            self.oe.dbg_log('diseqc::get_sat_list', 'ERROR: (' + repr(e) + ')')

    def setup_diseqc(self, listItem=None):
        try:
            self.oe.dbg_log('diseqc-set::setup_diseqc', 'enter_function', 0)
            if os.path.exists(self.SET_DISEQC):
                info_diseqc = self.oe.execute(self.SET_DISEQC, 1)
                xbmcDialog = xbmcgui.Dialog()
                answer = xbmcDialog.ok('DiSEqC',
                            'Create DiSEqC file:  %s' % info_diseqc)
        except Exception, e:
            self.oe.dbg_log('diseqc-set::setup_diseqc', 'ERROR: (' + repr(e) + ')')

    def exit(self):
        try:
            self.oe.dbg_log('diseqc::exit', 'enter_function', 0)
            self.oe.dbg_log('diseqc::exit', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('diseqc::exit', 'ERROR: (%s)' % repr(e), 4)
