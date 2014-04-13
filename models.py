#!/usr/bin/env python
# encoding=utf-8
# maintainer: Fadiga

from Common.ui.util import formatted_number
from datetime import datetime

DATE_FMT = u'%A %d %B %Y'

from Common import peewee
from Common.models import (BaseModel, Owner, Settings, SettingsAdmin, Version)


class Group(BaseModel):
    """ Group of contacts """

    name = peewee.CharField(max_length=30, verbose_name=u"Nom", unique=True)

    def __unicode__(self):
        return u"%(name)s" % {"name": self.display_name()}

    def display_name(self):
        return self.name.title()

    def to_dict(self):
        d = super(Group, self).to_dict()
        d.update({'name': self.name, 'display_name': self.display_name()})
        return d


class Operator(BaseModel):
    """ Operators """

    slug = peewee.CharField(max_length=30, verbose_name=u"Code", unique=True)
    name = peewee.CharField(max_length=30, verbose_name=u"Nom", unique=True)

    def __unicode__(self):
        return u"%(name)s" % {"name": self.name}

    def display_name(self):
        return self.name.title()


    def to_dict(self):
        d = super(Operator, self).to_dict()
        d.update({'display_name': self.display_name(),
                  'name': self.name, 'slug': self.slug})
        return d


class Contact(BaseModel):
    """ Contact address book """

    name = peewee.CharField(max_length=100, verbose_name=u"Nom", unique=True)

    def __unicode__(self):
        return u"%(name)s" % {"name": self.display_name()}

    def display_name(self):
        return self.name.title()

    def to_dict(self, verbose=False):
        d = super(Contact, self).to_dict()
        d.update({'display_name': self.display_name(),
                  'name': self.name})
        if verbose:
            d.update({'numbers': [number.to_dict() for number in PhoneNumber \
                                                        .filter(contact=self)],
                      'groups': [contact_group.group.to_dict()
                                 for contact_group in ContactGroup \
                                                      .filter(contact=self)]})
        return d


class PhoneNumber(BaseModel):
    """ Contact number """

    number = peewee.IntegerField(verbose_name=u"Numero de téléphone")
    operator = peewee.ForeignKeyField(Operator, verbose_name=u"Opérateur")
    contact = peewee.ForeignKeyField(Contact, verbose_name=u"Contact")

    def __unicode__(self):
        return u"%(number)s" % {u"number": self.number}

    def display_number(self):
        return formatted_number(self.number)

    def full_name(self):
        try:
            return self.contact.name
        except:
            return self.number

    def to_dict(self):
        d = super(PhoneNumber, self).to_dict()
        d.update({'number': self.number,
                  'operator': self.operator.to_dict(),
                  'display_number': self.display_number()})
        return d


class ContactGroup(BaseModel):
    """ Contact with group """

    contact = peewee.ForeignKeyField(Contact, verbose_name=u"Contact")
    group = peewee.ForeignKeyField(Group, verbose_name=u"Groupe")


class Transfer(BaseModel):
    """ Ensemble des  transferts effectués """

    amount = peewee.IntegerField(verbose_name=u"Montant")
    number = peewee.ForeignKeyField(PhoneNumber, verbose_name=u"Téléphone")
    date = peewee.DateTimeField(verbose_name=u"Date")

    def __unicode__(self):
        return u"%(amount)s/%(number)s" % {"number": self.number,
                                           "amount": self.amount}

    def to_dict(self):
        d = super(Transfer, self).to_dict()
        d.update({'number': self.number.to_dict(),
                  'amount': self.amount,
                  'date': self.date.isoformat(),
                  'display_date': self.date.strftime(DATE_FMT)})
        return d


class LocalSetting(BaseModel):
    password = peewee.CharField(max_length=30, verbose_name=(u"Nom"))
    password_orange = peewee.CharField(max_length=30,
                                         verbose_name=(u"Mot de passe Orange"))
    password_malitel = peewee.CharField(max_length=30,
                                        verbose_name=(u"Mot de passe Malitel"))
