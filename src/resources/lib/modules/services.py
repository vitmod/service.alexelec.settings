################################################################################
#      This file is part of Alex@ELEC - http://www.alexelec.in.ua
#      Copyright (C) 2011-2016 Alexandr Zuyev (alex@alexelec.in.ua)
################################################################################
# -*- coding: utf-8 -*-

import os
import glob

class services:

    ENABLED = False
    SAMBA_NMDB = None
    SAMBA_SMDB = None
    D_SAMBA_SECURE = None
    D_SAMBA_USERNAME = None
    D_SAMBA_PASSWORD = None
    D_SAMBA_AUTOSHARE = None
    KERNEL_CMD = None
    SSH_DAEMON = None
    D_SSH_DISABLE_PW_AUTH = None
    OPT_SSH_NOPASSWD = None
    AVAHI_DAEMON = None
    CRON_DAEMON = None
    LCD_DRIVER_DIR = None
    D_LCD_DRIVER = None
    D_RAMCLEAR_TIME = None
    D_VNC_DEBUG = None
    D_VNC_PORT = None
    D_VNC_PASSWORD = None

    menu = {'4': {
        'name': 32001,
        'menuLoader': 'load_menu',
        'listTyp': 'list',
        'InfoText': 703,
        }}

    def __init__(self, oeMain):
        try:
            oeMain.dbg_log('services::__init__', 'enter_function', 0)
            self.struct = {
                'samba': {
                    'order': 1,
                    'name': 32200,
                    'not_supported': [],
                    'settings': {
                        'samba_autostart': {
                            'order': 1,
                            'name': 32204,
                            'value': None,
                            'action': 'initialize_samba',
                            'type': 'bool',
                            'InfoText': 738,
                            },
                        'samba_secure': {
                            'order': 2,
                            'name': 32202,
                            'value': None,
                            'action': 'initialize_samba',
                            'type': 'bool',
                            'parent': {
                                'entry': 'samba_autostart',
                                'value': ['1'],
                                },
                            'InfoText': 739,
                            },
                        'samba_username': {
                            'order': 3,
                            'name': 32106,
                            'value': None,
                            'action': 'initialize_samba',
                            'type': 'text',
                            'parent': {
                                'entry': 'samba_secure',
                                'value': ['1'],
                                },
                            'InfoText': 740,
                            },
                        'samba_password': {
                            'order': 4,
                            'name': 32107,
                            'value': None,
                            'action': 'initialize_samba',
                            'type': 'text',
                            'parent': {
                                'entry': 'samba_secure',
                                'value': ['1'],
                                },
                            'InfoText': 741,
                            },
                        'samba_autoshare': {
                            'order': 5,
                            'name': 32216,
                            'value': None,
                            'action': 'initialize_samba',
                            'type': 'bool',
                            'parent': {
                                'entry': 'samba_autostart',
                                'value': ['1'],
                                },
                            'InfoText': 755,
                            },
                        },
                    },
                'ssh': {
                    'order': 2,
                    'name': 32201,
                    'not_supported': [],
                    'settings': {
                        'ssh_autostart': {
                            'order': 1,
                            'name': 32205,
                            'value': None,
                            'action': 'initialize_ssh',
                            'type': 'bool',
                            'InfoText': 742,
                            },
                        'ssh_secure': {
                            'order': 2,
                            'name': 32203,
                            'value': None,
                            'action': 'initialize_ssh',
                            'type': 'bool',
                            'parent': {
                                'entry': 'ssh_autostart',
                                'value': ['1'],
                                },
                            'InfoText': 743,
                            },
                        },
                    },
                'avahi': {
                    'order': 3,
                    'name': 32207,
                    'not_supported': [],
                    'settings': {'avahi_autostart': {
                        'order': 1,
                        'name': 32206,
                        'value': None,
                        'action': 'initialize_avahi',
                        'type': 'bool',
                        'InfoText': 744,
                        }},
                    },
                'cron': {
                    'order': 4,
                    'name': 32319,
                    'not_supported': [],
                    'settings': {'cron_autostart': {
                        'order': 1,
                        'name': 32320,
                        'value': None,
                        'action': 'initialize_cron',
                        'type': 'bool',
                        'InfoText': 745,
                        }},
                    },
                'driver': {
                    'order': 5,
                    'name': 32007,
                    'settings': {
                        'lcd_enabled': {
                            'name': 32391,
                            'value': 'none',
                            'action': 'set_lcd_driver',
                            'type': 'bool',
                            'InfoText': 717,
                            'order': 1,
                            },
                        'lcd': {
                            'name': 32008,
                            'value': 'none',
                            'action': 'set_lcd_driver',
                            'type': 'multivalue',
                            'parent': {
                                'entry': 'lcd_enabled',
                                'value': ['1'],
                                },
                            'values': [],
                            'InfoText': 717,
                            'order': 2,
                            },
                        },
                    },
                'bluez': {
                    'order': 6,
                    'name': 32331,
                    'not_supported': [],
                    'settings': {
                        'enabled': {
                            'order': 1,
                            'name': 32344,
                            'value': None,
                            'action': 'init_bluetooth',
                            'type': 'bool',
                            'InfoText': 720,
                            },
                        'obex_enabled': {
                            'order': 2,
                            'name': 32384,
                            'value': None,
                            'action': 'init_obex',
                            'type': 'bool',
                            'parent': {
                                'entry': 'enabled',
                                'value': ['1'],
                                },
                            'InfoText': 751,
                            },
                        'obex_root': {
                            'order': 3,
                            'name': 32385,
                            'value': None,
                            'action': 'init_obex',
                            'type': 'folder',
                            'parent': {
                                'entry': 'obex_enabled',
                                'value': ['1'],
                                },
                            'InfoText': 752,
                            },
                        },
                    },
                'mysql': {
                    'order': 7,
                    'name': 32401,
                    'not_supported': [],
                    'settings': {
                        'mysql_autostart': {
                            'order': 1,
                            'name': 32411,
                            'value': None,
                            'action': 'initialize_mysql',
                            'type': 'bool',
                            'InfoText': 811,
                            },
                        },
                    },
                'minidlna': {
                    'order': 8,
                    'name': 32402,
                    'not_supported': [],
                    'settings': {
                        'minidlna_autostart': {
                            'order': 1,
                            'name': 32412,
                            'value': None,
                            'action': 'initialize_minidlna',
                            'type': 'bool',
                            'InfoText': 812,
                            },
                        },
                    },
                'ramclear': {
                    'order': 9,
                    'name': 32403,
                    'not_supported': [],
                    'settings': {
                        'ramclear_autostart': {
                            'order': 1,
                            'name': 32413,
                            'value': None,
                            'action': 'initialize_ramclear',
                            'type': 'bool',
                            'InfoText': 813,
                            },
                        'ramclear_time': {
                            'order': 2,
                            'name': 32414,
                            'value': '5',
                            'action': 'initialize_ramclear',
                            'type': 'num',
                            'parent': {
                                'entry': 'ramclear_autostart',
                                'value': ['1']
                                },
                            'InfoText': 814,
                            },
                        }
                    },
                'x11vnc': {
                    'order': 10,
                    'name': 32420,
                    'not_supported': [],
                    'settings': {
                        'vnc_autostart': {
                            'order': 1,
                            'name': 32421,
                            'value': None,
                            'action': 'initialize_vnc',
                            'type': 'bool',
                            'InfoText': 821,
                            },
                        'vnc_port': {
                            'order': 2,
                            'name': 32422,
                            'value': None,
                            'action': 'initialize_vnc',
                            'type': 'num',
                            'parent': {
                                'entry': 'vnc_autostart',
                                'value': ['1'],
                                },
                            'InfoText': 822,
                            },
                        'vnc_password': {
                            'order': 3,
                            'name': 32423,
                            'value': None,
                            'action': 'initialize_vnc',
                            'type': 'text',
                            'parent': {
                                'entry': 'vnc_autostart',
                                'value': ['1'],
                                },
                            'InfoText': 823,
                            },
                        'vnc_debug': {
                            'order': 4,
                            'name': 32424,
                            'value': None,
                            'action': 'initialize_vnc',
                            'type': 'bool',
                            'parent': {
                                'entry': 'vnc_autostart',
                                'value': ['1'],
                                },
                            'InfoText': 824,
                            },
                        },
                    },
                }

            self.oe = oeMain
            oeMain.dbg_log('services::__init__', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('services::__init__', 'ERROR: (%s)' % repr(e))

    def start_service(self):
        try:
            self.oe.dbg_log('services::start_service', 'enter_function', 0)
            self.load_values()
            self.initialize_samba(service=1)
            self.initialize_ssh(service=1)
            self.initialize_avahi(service=1)
            self.initialize_cron(service=1)
            self.init_bluetooth(service=1)
            self.initialize_mysql(service=1)
            self.initialize_minidlna(service=1)
            self.initialize_ramclear(service=1)
            self.initialize_vnc(service=1)
            self.oe.dbg_log('services::start_service', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('services::start_service', 'ERROR: (%s)' % repr(e))

    def stop_service(self):
        try:
            self.oe.dbg_log('service::stop_service', 'enter_function', 0)
            self.oe.dbg_log('service::stop_service', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('service::stop_service', 'ERROR: (' + repr(e) + ')')

    def do_init(self):
        try:
            self.oe.dbg_log('services::do_init', 'exit_function', 0)
            self.load_values()
            self.oe.dbg_log('services::do_init', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('services::do_init', 'ERROR: (%s)' % repr(e))

    def set_value(self, listItem):
        try:
            self.oe.dbg_log('services::set_value', 'enter_function', 0)
            self.struct[listItem.getProperty('category')]['settings'][listItem.getProperty('entry')]['value'] = listItem.getProperty('value')
            self.oe.dbg_log('system::set_value', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('system::set_value', 'ERROR: (' + repr(e) + ')')

    def load_menu(self, focusItem):
        try:
            self.oe.dbg_log('services::load_menu', 'enter_function', 0)
            self.oe.winOeMain.build_menu(self.struct)
            self.oe.dbg_log('services::load_menu', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('services::load_menu', 'ERROR: (%s)' % repr(e))

    def load_values(self):
        try:
            self.oe.dbg_log('services::load_values', 'enter_function', 0)

            # LCD

            arrLcd = self.get_lcd_drivers()
            self.struct['driver']['settings']['lcd']['values'] = arrLcd
            self.struct['driver']['settings']['lcd_enabled']['value'] = self.oe.get_service_state('lcdd')
            self.struct['driver']['settings']['lcd']['value'] = self.oe.get_service_option('lcdd', 'LCD_DRIVER', self.D_LCD_DRIVER).replace('"',
                    '')

            # SAMBA

            if os.path.isfile(self.SAMBA_NMDB) and os.path.isfile(self.SAMBA_SMDB):
                self.struct['samba']['settings']['samba_autostart']['value'] = self.oe.get_service_state('samba')
                self.struct['samba']['settings']['samba_secure']['value'] = self.oe.get_service_option('samba', 'SAMBA_SECURE',
                        self.D_SAMBA_SECURE).replace('true', '1').replace('false', '0').replace('"', '')
                self.struct['samba']['settings']['samba_username']['value'] = self.oe.get_service_option('samba', 'SAMBA_USERNAME',
                        self.D_SAMBA_USERNAME).replace('"', '')
                self.struct['samba']['settings']['samba_password']['value'] = self.oe.get_service_option('samba', 'SAMBA_PASSWORD',
                        self.D_SAMBA_PASSWORD).replace('"', '')
                self.struct['samba']['settings']['samba_autoshare']['value'] = self.oe.get_service_option('samba', 'SAMBA_AUTOSHARE',
                        self.D_SAMBA_AUTOSHARE).replace('true', '1').replace('false', '0').replace('"', '')
            else:
                self.struct['samba']['hidden'] = 'true'

            # SSH

            if os.path.isfile(self.SSH_DAEMON):
                self.struct['ssh']['settings']['ssh_autostart']['value'] = self.oe.get_service_state('sshd')
                self.struct['ssh']['settings']['ssh_secure']['value'] = self.oe.get_service_option('sshd', 'SSHD_DISABLE_PW_AUTH',
                        self.D_SSH_DISABLE_PW_AUTH).replace('true', '1').replace('false', '0').replace('"', '')

                # hide ssh settings if Kernel Parameter isset

                cmd_file = open(self.KERNEL_CMD, 'r')
                cmd_args = cmd_file.read()
                if 'ssh' in cmd_args:
                    self.struct['ssh']['settings']['ssh_autostart']['value'] = '1'
                    self.struct['ssh']['settings']['ssh_autostart']['hidden'] = 'true'
                cmd_file.close()
            else:
                self.struct['ssh']['hidden'] = 'true'

            # AVAHI

            if os.path.isfile(self.AVAHI_DAEMON):
                self.struct['avahi']['settings']['avahi_autostart']['value'] = self.oe.get_service_state('avahi')
            else:
                self.struct['avahi']['hidden'] = 'true'

            # CRON

            if os.path.isfile(self.CRON_DAEMON):
                self.struct['cron']['settings']['cron_autostart']['value'] = self.oe.get_service_state('crond')
            else:
                self.struct['cron']['hidden'] = 'true'

            # BLUEZ / OBEX

            if 'bluetooth' in self.oe.dictModules:
                if os.path.isfile(self.oe.dictModules['bluetooth'].BLUETOOTH_DAEMON):
                    self.struct['bluez']['settings']['enabled']['value'] = self.oe.get_service_state('bluez')
                    if os.path.isfile(self.oe.dictModules['bluetooth'].OBEX_DAEMON):
                        self.struct['bluez']['settings']['obex_enabled']['value'] = self.oe.get_service_state('obexd')
                        self.struct['bluez']['settings']['obex_root']['value'] = self.oe.get_service_option('obexd', 'OBEXD_ROOT',
                                self.oe.dictModules['bluetooth'].D_OBEXD_ROOT).replace('"', '')
                    else:
                        self.struct['bluez']['settings']['obex_enabled']['hidden'] = True
                        self.struct['bluez']['settings']['obex_root']['hidden'] = True
                else:
                    self.struct['bluez']['hidden'] = 'true'
            self.oe.dbg_log('services::load_values', 'exit_function', 0)

            # mySQL
            self.struct['mysql']['settings']['mysql_autostart']['value'] = self.oe.get_service_state('mysqld')

            # miniDLNA
            self.struct['minidlna']['settings']['minidlna_autostart']['value'] = self.oe.get_service_state('minidlna')

            # CLEAR RAM
            self.struct['ramclear']['settings']['ramclear_autostart']['value'] = self.oe.get_service_state('ramclear')
            self.struct['ramclear']['settings']['ramclear_time']['value'] = self.oe.get_service_option('ramclear', 'RAMCLEAR_TIME', self.D_RAMCLEAR_TIME).replace('"', '')

            # x11VNC
            self.struct['x11vnc']['settings']['vnc_autostart']['value'] = self.oe.get_service_state('x11vnc')
            self.struct['x11vnc']['settings']['vnc_port']['value'] = self.oe.get_service_option('x11vnc', 'VNC_PORT', self.D_VNC_PORT).replace('"', '')
            self.struct['x11vnc']['settings']['vnc_password']['value'] = self.oe.get_service_option('x11vnc', 'VNC_PASSWORD', self.D_VNC_PASSWORD).replace('"', '')
            self.struct['x11vnc']['settings']['vnc_debug']['value'] = self.oe.get_service_option('x11vnc', 'VNC_DEBUG', self.D_VNC_DEBUG).replace('"', '')

        except Exception, e:
            self.oe.dbg_log('services::load_values', 'ERROR: (%s)' % repr(e))

    def initialize_samba(self, **kwargs):
        try:
            self.oe.dbg_log('services::initialize_samba', 'enter_function', 0)
            self.oe.set_busy(1)
            if 'listItem' in kwargs:
                self.set_value(kwargs['listItem'])
            options = {}
            state = 1
            if self.struct['samba']['settings']['samba_autostart']['value'] == '1':
                if 'hidden' in self.struct['samba']['settings']['samba_username']:
                    del self.struct['samba']['settings']['samba_username']['hidden']
                if 'hidden' in self.struct['samba']['settings']['samba_password']:
                    del self.struct['samba']['settings']['samba_password']['hidden']
                if self.struct['samba']['settings']['samba_secure']['value'] == '1':
                    val_secure = 'true'
                else:
                    val_secure = 'false'
                if self.struct['samba']['settings']['samba_autoshare']['value'] == '1':
                    val_autoshare = 'true'
                else:
                    val_autoshare = 'false'
                options['SAMBA_SECURE'] = '"%s"' % val_secure
                options['SAMBA_AUTOSHARE'] = '"%s"' % val_autoshare
                options['SAMBA_USERNAME'] = '"%s"' % self.struct['samba']['settings']['samba_username']['value']
                options['SAMBA_PASSWORD'] = '"%s"' % self.struct['samba']['settings']['samba_password']['value']
            else:
                state = 0
                self.struct['samba']['settings']['samba_username']['hidden'] = True
                self.struct['samba']['settings']['samba_password']['hidden'] = True
            self.oe.set_service('samba', options, state)
            self.oe.set_busy(0)
            self.oe.dbg_log('services::initialize_samba', 'exit_function', 0)
        except Exception, e:
            self.oe.set_busy(0)
            self.oe.dbg_log('services::initialize_samba', 'ERROR: (%s)' % repr(e), 4)

    def initialize_ssh(self, **kwargs):
        try:
            self.oe.dbg_log('services::initialize_ssh', 'enter_function', 0)
            self.oe.set_busy(1)
            if 'listItem' in kwargs:
                self.set_value(kwargs['listItem'])
            state = 1
            options = {}
            if self.struct['ssh']['settings']['ssh_autostart']['value'] == '1':
                if self.struct['ssh']['settings']['ssh_secure']['value'] == '1':
                    val = 'true'
                    options['SSH_ARGS'] = '"%s"' % self.OPT_SSH_NOPASSWD
                else:
                    val = 'false'
                    options['SSH_ARGS'] = '""'
                options['SSHD_DISABLE_PW_AUTH'] = '"%s"' % val
            else:
                state = 0
            self.oe.set_service('sshd', options, state)
            self.oe.set_busy(0)
            self.oe.dbg_log('services::initialize_ssh', 'exit_function', 0)
        except Exception, e:
            self.oe.set_busy(0)
            self.oe.dbg_log('services::initialize_ssh', 'ERROR: (%s)' % repr(e), 4)

    def initialize_avahi(self, **kwargs):
        try:
            self.oe.dbg_log('services::initialize_avahi', 'enter_function', 0)
            self.oe.set_busy(1)
            if 'listItem' in kwargs:
                self.set_value(kwargs['listItem'])
            state = 1
            options = {}
            if self.struct['avahi']['settings']['avahi_autostart']['value'] != '1':
                state = 0
            self.oe.set_service('avahi', options, state)
            self.oe.set_busy(0)
            self.oe.dbg_log('services::initialize_avahi', 'exit_function', 0)
        except Exception, e:
            self.oe.set_busy(0)
            self.oe.dbg_log('services::initialize_avahi', 'ERROR: (%s)' % repr(e), 4)

    def initialize_cron(self, **kwargs):
        try:
            self.oe.dbg_log('services::initialize_cron', 'enter_function', 0)
            self.oe.set_busy(1)
            if 'listItem' in kwargs:
                self.set_value(kwargs['listItem'])
            state = 1
            options = {}
            if self.struct['cron']['settings']['cron_autostart']['value'] != '1':
                state = 0
            self.oe.set_service('crond', options, state)
            self.oe.set_busy(0)
            self.oe.dbg_log('services::initialize_cron', 'exit_function', 0)
        except Exception, e:
            self.oe.set_busy(0)
            self.oe.dbg_log('services::initialize_cron', 'ERROR: (%s)' % repr(e), 4)

    def init_bluetooth(self, **kwargs):
        try:
            self.oe.dbg_log('services::init_bluetooth', 'enter_function', 0)
            self.oe.set_busy(1)
            if 'listItem' in kwargs:
                self.set_value(kwargs['listItem'])
            state = 1
            options = {}
            if self.struct['bluez']['settings']['enabled']['value'] != '1':
                state = 0
                self.struct['bluez']['settings']['obex_enabled']['hidden'] = True
                self.struct['bluez']['settings']['obex_root']['hidden'] = True
            else:
                if 'hidden' in self.struct['bluez']['settings']['obex_enabled']:
                    del self.struct['bluez']['settings']['obex_enabled']['hidden']
                if 'hidden' in self.struct['bluez']['settings']['obex_root']:
                    del self.struct['bluez']['settings']['obex_root']['hidden']
            self.oe.set_service('bluez', options, state)
            self.oe.set_busy(0)
            self.oe.dbg_log('services::init_bluetooth', 'exit_function', 0)
        except Exception, e:
            self.oe.set_busy(0)
            self.oe.dbg_log('services::init_bluetooth', 'ERROR: (' + repr(e) + ')', 4)

    def init_obex(self, **kwargs):
        try:
            self.oe.dbg_log('services::init_obex', 'enter_function', 0)
            self.oe.set_busy(1)
            if 'listItem' in kwargs:
                self.set_value(kwargs['listItem'])
            state = 1
            options = {}
            if self.struct['bluez']['settings']['obex_enabled']['value'] == '1':
                options['OBEXD_ROOT'] = '"%s"' % self.struct['bluez']['settings']['obex_root']['value']
            else:
                state = 0
            self.oe.set_service('obexd', options, state)
            self.oe.set_busy(0)
            self.oe.dbg_log('services::init_obex', 'exit_function', 0)
        except Exception, e:
            self.oe.set_busy(0)
            self.oe.dbg_log('services::init_obex', 'ERROR: (' + repr(e) + ')', 4)

    def initialize_mysql(self, **kwargs):
        try:
            self.oe.dbg_log('services::initialize_mysql', 'enter_function', 0)
            self.oe.set_busy(1)
            if 'listItem' in kwargs:
                self.set_value(kwargs['listItem'])
            state = 1
            options = {}
            if self.struct['mysql']['settings']['mysql_autostart']['value'] != '1':
                state = 0
            self.oe.set_service('mysqld', options, state)   
            self.oe.set_busy(0)
            self.oe.dbg_log('services::initialize_mysql', 'exit_function', 0)
        except Exception, e:
            self.oe.set_busy(0)
            self.oe.dbg_log('services::initialize_mysql', 'ERROR: (' + repr(e) + ')', 4)

    def initialize_minidlna(self, **kwargs):
        try:
            self.oe.dbg_log('services::initialize_minidlna', 'enter_function', 0)
            self.oe.set_busy(1)
            if 'listItem' in kwargs:
                self.set_value(kwargs['listItem'])
            state = 1
            options = {}
            if self.struct['minidlna']['settings']['minidlna_autostart']['value'] != '1':
                state = 0
            self.oe.set_service('minidlna', options, state)   
            self.oe.set_busy(0)
            self.oe.dbg_log('services::initialize_minidlna', 'exit_function', 0)
        except Exception, e:
            self.oe.set_busy(0)
            self.oe.dbg_log('services::initialize_minidlna', 'ERROR: (' + repr(e) + ')', 4)

    def initialize_ramclear(self, **kwargs):
        try:
            self.oe.dbg_log('services::initialize_ramclear', 'enter_function', 0)
            self.oe.set_busy(1)
            if 'listItem' in kwargs:
                self.set_value(kwargs['listItem'])
            state = 0
            options = {}
            if self.struct['ramclear']['settings']['ramclear_autostart']['value'] == '1':
                state = 1
                options['RAMCLEAR_TIME']  = '"%s"' % self.struct['ramclear']['settings']['ramclear_time']['value']
            self.oe.set_service('ramclear', options, state)   
            self.oe.set_busy(0)
            self.oe.dbg_log('services::initialize_ramclear', 'exit_function', 0)
        except Exception, e:
            self.oe.set_busy(0)
            self.oe.dbg_log('services::initialize_ramclear', 'ERROR: (' + repr(e) + ')', 4)

    def initialize_vnc(self, **kwargs):
        try:
            self.oe.dbg_log('services::initialize_vnc', 'enter_function', 0)
            self.oe.set_busy(1)
            if 'listItem' in kwargs:
                self.set_value(kwargs['listItem'])
            state = 0
            options = {}
            if self.struct['x11vnc']['settings']['vnc_autostart']['value'] == '1':
                state = 1
                options['VNC_PORT']     = '"%s"' % self.struct['x11vnc']['settings']['vnc_port']['value']
                options['VNC_PASSWORD'] = '"%s"' % self.struct['x11vnc']['settings']['vnc_password']['value']
                options['VNC_DEBUG']    = '"%s"' % self.struct['x11vnc']['settings']['vnc_debug']['value']
            self.oe.set_service('x11vnc', options, state)   
            self.oe.set_busy(0)
            self.oe.dbg_log('services::initialize_vnc', 'exit_function', 0)
        except Exception, e:
            self.oe.set_busy(0)
            self.oe.dbg_log('services::initialize_vnc', 'ERROR: (' + repr(e) + ')', 4)

    def set_lcd_driver(self, listItem=None):
        try:
            self.oe.dbg_log('services::set_lcd_driver', 'enter_function', 0)
            self.oe.set_busy(1)
            state = 0
            options = {}
            if not listItem == None:
                self.set_value(listItem)
            if self.struct['driver']['settings']['lcd_enabled']['value'] == '1':
                state = 1
            if not self.struct['driver']['settings']['lcd']['value'] is None and not self.struct['driver']['settings']['lcd']['value'] == 'none' \
                and state == 1:
                options['LCD_DRIVER'] = '"%s"' % self.struct['driver']['settings']['lcd']['value']
            self.oe.dbg_log('services::set_lcd_driver', repr(options), 0)
            self.oe.dbg_log('services::set_lcd_driver', repr(state), 0)
            self.oe.set_service('lcdd', options, state)
            self.oe.set_busy(0)
            self.oe.dbg_log('services::set_lcd_driver', 'exit_function', 0)
        except Exception, e:
            self.oe.set_busy(0)
            self.oe.dbg_log('services::set_lcd_driver', 'ERROR: (' + repr(e) + ')')

    def get_lcd_drivers(self):
        try:
            self.oe.dbg_log('services::get_lcd_drivers', 'enter_function', 0)
            arrDrivers = ['none']
            if os.path.exists(self.LCD_DRIVER_DIR):
                for driver in glob.glob(self.LCD_DRIVER_DIR + '*'):
                    arrDrivers.append(os.path.basename(driver).replace('.so', ''))
            self.oe.dbg_log('services::get_lcd_drivers', 'exit_function', 0)
            return arrDrivers
        except Exception, e:
            self.oe.dbg_log('services::get_lcd_drivers', 'ERROR: (' + repr(e) + ')')

    def exit(self):
        try:
            self.oe.dbg_log('services::exit', 'enter_function', 0)
            self.oe.dbg_log('services::exit', 'exit_function', 0)
        except Exception, e:
            self.oe.dbg_log('services::exit', 'ERROR: (%s)' % repr(e), 4)
