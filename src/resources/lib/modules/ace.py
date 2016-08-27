################################################################################
#      This file is part of Alex@ELEC - http://www.alexelec.in.ua
#      Copyright (C) 2011-2016 Alexandr Zuyev (alex@alexelec.in.ua)
################################################################################
# -*- coding: utf-8 -*-

import os
import glob

class ace:

    ENABLED=False
    D_ACE_CACHE_TYPE = None
    D_ACE_CACHE_LIMIT = None
    D_ACE_LIFE_CACHE_SIZE = None
    D_ACE_LIFE_BUFFER = None
    D_ACE_CACHE_DIR = None
    D_ACE_CLEAN_CACHE = None
    D_ACE_DEBUG = None
    D_ACE_LOGIN = None
    D_ACE_PASSW = None
    D_ACE_ALWAYS = None
    D_ACEPROXY_LOGIN = None
    D_ACEPROXY_PASSW = None
    D_ACEPROXY_DEBUG = None
    D_ACEPROXY_ALWAYS = None

    menu = {'6': {
        'name': 34000,
        'menuLoader': 'load_menu',
        'listTyp': 'list',
        'InfoText': 3400,
        }}

    def __init__(self, oeMain):
        try:
            oeMain.dbg_log('ace::__init__', 'enter_function', 0)
            self.struct = {
                'acestream': {
                    'order': 1,
                    'name': 34010,
                    'not_supported': [],
                    'settings': {
                        'enable_acestream': {
                            'order': 1,
                            'name': 34011,
                            'value': None,
                            'action': 'initialize_acestream',
                            'type': 'bool',
                            'InfoText': 3411,
                            },
                        'ace_login': {
                            'order': 2,
                            'name': 34012,
                            'value': None,
                            'action': 'initialize_acestream',
                            'type': 'text',
                            'parent': {
                                'entry': 'enable_acestream',
                                'value': ['1']
                                },
                            'InfoText': 3412,
                            },
                        'ace_passw': {
                            'order': 3,
                            'name': 34013,
                            'value': None,
                            'action': 'initialize_acestream',
                            'type': 'text',
                            'parent': {
                                'entry': 'enable_acestream',
                                'value': ['1']
                                },
                            'InfoText': 3413,
                            },
                        'ace_life_buffer': {
                            'order': 4,
                            'name': 34014,
                            'value': None,
                            'action': 'initialize_acestream',
                            'type': 'num',
                            'parent': {
                                'entry': 'enable_acestream',
                                'value': ['1']
                                },
                            'InfoText': 3414,
                            },
                        'ace_cache_type': {
                            'order': 5,
                            'name': 34015,
                            'value': 'memory',
                            'values': ['disk', 'memory'],
                            'action': 'initialize_acestream',
                            'type': 'multivalue',
                            'parent': {
                                'entry': 'enable_acestream',
                                'value': ['1']
                                },
                            'InfoText': 3415,
                            },
                        'ace_cache_limit': {
                            'order': 6,
                            'name': 34016,
                            'value': None,
                            'action': 'initialize_acestream',
                            'type': 'num',
                            'parent': {
                                'entry': 'enable_acestream',
                                'value': ['1']
                                },
                            'InfoText': 3416,
                            },
                        'ace_life_cache_size': {
                            'order': 7,
                            'name': 34017,
                            'value': None,
                            'action': 'initialize_acestream',
                            'type': 'num',
                            'parent': {
                                'entry': 'enable_acestream',
                                'value': ['1']
                                },
                            'InfoText': 3417,
                            },
                        'ace_cache_dir': {
                            'order': 8,
                            'name': 34018,
                            'value': None,
                            'action': 'initialize_acestream',
                            'type': 'folder',
                            'parent': {
                                'entry': 'enable_acestream',
                                'value': ['1']
                                },
                            'InfoText': 3418,
                            },
                        'ace_clean_cache': {
                            'order': 9,
                            'name': 34019,
                            'value': None,
                            'action': 'initialize_acestream',
                            'type': 'bool',
                            'parent': {
                                'entry': 'enable_acestream',
                                'value': ['1']
                                },
                            'InfoText': 3419,
                            },
                        'ace_debug': {
                            'order': 10,
                            'name': 34020,
                            'value': None,
                            'action': 'initialize_acestream',
                            'type': 'bool',
                            'parent': {
                                'entry': 'enable_acestream',
                                'value': ['1']
                                },
                            'InfoText': 3420,
                            },
                        'ace_always': {
                            'order': 11,
                            'name': 34021,
                            'value': None,
                            'action': 'initialize_acestream',
                            'type': 'bool',
                            'parent': {
                                'entry': 'enable_acestream',
                                'value': ['1']
                                },
                            'InfoText': 3421,
                            },
                        },
                    },
                'aceproxy': {
                    'order': 2,
                    'name': 34030,
                    'not_supported': [],
                    'settings': {
                        'enable_aceproxy': {
                            'order': 1,
                            'name': 34031,
                            'value': None,
                            'action': 'initialize_aceproxy',
                            'type': 'bool',
                            'InfoText': 3431,
                            },
                        'aceproxy_login': {
                            'order': 2,
                            'name': 34032,
                            'value': None,
                            'action': 'initialize_aceproxy',
                            'type': 'text',
                            'parent': {
                                'entry': 'enable_aceproxy',
                                'value': ['1']
                                },
                            'InfoText': 3432,
                            },
                        'aceproxy_passw': {
                            'order': 3,
                            'name': 34033,
                            'value': None,
                            'action': 'initialize_aceproxy',
                            'type': 'text',
                            'parent': {
                                'entry': 'enable_aceproxy',
                                'value': ['1']
                                },
                            'InfoText': 3433,
                            },
                        'aceproxy_debug': {
                            'order': 4,
                            'name': 34034,
                            'value': 'INFO',
                            'values': ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                            'action': 'initialize_aceproxy',
                            'type': 'multivalue',
                            'parent': {
                                'entry': 'enable_aceproxy',
                                'value': ['1']
                                },
                            'InfoText': 3434,
                            },
                        'aceproxy_always': {
                            'order': 5,
                            'name': 34021,
                            'value': None,
                            'action': 'initialize_aceproxy',
                            'type': 'bool',
                            'parent': {
                                'entry': 'enable_aceproxy',
                                'value': ['1']
                                },
                            'InfoText': 3421,
                            },
                        },
                    },
            }

            self.oe = oeMain
            oeMain.dbg_log('ace::__init__', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('ace::__init__', 'ERROR: (%s)' % repr(e))

    def start_service(self):
        try:
            self.oe.dbg_log('ace::start_service', 'enter_function', 0)
            self.load_values()
            self.initialize_acestream(service=1)
            self.initialize_aceproxy(service=1)
            self.oe.dbg_log('ace::start_service', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('ace::start_service', 'ERROR: (%s)' % repr(e))

    def stop_service(self):
        try:
            self.oe.dbg_log('ace::stop_service', 'enter_function', 0)
            self.oe.dbg_log('ace::stop_service', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('ace::stop_service', 'ERROR: (' + repr(e) + ')')

    def do_init(self):
        try:
            self.oe.dbg_log('ace::do_init', 'exit_function', 0)
            self.load_values()
            self.oe.dbg_log('ace::do_init', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('ace::do_init', 'ERROR: (%s)' % repr(e))

    def set_value(self, listItem):
        try:
            self.oe.dbg_log('ace::set_value', 'enter_function', 0)
            self.struct[listItem.getProperty('category')]['settings'][listItem.getProperty('entry')]['value'] = listItem.getProperty('value')
            self.oe.dbg_log('ace::set_value', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('ace::set_value', 'ERROR: (' + repr(e) + ')')

    def load_menu(self, focusItem):
        try:
            self.oe.dbg_log('ace::load_menu', 'enter_function', 0)
            self.oe.winOeMain.build_menu(self.struct)
            self.oe.dbg_log('ace::load_menu', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('ace::load_menu', 'ERROR: (%s)' % repr(e))

    def load_values(self):
        try:
            self.oe.dbg_log('ace::load_values', 'enter_function', 0)

            #ACESTREAM
            if 'hidden' in self.struct['acestream']:
                del self.struct['acestream']['hidden']

            self.struct['acestream']['settings']['enable_acestream']['value'] = \
                    self.oe.get_service_state('acestream')

            self.struct['acestream']['settings']['ace_login']['value'] = \
            self.oe.get_service_option('acestream', 'ACE_LOGIN', self.D_ACE_LOGIN).replace('"', '')

            self.struct['acestream']['settings']['ace_passw']['value'] = \
            self.oe.get_service_option('acestream', 'ACE_PASSW', self.D_ACE_PASSW).replace('"', '')

            self.struct['acestream']['settings']['ace_life_buffer']['value'] = \
            self.oe.get_service_option('acestream', 'ACE_LIFE_BUFFER', self.D_ACE_LIFE_BUFFER).replace('"', '')

            self.struct['acestream']['settings']['ace_cache_type']['value'] = \
            self.oe.get_service_option('acestream', 'ACE_CACHE_TYPE', self.D_ACE_CACHE_TYPE).replace('"', '')

            self.struct['acestream']['settings']['ace_cache_limit']['value'] = \
            self.oe.get_service_option('acestream', 'ACE_CACHE_LIMIT', self.D_ACE_CACHE_LIMIT).replace('"', '')

            self.struct['acestream']['settings']['ace_life_cache_size']['value'] = \
            self.oe.get_service_option('acestream', 'ACE_LIFE_CACHE_SIZE', self.D_ACE_LIFE_CACHE_SIZE).replace('"', '')

            self.struct['acestream']['settings']['ace_cache_dir']['value'] = \
            self.oe.get_service_option('acestream', 'ACE_CACHE_DIR', self.D_ACE_CACHE_DIR).replace('"', '')

            self.struct['acestream']['settings']['ace_clean_cache']['value'] = \
            self.oe.get_service_option('acestream', 'ACE_CLEAN_CACHE', self.D_ACE_CLEAN_CACHE).replace('"', '')

            self.struct['acestream']['settings']['ace_debug']['value'] = \
            self.oe.get_service_option('acestream', 'ACE_DEBUG', self.D_ACE_DEBUG).replace('"', '')

            self.struct['acestream']['settings']['ace_always']['value'] = \
            self.oe.get_service_option('acestream', 'ACE_ALWAYS', self.D_ACE_ALWAYS).replace('"', '')

            # ACEPROXY
            if 'hidden' in self.struct['aceproxy']:
                del self.struct['aceproxy']['hidden']

            self.struct['aceproxy']['settings']['enable_aceproxy']['value'] = \
                    self.oe.get_service_state('aceproxy')

            self.struct['aceproxy']['settings']['aceproxy_login']['value'] = \
            self.oe.get_service_option('aceproxy', 'ACEPROXY_LOGIN', self.D_ACEPROXY_LOGIN).replace('"', '')

            self.struct['aceproxy']['settings']['aceproxy_passw']['value'] = \
            self.oe.get_service_option('aceproxy', 'ACEPROXY_PASSW', self.D_ACEPROXY_PASSW).replace('"', '')

            self.struct['aceproxy']['settings']['aceproxy_debug']['value'] = \
            self.oe.get_service_option('aceproxy', 'ACEPROXY_DEBUG', self.D_ACEPROXY_DEBUG).replace('"', '')

            self.struct['aceproxy']['settings']['aceproxy_always']['value'] = \
            self.oe.get_service_option('aceproxy', 'ACEPROXY_ALWAYS', self.D_ACEPROXY_ALWAYS).replace('"', '')

            self.oe.dbg_log('ace::load_values', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('ace::load_values', 'ERROR: (%s)' % repr(e))

    def initialize_acestream(self, **kwargs):
        try:
            self.oe.dbg_log('ace::initialize_acestream', 'enter_function', 0)
            self.oe.set_busy(1)
            if 'listItem' in kwargs:
                self.set_value(kwargs['listItem'])
            options = {}
            state = 1
            if self.struct['acestream']['settings']['enable_acestream']['value'] == '1':
                options['ACE_LOGIN'] = '"%s"' % self.struct['acestream']['settings']['ace_login']['value']
                options['ACE_PASSW'] = '"%s"' % self.struct['acestream']['settings']['ace_passw']['value']
                options['ACE_LIFE_BUFFER'] = '"%s"' % self.struct['acestream']['settings']['ace_life_buffer']['value']
                options['ACE_CACHE_TYPE'] = '"%s"' % self.struct['acestream']['settings']['ace_cache_type']['value']
                options['ACE_CACHE_LIMIT'] = '"%s"' % self.struct['acestream']['settings']['ace_cache_limit']['value']
                options['ACE_LIFE_CACHE_SIZE'] = '"%s"' % self.struct['acestream']['settings']['ace_life_cache_size']['value']
                options['ACE_CACHE_DIR'] = '"%s"' % self.struct['acestream']['settings']['ace_cache_dir']['value']
                options['ACE_CLEAN_CACHE'] = '"%s"' % self.struct['acestream']['settings']['ace_clean_cache']['value']
                options['ACE_DEBUG']    = '"%s"' % self.struct['acestream']['settings']['ace_debug']['value']
                options['ACE_ALWAYS']    = '"%s"' % self.struct['acestream']['settings']['ace_always']['value']
            else:
                state = 0
            self.oe.set_service('acestream', options, state)   
            self.oe.set_busy(0)
            self.oe.dbg_log('ace::initialize_acestream', 'exit_function', 0)
        except Exception, e:
            self.oe.set_busy(0)
            self.oe.dbg_log('ace::initialize_acestream', 'ERROR: (%s)' % repr(e), 4)

    def initialize_aceproxy(self, **kwargs):
        try:
            self.oe.dbg_log('ace::initialize_aceproxy', 'enter_function', 0)
            self.oe.set_busy(1)
            if 'listItem' in kwargs:
                self.set_value(kwargs['listItem'])
            options = {}
            state = 1
            if self.struct['aceproxy']['settings']['enable_aceproxy']['value'] == '1':
                options['ACEPROXY_LOGIN'] = '"%s"' % self.struct['aceproxy']['settings']['aceproxy_login']['value']
                options['ACEPROXY_PASSW'] = '"%s"' % self.struct['aceproxy']['settings']['aceproxy_passw']['value']
                options['ACEPROXY_DEBUG'] = '"%s"' % self.struct['aceproxy']['settings']['aceproxy_debug']['value']
                options['ACEPROXY_ALWAYS'] = '"%s"' % self.struct['aceproxy']['settings']['aceproxy_always']['value']
            else:
                state = 0
            self.oe.set_service('aceproxy', options, state)   
            self.oe.set_busy(0)
            self.oe.dbg_log('ace::initialize_aceproxy', 'exit_function', 0)
        except Exception, e:
            self.oe.set_busy(0)
            self.oe.dbg_log('ace::initialize_aceproxy', 'ERROR: (%s)' % repr(e), 4)

    def exit(self):
        try:
            self.oe.dbg_log('ace::exit', 'enter_function', 0)
            self.oe.dbg_log('ace::exit', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('ace::exit', 'ERROR: (%s)' % repr(e), 4)
