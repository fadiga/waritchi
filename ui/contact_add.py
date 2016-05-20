#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Fadiga
from __future__ import (
    unicode_literals, absolute_import, division, print_function)

import sqlite3

from PyQt4.QtGui import (QVBoxLayout, QGridLayout, QDialog, QIntValidator, QFont,
                         QComboBox)
from PyQt4.QtCore import QVariant, Qt

from models import Contact, Group, ContactGroup
from Common.ui.util import raise_success, raise_error
from Common.ui.common import (FWidget, FBoxTitle, FLabel, LineEdit,
                              Button, ErrorLabel, IntLineEdit)
# from ussd import multiple_sender
try:
    unicode
except Exception as e:
    unicode = str


class ContactNewViewWidget(QDialog, FWidget):

    def __init__(self, parent, *args, **kwargs):
        QDialog.__init__(self, parent, *args, **kwargs)

        vbox = QVBoxLayout()
        vbox.addWidget(FBoxTitle(u"<h3>Ajout de contact </h3>"))
        self.combo_grp = QComboBox()
        groups = Group()
        groups.name = "Aucun"

        self.list_grp = Group.all()
        self.list_grp.append(groups)
        self.list_grp.reverse()

        for index in self.list_grp:
            sentence = u"%(name)s" % {'name': index.name}
            self.combo_grp.addItem(sentence)

        self.full_name = LineEdit()
        self.msg_e_or_c = FLabel("")
        self.full_name.setFont(QFont("Arial", 16))
        self.phone_number = IntLineEdit()
        self.phone_number.setInputMask("D9.99.99.99")
        self.phone_number.setAlignment(Qt.AlignCenter)
        self.phone_number.setFont(QFont("Arial", 16))

        send_butt = Button(u"Enregistrer")
        send_butt.clicked.connect(self.save_form)
        cancel_but = Button(u"Fermer")
        cancel_but.clicked.connect(self.cancel)

        formbox = QGridLayout()
        formbox.addWidget(FLabel(u"Groupes:"), 0, 0)
        formbox.addWidget(self.combo_grp, 1, 0)
        formbox.addWidget(FLabel(u"Nom complèt: "), 0, 1)
        formbox.addWidget(self.full_name, 1, 1)
        formbox.addWidget(FLabel(u"Numéro: "), 0, 2)
        formbox.addWidget(self.phone_number, 1, 2)
        formbox.addWidget(send_butt, 2, 1)
        formbox.addWidget(cancel_but, 2, 0)
        formbox.addWidget(self.msg_e_or_c, 3, 0, 3, 2)

        vbox.addLayout(formbox)
        self.setLayout(vbox)

    def cancel(self):
        self.close()

    def iscomplet(self):
        self.phone_number.setStyleSheet("")
        self.msg_e_or_c.setText("")
        self.msg_e_or_c.setStyleSheet("")

        try:
            int(self.phone_number.text().replace('.', ''))
        except:
            self.phone_number.setStyleSheet("border-bottom: 3px solid red;"
                                            "background-color:#AFAFAF;")
            self.phone_number.setToolTip(u"Ce champ est obligatoire.")
            return False
        return True

    def save_form(self):

        if not self.iscomplet():
            return
        full_name = unicode(self.full_name.text())
        phone_number = int(self.phone_number.text().replace('.', ''))
        try:
            Contact(number=phone_number, name=full_name).save()
        except:
            self.msg_e_or_c.setText(u"Ce numéro existe déjà")
            self.msg_e_or_c.setStyleSheet("color: red")
            return

        grp = unicode(self.list_grp[self.combo_grp.currentIndex()])

        if not grp == "Aucun":
            grp = Group.select().where(Group.name == grp).get()
            contact = Contact.select().where(Contact.number == phone_number).get()
            ContactGroup(group=grp.id, contact=contact).save()
        self.full_name.setText("")
        self.phone_number.setText("")
        self.msg_e_or_c.setText(u"Le numéro (<b>{}</b>) à éte bien enregistré"
                                .format(phone_number))
