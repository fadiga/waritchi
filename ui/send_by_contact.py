#!/usr/bin/env python
# encoding=utf-8
# maintainer: Fadiga

from PyQt4.QtGui import QVBoxLayout, QGridLayout, QDialog, QIntValidator, QFont

from models import Contact
from Common.ui.common import (F_Widget, F_BoxTitle, F_Label, LineEdit,
                              Button, ErrorLabel, EnterTabbedLineEdit)
from ussd import multiple_sender


class SendByCtViewWidget(QDialog, F_Widget):
    def __init__(self, ctct_id, parent, *args, **kwargs):
        QDialog.__init__(self, parent, *args, **kwargs)

        self.contact = Contact.select().where(Contact.id==ctct_id).get()
        vbox = QVBoxLayout()
        vbox.addWidget(F_BoxTitle(u"<h2>Envoie pour le contact <b>{}</b></h2>".format(self.contact.display_name())))
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
        formbox.addWidget(F_Label(u"Montant: "), 0, 0)
        formbox.addWidget(self.amount, 0, 1)
        formbox.addWidget(F_Label(u"Code: "), 1, 0)
        formbox.addWidget(self.password_field, 1, 1)
        formbox.addWidget(self.send_butt, 2, 1)
        formbox.addWidget(cancel_but, 2, 0)

        self.isvalid()

        vbox.addLayout(formbox)
        self.setLayout(vbox)

    def cancel(self):
        self.close()

    def isvalid(self):
        return True

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
        data = {"phone_num": [self.contact.number],
                "code": unicode(self.password_field.text()),
                "amount": unicode(self.amount.text())
        }
        multiple_sender(data)
        self.cancel()
