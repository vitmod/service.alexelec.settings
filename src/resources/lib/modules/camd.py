################################################################################
#      This file is part of Alex@ELEC - http://www.alexelec.in.ua
#      Copyright (C) 2011-2016 Alexandr Zuyev (alex@alexelec.in.ua)
################################################################################
# -*- coding: utf-8 -*-

import os
import glob

class camd:

    ENABLED = False
    D_WICARD_TYPE = None
    D_WICARD_DEBUG = None
    D_OSCAM_TYPE = None
    
    menu = {'8': {
        'name': 36000,
        'menuLoader': 'load_menu',
        'listTyp': 'list',
        'InfoText': 3600,
        }}

    def __init__(self, oeMain):
        try:
            oeMain.dbg_log('camd::__init__', 'enter_function', 0)
            self.struct = {
                'wicard': {
                    'order': 1,
                    'name': 36010,
                    'not_supported': [],
                    'settings': {
                        'enable_wicard': {
                            'order': 1,
                            'name': 36011,
                            'value': '0',
                            'action': 'initialize_wicard',
                            'type': 'bool',
                            'InfoText': 3611,
                        },
                        'wicard_type': {
                            'order': 2,
                            'name': 36012,
                            'value': 'TVON',
                            'values': ['ALL', 'TVON'],
                            'action': 'initialize_wicard',
                            'type': 'multivalue',
                            'parent': {'entry': 'enable_wicard','value': ['1']},
                            'InfoText': 3612,
                        },
                        'wicard_debug': {
                            'order': 3,
                            'name': 36013,
                            'value': '0',
                            'action': 'initialize_wicard',
                            'type': 'bool',
                            'parent': {'entry': 'enable_wicard','value': ['1']},
                            'InfoText': 3613,
                        },
                    },
                },
                'oscam': {
                    'order': 2,
                    'name': 36020,
                    'not_supported': [],
                    'settings': {
                        'enable_oscam': {
                            'order': 1,
                            'name': 36021,
                            'value': '0',
                            'action': 'initialize_oscam',
                            'type': 'bool',
                            'InfoText': 3621,
                        },
                        'oscam_type': {
                            'order': 2,
                            'name': 36022,
                            'value': 'TVON',
                            'values': ['ALL', 'TVON'],
                            'action': 'initialize_oscam',
                            'type': 'multivalue',
                            'parent': {'entry': 'enable_oscam','value': ['1']},
                            'InfoText': 3622,
                        },
                    },
                },
            }

            self.oe = oeMain
            oeMain.dbg_log('camd::__init__', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('camd::__init__', 'ERROR: (%s)' % repr(e))

    def start_service(self):
        try:
            self.oe.dbg_log('camd::start_service', 'enter_function', 0)
            self.load_values()
            self.initialize_wicard(service=1)
            self.initialize_oscam(service=1)
            self.oe.dbg_log('camd::start_service', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('camd::start_service', 'ERROR: (%s)' % repr(e))

    def stop_service(self):
        try:
            self.oe.dbg_log('camd::stop_service', 'enter_function', 0)
            self.oe.dbg_log('camd::stop_service', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('camd::stop_service', 'ERROR: (' + repr(e) + ')')

    def do_init(self):
        try:
            self.oe.dbg_log('camd::do_init', 'exit_function', 0)
            self.load_values()
            self.oe.dbg_log('camd::do_init', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('camd::do_init', 'ERROR: (%s)' % repr(e))

    def set_value(self, listItem):
        try:
            self.oe.dbg_log('camd::set_value', 'enter_function', 0)
            self.struct[listItem.getProperty('category')]['settings'][listItem.getProperty('entry')]['value'] = listItem.getProperty('value')
            self.oe.dbg_log('camd::set_value', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('camd::set_value', 'ERROR: (' + repr(e) + ')')

    def load_menu(self, focusItem):
        try:
            self.oe.dbg_log('camd::load_menu', 'enter_function', 0)
            self.oe.winOeMain.build_menu(self.struct)
            self.oe.dbg_log('camd::load_menu', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('camd::load_menu', 'ERROR: (%s)' % repr(e))

    def load_values(self):
        try:
            self.oe.dbg_log('camd::load_values', 'enter_function', 0)
            # WICARD_DAEMON
            self.struct['wicard']['settings']['enable_wicard']['value'] = self.oe.get_service_state('wicard')

            self.struct['wicard']['settings']['wicard_type']['value'] = \
            self.oe.get_service_option('wicard', 'WICARD_TYPE', self.D_WICARD_TYPE).replace('"', '')

            self.struct['wicard']['settings']['wicard_debug']['value'] = \
            self.oe.get_service_option('wicard', 'WICARD_DEBUG', self.D_WICARD_DEBUG).replace('"', '')

            # OSCAM_DAEMON
            self.struct['oscam']['settings']['enable_oscam']['value'] = self.oe.get_service_state('oscam')

            self.struct['oscam']['settings']['oscam_type']['value'] = \
            self.oe.get_service_option('oscam', 'OSCAM_TYPE', self.D_OSCAM_TYPE).replace('"', '')
            
            self.oe.dbg_log('camd::load_values', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('camd::load_values', 'ERROR: (%s)' % repr(e))

    def initialize_wicard(self, **kwargs):
        try:
            self.oe.dbg_log('camd::initialize_wicard', 'enter_function', 0)
            self.oe.set_busy(1)
            if 'listItem' in kwargs:
                self.set_value(kwargs['listItem'])
            options = {}
            state = 0
            if self.struct['wicard']['settings']['enable_wicard']['value'] == '1':
                state = 1
                options['WICARD_TYPE']  = '"%s"' % self.struct['wicard']['settings']['wicard_type']['value']
                options['WICARD_DEBUG'] = '"%s"' % self.struct['wicard']['settings']['wicard_debug']['value']
            self.oe.set_service('wicard', options, state)
            self.oe.set_busy(0)
            self.oe.dbg_log('camd::initialize_wicard', 'exit_function', 0)
        except Exception, e:
            self.oe.set_busy(0)
            self.oe.dbg_log('camd::initialize_wicard', 'ERROR: (%s)' % repr(e), 4)

    def initialize_oscam(self, **kwargs):
        try:
            self.oe.dbg_log('camd::initialize_oscam', 'enter_function', 0)
            self.oe.set_busy(1)
            if 'listItem' in kwargs:
                self.set_value(kwargs['listItem'])
            options = {}
            state = 0
            if self.struct['oscam']['settings']['enable_oscam']['value'] == '1':
                state = 1
                options['OSCAM_TYPE'] = '"%s"' % self.struct['oscam']['settings']['oscam_type']['value']
            self.oe.set_service('oscam', options, state)
            self.oe.set_busy(0)
            self.oe.dbg_log('camd::initialize_oscam', 'exit_function', 0)
        except Exception, e:
            self.oe.set_busy(0)
            self.oe.dbg_log('camd::initialize_oscam', 'ERROR: (%s)' % repr(e), 4)

    def exit(self):
        try:
            self.oe.dbg_log('camd::exit', 'enter_function', 0)
            self.oe.dbg_log('camd::exit', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('camd::exit', 'ERROR: (%s)' % repr(e), 4)
