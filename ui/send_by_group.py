#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Fadiga

from PyQt4.QtGui import QVBoxLayout, QGridLayout, QDialog, QIntValidator, QFont

from models import Group, ContactGroup
from Common.ui.common import (FWidget, FBoxTitle, FLabel, LineEdit,
                              Button, ErrorLabel, EnterTabbedLineEdit)
from ussd import multiple_sender

try:
    unicode
except Exception as e:
    unicode = str


class SendGroupViewWidget(QDialog, FWidget):

    def __init__(self, table_group, parent, *args, **kwargs):
        QDialog.__init__(self, parent, *args, **kwargs)

        self.parent = table_group
        group_id = self.parent.table_group.group.group_id
        self.group = Group.select().where(Group.id == group_id).get()
        vbox = QVBoxLayout()
        vbox.addWidget(FBoxTitle(
            u"<h2>Envoi pour les ({0}) contactes du groupe <b>{1}</b></h2>".format(len(self.group.contacts), self.group.name)))

        # form transfer
        self.amount = LineEdit()
        self.amount.setFont(QFont("Arial", 15))
        self.amount.setValidator(QIntValidator())
        self.amount.setToolTip(u"Taper le montant du transfert")
        self.amount_error = ErrorLabel(u"")
        self.password_field = EnterTabbedLineEdit()
        self.password_field.setEchoMode(LineEdit.Password)
        self.password_field.setToolTip(u"Taper le code orange money")

        self.send_butt = Button(u"Envoyer")
        self.send_butt.clicked.connect(self.sender)
        cancel_but = Button(u"Annuler")
        cancel_but.clicked.connect(self.cancel)

        formbox = QGridLayout()
        formbox.addWidget(FLabel(u"Montant: "), 0, 0)
        formbox.addWidget(self.amount, 0, 1)
        formbox.addWidget(FLabel(u"Code: "), 1, 0)
        formbox.addWidget(self.password_field, 1, 1)
        formbox.addWidget(self.send_butt, 2, 1)
        formbox.addWidget(cancel_but, 2, 0)

        self.isvalid()

        vbox.addLayout(formbox)
        self.setLayout(vbox)

    def cancel(self):
        self.close()

    def isvalid(self):
        self.list_phone_num = [(i.contact.number) for i in
                               ContactGroup.filter(group__id=self.group.id)]
        if self.list_phone_num == []:
            self.send_butt.setEnabled(False)
            self.send_butt.setToolTip(u"""Ce groupe n'a pas le numéro de
                                          téléphone.""")

    def iscomplet(self):
        self.amount.setStyleSheet("")
        self.amount.setText(u"")
        self.password_field.setStyleSheet("")
        self.password_field.setText(u"")
        if unicode(self.amount.text()) == "":
            self.amount.setStyleSheet("font-size:20px; color: red")
            self.amount.setText(u"Ce champ est obligatoire.")
            return False
        if unicode(self.password_field.text()) == "":
            self.password_field.setStyleSheet("font-size:20px; color: red")
            self.password_field.setText(u"Ce champ est obligatoire.")
            return False
        return True

    def sender(self):
        if not self.iscomplet:
            return
        data = {"phone_num": self.list_phone_num,
                "code": unicode(self.password_field.text()),
                "amount": unicode(self.amount.text())
                }
        multiple_sender(data)
        self.cancel()
        self.parent.table_group.refresh_()
