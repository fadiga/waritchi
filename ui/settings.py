#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Fadiga

import sqlite3

from PyQt4.QtGui import QVBoxLayout, QGridLayout, QDialog

from models import LocalSetting
from Common.ui.common import FWidget, FBoxTitle, FLabel, LineEdit, Button
try:
    unicode
except Exception as e:
    unicode = str


class SettgViewWidget(QDialog, FWidget):

    def __init__(self, parent, *args, **kwargs):
        QDialog.__init__(self, parent, *args, **kwargs)

        vbox = QVBoxLayout()
        vbox.addWidget(FBoxTitle(u" Configuration "))

        self.sttg = LocalSetting.get(LocalSetting.slug == 1)

        self.baudrate = LineEdit(self.sttg.baudrate)
        self.code_consultation = LineEdit(self.sttg.code_consultation)
        self.code_send = LineEdit(self.sttg.code_send)
        self.code_send.setEchoMode(LineEdit.Password)
        self.port = LineEdit(self.sttg.port)

        formbox = QGridLayout()
        formbox.addWidget(FLabel(u"Mon de passe"), 1, 0)
        formbox.addWidget(self.baudrate, 1, 1)
        formbox.addWidget(FLabel(u"Consultation"), 2, 0)
        formbox.addWidget(self.code_consultation, 2, 1)
        formbox.addWidget(FLabel(u"Code envoi"), 3, 0)
        formbox.addWidget(self.code_send, 3, 1)
        formbox.addWidget(FLabel(u"PORT"), 4, 0)
        formbox.addWidget(self.port, 4, 1)
        butt = Button(u"Enregistrer")
        butt.clicked.connect(self.edit_prod)
        cancel_but = Button(u"Annuler")
        cancel_but.clicked.connect(self.cancel)
        formbox.addWidget(butt, 5, 1)
        formbox.addWidget(cancel_but, 5, 0)

        formbox.setColumnStretch(3, 3)
        formbox.setRowStretch(2, 2)
        vbox.addLayout(formbox)
        self.setLayout(vbox)

    def cancel(self):
        self.close()

    def edit_prod(self):
        self.port.setStyleSheet("")
        baudrate = unicode(self.baudrate.text())
        code_consultation = unicode(self.code_consultation.text())
        code_send = unicode(self.code_send.text())
        port = unicode(self.port.text())
        if port == "":
            self.port.setStyleSheet("font-size:20px; color: red")
            self.port.setText(u"Ce champ est obligatoire.")
            return False

        try:
            self.sttg.baudrate = baudrate
            self.sttg.code_consultation = code_consultation
            self.sttg.code_send = code_send
            self.sttg.port = port
            self.sttg.save()
            self.cancel()
        except sqlite3.IntegrityError:
            self.port.setStyleSheet("font-size:20px; color: red")
