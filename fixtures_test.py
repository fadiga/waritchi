#!/usr/bin/env python
# -*- coding: utf8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# maintainer: Fad

from __future__ import (unicode_literals, absolute_import, division, print_function)

import os, sys; sys.path.append(os.path.abspath('../'))

from random import randint

from datetime import datetime
from models import  (Group, PhoneNumber, Contact,
                     ContactGroup, Transfer)


print( "Group")

group_list = [u"kunafoni", u"LEO", u"Yeleman", u"fanga"]
for i in group_list:
    try:
        Group(name=i).save()
        print( i, "............. OK")
    except:
        print( i, "no...............")


print( "PhoneNumber")
list_phone = [(76499055, 1), (69500451, 1),
              (76433890, 2), (63341424, 2),
              (73120896, 3), (76333005, 4),
              (66430000, 5)]

for number, contact in list_phone:
    try:
        PhoneNumber(number=number, contact=contact).save()
        print( number, contact, "............. OK")
    except:
        print(number, "no")


print( "Contact")

list_contacts = [u'alou Dolo', u'Ibrahima Fadiga',
                 u'Ali Toure', u'Renaud Gaudin',
                 u'Marie Augustine Rose Sidibe']

for contact in list_contacts:
    try:
        Contact(name=contact).save()
        print(contact, "............. OK")
    except:
        print(contact, "no")

print( "ContactGroup")
Group.filter(id=1).get()
l_cont_group = [(1, 2), (1, 3), (1, 4),
                (2, 3), (2, 4),
                (3, 1), (3, 3),
                (4, 1), (4, 3),
                (5, 4)]

for c, g in l_cont_group:
    try:
        ContactGroup(contact=c, group=g).save()
        print( c, g, "............. OK")
    except:
        print( c, g, "............. OK")

print( "Transfer")


for i in range(1, 15):
    try:
        num = randint(1, 5)
        Transfer(amount=randint(100, 1000),
                 date=datetime(2012, 11, randint(1, 29), randint(1, 23),
                               randint(1, 59), randint(1, 59)),
                 number=num).save()
        print(u"Transfert N:", i, " de ",
                Transfer.filter(number=num).get().number.contact.name,
                "............. OK")
    except:
        raise
        print( i, "no")
