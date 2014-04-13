#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Fadiga

from PyQt4 import QtGui, QtCore
from datetime import datetime
from Common.ui.common import F_Widget, F_PageTitle, Button
from Common.ui.util import formatted_number, raise_success, raise_error
from Common.ui.table import F_TableWidget
from database import Transfer, PhoneNumber, Operator


class HomeViewWidget(F_Widget):
    """ Shows the home page  """

    def __init__(self, parent=0, *args, **kwargs):
        super(HomeViewWidget, self).__init__(parent=parent,
                                                        *args, **kwargs)

        self.table = OperationTableWidget(parent=self)
        table_box = QtGui.QVBoxLayout()
        self.title_table = F_PageTitle(u"Historique des transferts")
        table_box.addWidget(self.title_table)
        table_box.addWidget(self.table)

        self.parent = parent
        self.parentWidget().setWindowTitle(u"Bienvenu sur transfert Wari")
        self.title = F_PageTitle(u"Tranfert credit")
        self.order_number = QtGui.QLineEdit()

        # form transfer
        self.number = QtGui.QLineEdit()
        self.number.setInputMask("D9.99.99.99")
        self.number.setAlignment(QtCore.Qt.AlignCenter)
        self.number.setFont(QtGui.QFont("Arial", 18))
        self.number.setText(u"70.00.00.00")
        self.number.setToolTip(u"Taper le nom ou le numéro de "
                                     u"téléphone du beneficiare")

        self.amount = QtGui.QLineEdit()
        self.amount.setValidator(QtGui.QIntValidator())
        self.amount.setToolTip(u"Taper le montant du transfert")

        butt = Button(u"OK")
        butt.clicked.connect(self.add_operation)

        formbox = QtGui.QGridLayout()
        formbox.addWidget(self.number, 0, 0)
        formbox.addWidget(self.amount, 0, 1)
        formbox.addWidget(butt, 0, 2)

        transfer_box = QtGui.QVBoxLayout()
        formbox.setSizeConstraint(QtGui.QLayout.SetFixedSize)

        transfer_box.addWidget(self.title)

        transfer_box.addLayout(formbox)
        formbox.addWidget(butt)

        transfer_box.addLayout(table_box)
        self.setLayout(transfer_box)

    def add_operation(self):
        ''' add operation '''

        number = self.number.text().replace('.', '')

        phonenumber = self.verification_number(number)

        if phonenumber.operator.slug == 'orange':
            self.send_orange(phonenumber)
        elif phonenumber.operator.slug == 'malitel':
            self.send_malitel(phonenumber)

    def verification_number(self, number):
        """ Check number """
        try:
            return PhoneNumber.get(number=number)
        except:
            phonenumber = PhoneNumber()
            phonenumber.number = number
            if number.startswith('7'):
                phonenumber.operator = Operator.get(slug='orange')
            elif number.startswith('6'):
                phonenumber.operator = Operator.get(slug='malitel')
            phonenumber.contact = None
            phonenumber.save()

            return phonenumber

    def send_orange(self, number):
        """ Transfer credit Orange """

        self.transfer_credit(number)
        return u"function Orange"

    def send_malitel(self, number):
        """ Transfer credit Malitel """
        self.transfer_credit(number)
        return u"function Malitel"

    def transfer_credit(self, number):
        """ transfer amount credit"""
        date_send = datetime.now()
        amount = self.amount.text()
        if amount:
            transfer = Transfer(amount=self.amount.text(), number=number,
                                date=date_send)

            transfer.save()

            self.number.setText(u"70.00.00.00")
            self.amount.clear()
            self.table.refresh_()
            raise_success(u'Confirmation', u'Transfert effectué')
        else:
            raise_error(u"Erreur Montant",
                        u"Donner un montant s'il vous plait.")


class OperationTableWidget(F_TableWidget):
    """ display all transfers """
    def __init__(self, parent, *args, **kwargs):

        F_TableWidget.__init__(self, parent=parent, *args, **kwargs)
        self.max_width = 450
        self.header = [u'Contact', u'Montant', u'Heure', 'Status']

        self.set_data_for()
        self.refresh(True)

    def refresh_(self):
        """ refresh table """
        self._reset()
        self.set_data_for()
        self.refresh(True)

    def set_data_for(self):
        """ completed the table """
        self._data = [(operation.number.full_name(),
                       formatted_number(operation.amount) + " fcfa",
                      operation.date.strftime(u'%H:%M')) \
                      for operation in Transfer.select().order_by('date')]
