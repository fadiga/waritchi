#!/usr/bin/env python
# -*- coding: utf8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# maintainer: Fad
from __future__ import (unicode_literals, absolute_import, division, print_function)

from static import Constants


class Config(Constants):
    """ docstring for Config
                            """
    def __init__(self):
        Constants.__init__(self)

    # ------------------------- Organisation --------------------------#

    from models import Organization, Version
    try:
        sttg = Organization.get(id=1)
    except:
        sttg = Organization(login=True, name_orga="Demo",
                         adress_org="Bamako Boulkassoumbougou",
                         email_org="demo@demo.ml", bp="177")

    try:
        DB_VERS = Version.get(id=1)
    except:
        DB_VERS = Version(number=1)

    LOGIN = sttg.login
    NAME_ORGA = sttg.name_orga
    TEL_ORGA = sttg.phone
    ADRESS_ORGA = sttg.adress_org
    BP = sttg.bp
    EMAIL_ORGA = sttg.email_org

