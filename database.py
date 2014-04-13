#!/usr/bin/env python
# encoding=utf-8
# Autor: Fadiga

from models import  (Group, Operator, PhoneNumber, Contact, Version, Settings,
                     ContactGroup, Transfer, Owner, LocalSetting, SettingsAdmin)


def setup(drop_tables=False):
    """ create tables if not exist """

    did_create = False

    for models in [Group, Operator, Contact, PhoneNumber, LocalSetting, Settings,
                   ContactGroup, Transfer, Version, Owner, SettingsAdmin]:
        if drop_tables:
            models.drop_table()
        if not models.table_exists():
            models.create_table()
            did_create = True
    if did_create:
        from Common.fixture import init_fuxture
        print(u"---- Creation de la BD -----")
        init_fuxture()
