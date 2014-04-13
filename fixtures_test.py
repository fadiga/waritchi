#!/usr/bin/env python
# encoding= utf-8
#maintainer : alou

from random import randint

from datetime import datetime
from models import  (Group, Operator, PhoneNumber, Contact,
                     ContactGroup, Transfer)


print "Group"

group_list = [u"kunafoni", u"LEO", u"Yeleman", u"fanga"]
for i in group_list:
    try:
        Group(name=i).save()
        print i, "............. OK"
    except:
        print i, "no..............."

print "Operator"
list_op = [('orange', u'Orange'), ('malitel', u'Malitel')]

for i, n in list_op:
    try:
        Operator(slug=i, name=n).save()
        print i, n, "............. OK"
    except:
        print n, "no"

print "PhoneNumber"
list_phone = [(76499055, 1, 1), (69500451, 2, 1),
              (76433890, 1, 2), (63341424, 2, 2),
              (73120896, 1, 3), (76333005, 1, 4),
              (66430000, 2, 5)]

for number, operator, contact in list_phone:
    try:
        PhoneNumber(number=number, operator=operator, contact=contact).save()
        print i, n, "............. OK"
    except:
        print n, "no"


print "Contact"

list_contacts = [u'alou Dolo', u'Ibrahima Fadiga',
                 u'Ali Toure', u'Renaud Gaudin',
                 u'Marie Augustine Rose Sidibe']

for contact in list_contacts:
    try:
        Contact(name=contact).save()
        print i, n, "............. OK"
    except:
        print i, n, "no"

print "ContactGroup"
Group.filter(id=1).get()
l_cont_group = [(1, 2), (1, 3), (1, 4),
                (2, 3), (2, 4),
                (3, 1), (3, 3),
                (4, 1), (4, 3),
                (5, 4)]

for c, g in l_cont_group:
    try:
        ContactGroup(contact=c, group=g).save()
        print c, g, "............. OK"
    except:
        print c, g, "............. OK"

print "Transfer"


for i in range(1, 15):
    try:
        num = randint(1, 5)
        Transfer(amount=randint(100, 1000),
                 date=datetime(2012, 11, randint(1, 29), randint(1, 23),
                               randint(1, 59), randint(1, 59)),
                 number=num).save()
        print (u"Transfert N:", i, " de ",
                Transfer.filter(number=num).get().number.contact.name,
                "............. OK")
    except:
        raise
        print i, "no"
