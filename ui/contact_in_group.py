#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Fadiga

import sqlite3

from PyQt4.QtGui import QVBoxLayout, QGridLayout, QDialog, QIntValidator, QFont

from models import Transfer, Group
from Common.ui.common import (F_Widget, F_BoxTitle, F_Label, LineEdit,
                              Button, ErrorLabel)
from ussd import multiple_sender


class ContactGroupViewWidget(QDialog, F_Widget):
    def __init__(self, table_group, parent, *args, **kwargs):
        QDialog.__init__(self, parent, *args, **kwargs)

        self.parent = table_group
        group_id = self.parent.table_group.group.group_id
        self.group = Group.select().where(Group.id==group_id).get()
        vbox = QVBoxLayout()
        vbox.addWidget(F_BoxTitle(u"<h3>Groupe: {}</h3>".format(self.group.name)))
        self.order_number = LineEdit()

        # form transfer
        self.amount = LineEdit()
        self.amount.setFont(QFont("Arial", 15))
        self.amount.setValidator(QIntValidator())
        self.amount.setToolTip(u"Taper le montant du transfert")
        # self.solde = F_Label(get_solde())
        self.amount_error = ErrorLabel(u"")

        send_butt = Button(u"Envoyer")
        send_butt.clicked.connect(self.sender)
        cancel_but = Button(u"Annuler")
        cancel_but.clicked.connect(self.cancel)

        formbox = QGridLayout()
        formbox.addWidget(F_Label(u"Montant: "), 0, 0)
        formbox.addWidget(self.amount, 0, 1)
        formbox.addWidget(send_butt, 2, 1)
        formbox.addWidget(cancel_but, 2, 0)

        vbox.addLayout(formbox)
        self.setLayout(vbox)

    def cancel(self):
        self.close()

    def isvalid(self):
        if unicode(self.amount.text()) == "":
            return False

    def iscomplet(self):
        self.amount.setStyleSheet("")
        self.amount.setText(u"")
        if unicode(self.amount.text()) == "":
            self.amount.setStyleSheet("font-size:20px; color: red")
            self.amount.setText(u"Ce champ est obligatoire.")
            return False

    def sender(self):

        if self.iscomplet:
            return
        list_phone_num = [(i.contact.number)
                          for i in ContactGroup.filter(group__id=self.group.id)]
        data = {"phone_num": list_phone_num,
                "code": "03944", "amount": unicode(self.amount.text())
        }
        print data
        # multiple_sender(data)
        self.cancel()
        self.parent.table_group.refresh_()
