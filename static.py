#!/usr/bin/env python
# -*- coding: utf8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# Maintainer: Fadiga

import os

from Common.cstatic import CConstants

ROOT_DIR = os.path.dirname(os.path.abspath('__file__'))


class Constants(CConstants):

    def __init__(self):
        CConstants.__init__(self)

    ORG_AUT = u"Copyright fadsoft © 2014"
    credit = 17
    tolerance = 50
    nb_warning = 5

    # ------------------------- Application --------------------------#

    NAME_MAIN = "wari_main.py"
    APP_NAME = "Transfert d'argent"
    APP_VERSION = u"0.3"
    APP_DATE = u"04/2014"
    img_media = os.path.join(os.path.join(ROOT_DIR, "static"), "images/")
    APP_LOGO =  os.path.join(img_media, "logo.png")
    APP_LOGO_ICO = os.path.join(img_media, "logo.ico")
