#!/usr/bin/env python
# -*- coding: utf8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# maintainer: Fad
from __future__ import (unicode_literals, absolute_import, division, print_function)

from datetime import datetime

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QVBoxLayout, QGridLayout, QDialog, QIntValidator, QFont

from Common.ui.common import (F_Widget, F_PageTitle, Button, F_Label, LineEdit,
                              ErrorLabel, EnterTabbedLineEdit)
from Common.ui.util import formatted_number, raise_success, raise_error
from Common.ui.table import F_TableWidget
from database import Transfer, Contact
from ussd import multiple_sender


class HomeViewWidget(F_Widget):
    """ Shows the home page  """

    def __init__(self, parent=0, *args, **kwargs):
        super(HomeViewWidget, self).__init__(parent=parent,
                                                        *args, **kwargs)

        self.table = OperationTableWidget(parent=self)
        table_box = QVBoxLayout()
        self.title_table = F_PageTitle(u"Historique des transferts")
        table_box.addWidget(self.title_table)
        table_box.addWidget(self.table)

        self.parent = parent
        self.parentWidget().setWindowTitle(u"Bienvenu sur transfert Wari")
        self.title = F_PageTitle(u"Tranfert")
        # form transfer
        self.number = LineEdit()
        self.number.setInputMask("D9.99.99.99")
        self.number.setAlignment(Qt.AlignCenter)
        self.number.setFont(QFont("Arial", 17))
        self.number.setToolTip(u"""Taper le nom ou le numéro de téléphone du
                                beneficiare""")

        self.amount = LineEdit()
        self.amount.setFont(QFont("Arial", 15))
        self.amount.setValidator(QIntValidator())
        self.amount.setToolTip(u"Taper le montant du transfert")
        self.password_field = EnterTabbedLineEdit()
        self.password_field.setFont(QFont("Arial", 15))
        self.password_field.setEchoMode(LineEdit.Password)
        self.password_field.setToolTip(u"Taper le code orange money")

        butt = Button(u"Envoyer")
        butt.clicked.connect(self.get_or_creat_nbr)

        formbox = QGridLayout()
        formbox.addWidget(F_Label(u"Numéro"), 0, 0)
        formbox.addWidget(self.number, 1, 0)
        formbox.addWidget(F_Label(u"Montant"), 0, 1)
        formbox.addWidget(self.amount, 1, 1)
        formbox.addWidget(F_Label(u"code"), 0, 2)
        formbox.addWidget(self.password_field, 1, 2)
        formbox.addWidget(butt, 1, 4)
        formbox.setColumnStretch(5, 3)

        transfer_box = QVBoxLayout()
        # formbox.setSizeConstraint(QLayout.SetFixedSize)
        transfer_box.addWidget(self.title)
        transfer_box.addLayout(formbox)
        transfer_box.addLayout(table_box)
        self.setLayout(transfer_box)

    def get_or_creat_nbr(self):
        ''' add operation '''

        if not self.is_complete():
            return

        number = self.number.text().replace('.', '')

        try:
            phonenumber = Contact.get(number=number)
        except:
            phonenumber = Contact(number=number,contact=None)
        phonenumber.save()
        self.send_for(phonenumber)

    def send_for(self, number):
        data = {"phone_num": [number,],
                "code": unicode(self.password_field.text()),
                 "amount": self.amount.text()}
        if amount:
            transfer = Transfer()
            transfer.amount = self.amount.text()
            transfer.number = number
            transfer.date = datetime.now()
            transfer.reponse = multiple_sender(data).message
            transfer.save()
            self.number.clear()
            self.amount.clear()
            self.table.refresh_()
            raise_success(u'Confirmation', u'Transfert effectué')
        else:
            raise_error(u"Erreur Montant",
                        u"Donner un montant s'il vous plait.")

    def is_complete(self):
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


class OperationTableWidget(F_TableWidget):
    """ display all transfers """
    def __init__(self, parent, *args, **kwargs):

        F_TableWidget.__init__(self, parent=parent, *args, **kwargs)
        self.hheaders = [u'Contact', u'Montant', u'Heure', 'Status']
        self.stretch_columns = [2]
        self.align_map = {1: 'l'}
        self.display_vheaders = True
        self.display_fixed = True
        self.refresh_()

    def refresh_(self):
        """ refresh table """
        self._reset()
        self.set_data_for()
        self.refresh()
        pw = 100
        self.setColumnWidth(0, pw * 3)
        self.setColumnWidth(1, pw)
        self.setColumnWidth(2, pw * 3)
        self.setColumnWidth(3, 40)


    def set_data_for(self):
        """ completed the table """
        self._data = [(transfer.contact.number, formatted_number(transfer.amount) + " fcfa",
                      transfer.date.strftime(u"%c"), transfer.response)
                      for transfer in Transfer.select()]
