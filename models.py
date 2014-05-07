#!/usr/bin/env python
# encoding=utf-8
# maintainer: Fadiga

from datetime import datetime

DATE_FMT = u'%c'

from Common import peewee
from Common.models import (BaseModel, Owner, Organization, SettingsAdmin, Version)


class Group(BaseModel):
    """ Group of contacts """
    class Meta:
        order_by = ('name',)

    name = peewee.CharField(max_length=30, verbose_name=u"Nom", unique=True)

    def __unicode__(self):
        return u"{name}".format(name=self.name)

    def display_name(self):
        return self.name.title()

    def to_dict(self):
        d = super(Group, self).to_dict()
        d.update({'name': self.name, 'display_name': self.display_name()})
        return d

    @property
    def contacts(self):
        return [p.contact for p in ContactGroup.select().where(ContactGroup.group==self)]


class Contact(BaseModel):
    """ Contact address book """
    class Meta:
        order_by = ('name', 'number')


    name = peewee.CharField(max_length=200, verbose_name=u"Nom", null=True )
    number = peewee.IntegerField(verbose_name=u"Numero de téléphone", unique=True)

    def __unicode__(self):
        return u"{name}/{number}".format(name=self.name, number=self.number)

    def display_name(self):
        from Common.ui.util import formatted_number
        ctct = "{}".format(formatted_number(self.number))
        if self.name:
            ctct = u"({number}) {name}".format(name=self.name.title(), number=ctct)
        return ctct

    @classmethod
    def get_or_create(cls, number):
        try:
            ctct = cls.get(number=number)
        except cls.DoesNotExist:
            ctct = cls.create(number=number)
        return ctct

    def to_dict(self, verbose=False):
        d = super(Contact, self).to_dict()
        d.update({'display_name': self.display_name(),
                  'name': self.name})
        if verbose:
            d.update({'numbers': self.number,
                      'groups': [contact_group.group.to_dict()
                                 for contact_group in ContactGroup \
                                                      .filter(contact=self)]})
        return d


class ContactGroup(BaseModel):
    """ Contact with group """

    contact = peewee.ForeignKeyField(Contact, verbose_name=u"Contact")
    group = peewee.ForeignKeyField(Group, verbose_name=u"Groupe")

    @classmethod
    def get_or_create(cls, contact, group):
        try:
            ctct = cls.get(contact=contact, group=group)
        except cls.DoesNotExist:
            ctct = cls.create(contact=contact, group=group)
        return ctct


class Transfer(BaseModel):
    """ Ensemble des  transferts effectués """
    class Meta:
        order_by = ('date', 'contact')

    amount = peewee.IntegerField(verbose_name=u"Montant")
    contact = peewee.ForeignKeyField(Contact, verbose_name=u"Téléphone")
    date = peewee.DateTimeField(verbose_name=u"Date", default=datetime.now)
    response = peewee.CharField(verbose_name=u"Reponse", default="Inconu")

    def __unicode__(self):
        return u"{contact}/{amount}/{date}".format(contact=self.contact,
                                                   amount=self.amount,
                                                   date=self.strftime(DATE_FMT))

    def to_dict(self):
        d = super(Transfer, self).to_dict()
        d.update({'contact': self.contact.to_dict(),
                  'amount': self.amount,
                  'date': self.date.isoformat(),
                  'response': self.response,
                  'display_date': self.date.strftime(DATE_FMT)})
        return d


class LocalSetting(BaseModel):
    slug = peewee.IntegerField(default=1)
    baudrate = peewee.CharField(max_length=30, verbose_name=(u"baudrate"),
                                default="115200")
    port = peewee.CharField(max_length=100, verbose_name=(u"PORT"), default="/dev/ttyUSB2")
    code_consultation = peewee.CharField(max_length=100, verbose_name=(u"Consultation",),
                                        null=True)
    code_send = peewee.CharField(max_length=100, verbose_name=(u"Envoie"), null=True)

    def __unicode__(self):
        return u"{port}".format(port=self.port)

    @classmethod
    def get_or_create(cls, slug):
        try:
            ctct = cls.get(slug=slug)
            print(ctct)
        except cls.DoesNotExist:
            ctct = cls.create(slug=slug)
        return ctct
