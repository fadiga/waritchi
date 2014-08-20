#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Autor: Fadiga

from Common.models import Version, Organization, Owner, SettingsAdmin
from models import  (Group, Contact, ContactGroup, Transfer, LocalSetting)


def setup(drop_tables=False):
    """ create tables if not exist """

    did_create = False

    for models in [Version, Owner, SettingsAdmin, LocalSetting, Organization,
                   Group, Contact, ContactGroup, Transfer]:
        if drop_tables:
            models.drop_table()
        if not models.table_exists():
            models.create_table()
            did_create = True
    if did_create:
        from fixture import fixt_init
        fixt_init().creat_all_or_pass()
