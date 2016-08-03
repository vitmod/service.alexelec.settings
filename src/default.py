################################################################################
#      This file is part of Alex@ELEC - http://www.alexelec.in.ua
#      Copyright (C) 2011-2016 Alexandr Zuyev (alex@alexelec.in.ua)
################################################################################
# -*- coding: utf-8 -*-

import xbmc
import socket
import xbmcaddon

__scriptid__ = 'service.alexelec.settings'
__addon__ = xbmcaddon.Addon(id=__scriptid__)
__cwd__ = __addon__.getAddonInfo('path')
__media__ = '%s/resources/skins/Default/media/' % __cwd__
_ = __addon__.getLocalizedString

try:
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect('/var/run/service.alexelec.settings.sock')
    sock.send('openConfigurationWindow')
    sock.close()
except Exception, e:
    xbmc.executebuiltin('Notification("AlexELEC", "%s", 5000, "%sicon.png")' % (_(32390).encode('utf-8'), __media__))
