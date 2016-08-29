################################################################################
#      This file is part of Alex@ELEC - http://www.alexelec.in.ua
#      Copyright (C) 2011-2016 Alexandr Zuyev (alex@alexelec.in.ua)
################################################################################
# -*- coding: utf-8 -*-

import os
import glob
import oeWindows

class transmission:

    ENABLED = False
    TRANSMISSION_DAEMON = None
    D_TRANSMISSION_LOG = None
    D_TRANSMISSION_AUTH = None
    D_TRANSMISSION_USER = None
    D_TRANSMISSION_PWD = None
    D_TRANSMISSION_IP = None
    D_TRANSMISSION_DL_DIR = None

    menu = {'98': {
        'name': 46000,
        'menuLoader': 'load_menu',
        'listTyp': 'list',
        'InfoText': 4600,
        }}

    def __init__(self, oeMain):
        try:
            oeMain.dbg_log('transmission::__init__', 'enter_function', 0)
            self.struct = {
                'transmission': {
                    'order': 1,
                    'name': 46010,
                    'not_supported': [],
                    'settings': {
                        'transmission_autostart': {
                            'order': 1,
                            'name': 46011,
                            'value': '0',
                            'action': 'initialize_transmission',
                            'type': 'bool',
                            'InfoText': 4611,
                        },
                        'transmission_auth': {
                            'order': 2,
                            'name': 46012,
                            'value': '0',
                            'action': 'initialize_transmission',
                            'type': 'bool',
                            'parent': {'entry': 'transmission_autostart','value': ['1']},
                            'InfoText': 4612,
                        },
                        'transmission_user': {
                            'order': 3,
                            'name': 46013,
                            'value': 'alexelec',
                            'action': 'initialize_transmission',
                            'type': 'text',
                            'parent': {'entry': 'transmission_auth','value': ['1']},
                            'InfoText': 4613,
                        },
                        'transmission_pwd': {
                            'order': 4,
                            'name': 46014,
                            'value': 'alexelec',
                            'action': 'initialize_transmission',
                            'type': 'text',
                            'parent': {'entry': 'transmission_auth','value': ['1']},
                            'InfoText': 4614,
                        },
                        'transmission_ip': {
                            'order': 5,
                            'name': 46015,
                            'value': '*.*.*.*',
                            'action': 'initialize_transmission',
                            'type': 'text',
                            'parent': {'entry': 'transmission_autostart','value': ['1']},
                            'InfoText': 4615,
                        },
                        'transmission_dl_dir': {
                            'order': 6,
                            'name': 46016,
                            'value': '/storage/downloads/',
                            'action': 'initialize_transmission',
                            'type': 'folder',
                            'parent': {'entry': 'transmission_autostart','value': ['1']},
                            'InfoText': 4616,
                        },
                        'transmission_log': {
                            'order': 7,
                            'name': 46017,
                            'value': 'Error',
                            'values': ['Error','Info','Debug'],
                            'action': 'initialize_transmission',
                            'type': 'multivalue',
                            'parent': {'entry': 'transmission_autostart','value': ['1']},
                            'InfoText': 4617,
                        },
                    },
                },
            }

            self.oe = oeMain
            oeMain.dbg_log('transmission::__init__', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('transmission::__init__', 'ERROR: (%s)' % repr(e))

    def start_service(self):
        try:
            self.oe.dbg_log('transmission::start_service', 'enter_function', 0)
            self.load_values()
            self.initialize_transmission(service=1)
            self.oe.dbg_log('transmission::start_service', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('transmission::start_service', 'ERROR: (%s)' % repr(e))

    def stop_service(self):
        try:
            self.oe.dbg_log('transmission::stop_service', 'enter_function', 0)
            self.oe.dbg_log('transmission::stop_service', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('transmission::stop_service', 'ERROR: (' + repr(e) + ')')

    def do_init(self):
        try:
            self.oe.dbg_log('transmission::do_init', 'exit_function', 0)
            self.load_values()
            self.oe.dbg_log('transmission::do_init', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('transmission::do_init', 'ERROR: (%s)' % repr(e))

    def set_value(self, listItem):
        try:
            self.oe.dbg_log('transmission::set_value', 'enter_function', 0)
            self.struct[listItem.getProperty('category')]['settings'
                    ][listItem.getProperty('entry')]['value'] = \
                listItem.getProperty('value')
            self.oe.dbg_log('transmission::set_value', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('transmission::set_value', 'ERROR: (' + repr(e) + ')')

    def load_menu(self, focusItem):
        try:
            self.oe.dbg_log('transmission::load_menu', 'enter_function', 0)
            self.oe.winOeMain.build_menu(self.struct)
            self.oe.dbg_log('transmission::load_menu', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('transmission::load_menu', 'ERROR: (%s)' % repr(e))

    def load_values(self):
        try:
            self.oe.dbg_log('transmission::load_values', 'enter_function', 0)
            if os.path.isfile(self.TRANSMISSION_DAEMON):
                if 'hidden' in self.struct['transmission']:
                    del self.struct['transmission']['hidden']

                self.struct['transmission']['settings']['transmission_autostart']['value'] = \
                    self.oe.get_service_state('transmission')

                self.struct['transmission']['settings']['transmission_auth']['value'] = \
                self.oe.get_service_option('transmission', 'TRANSMISSION_AUTH', self.D_TRANSMISSION_AUTH).replace('"', '')

                self.struct['transmission']['settings']['transmission_user']['value'] = \
                self.oe.get_service_option('transmission', 'TRANSMISSION_USER', self.D_TRANSMISSION_USER).replace('"', '')

                self.struct['transmission']['settings']['transmission_pwd']['value'] = \
                self.oe.get_service_option('transmission', 'TRANSMISSION_PWD', self.D_TRANSMISSION_PWD).replace('"', '')

                self.struct['transmission']['settings']['transmission_ip']['value'] = \
                self.oe.get_service_option('transmission', 'TRANSMISSION_IP', self.D_TRANSMISSION_IP).replace('"', '')

                self.struct['transmission']['settings']['transmission_dl_dir']['value'] = \
                self.oe.get_service_option('transmission', 'TRANSMISSION_DL_DIR', self.D_TRANSMISSION_DL_DIR).replace('"', '')

                self.struct['transmission']['settings']['transmission_log']['value'] = \
                self.oe.get_service_option('transmission', 'TRANSMISSION_LOG', self.D_TRANSMISSION_LOG).replace('"', '')
            else:
                self.struct['transmission']['hidden'] = 'true'

            self.oe.dbg_log('transmission::load_values', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('transmission::load_values', 'ERROR: (%s)' % repr(e))

    def initialize_transmission(self, **kwargs):
        try:
            self.oe.dbg_log('transmission::initialize_transmission', 'enter_function', 0)
            self.oe.set_busy(1)
            if 'listItem' in kwargs:
                self.set_value(kwargs['listItem'])
            options = {}

            if self.struct['transmission']['settings']['transmission_autostart']['value'] == '1':
                state = 1
                if 'hidden' in self.struct['transmission']['settings']['transmission_user']:
                    del self.struct['transmission']['settings']['transmission_user']['hidden']
                if 'hidden' in self.struct['transmission']['settings']['transmission_pwd']:
                    del self.struct['transmission']['settings']['transmission_pwd']['hidden']
                options['TRANSMISSION_AUTH'] = '"%s"' % self.struct['transmission']['settings']['transmission_auth']['value']
                options['TRANSMISSION_USER'] = '"%s"' % self.struct['transmission']['settings']['transmission_user']['value']
                options['TRANSMISSION_PWD'] = '"%s"' % self.struct['transmission']['settings']['transmission_pwd']['value']
                options['TRANSMISSION_IP'] = '"%s"' % self.struct['transmission']['settings']['transmission_ip']['value']
                options['TRANSMISSION_DL_DIR'] = '"%s"' % self.struct['transmission']['settings']['transmission_dl_dir']['value']
                options['TRANSMISSION_LOG'] = '"%s"' % self.struct['transmission']['settings']['transmission_log']['value']

            else:
                state = 0
                self.struct['transmission']['settings']['transmission_user']['hidden'] = True
                self.struct['transmission']['settings']['transmission_pwd']['hidden'] = True

            self.oe.set_service('transmission', options, state)
            self.oe.set_busy(0)
            self.oe.dbg_log('transmission::initialize_transmission', 'exit_function', 0)
        except Exception, e:
            self.oe.set_busy(0)
            self.oe.dbg_log('transmission::initialize_transmission', 'ERROR: (%s)' % repr(e), 4)

    def exit(self):
        try:
            self.oe.dbg_log('transmission::exit', 'enter_function', 0)
            self.oe.dbg_log('transmission::exit', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('transmission::exit', 'ERROR: (%s)' % repr(e), 4)
