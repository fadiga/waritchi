#!/usr/bin/env python
# encoding=utf-8
# Autor: Fadiga

from models import  (Group, Contact, Version, Settings,
                     ContactGroup, Transfer, Owner, LocalSetting, SettingsAdmin)


def setup(drop_tables=False):
    """ create tables if not exist """

    did_create = False

    for models in [ Version, Owner, SettingsAdmin, LocalSetting, Settings,Group, Contact,
                   ContactGroup, Transfer,]:
        if drop_tables:
            models.drop_table()
        if not models.table_exists():
            models.create_table()
            did_create = True
    if did_create:
        from Common.fixture import init_fuxture
        from fixtures import localfixture
        print(u"---- Creation de la BD -----")
        init_fuxture()
        localfixture()

