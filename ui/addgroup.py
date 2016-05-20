#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Fadiga

import sqlite3

from PyQt4.QtGui import QVBoxLayout, QGridLayout, QDialog

from models import Group
from Common.ui.common import FWidget, FBoxTitle, FLabel, LineEdit, Button

try:
    unicode
except Exception as e:
    unicode = str


class GroupViewWidget(QDialog, FWidget):

    def __init__(self, table_group, parent, *args, **kwargs):
        QDialog.__init__(self, parent, *args, **kwargs)

        vbox = QVBoxLayout()
        vbox.addWidget(FBoxTitle(u"Ajout d'un nouveau groupe"))
        self.parent = table_group

        self.name = LineEdit()
        formbox = QGridLayout()

        self.error_field = FLabel(u"")
        formbox.addWidget(self.error_field, 0, 1)
        formbox.addWidget(FLabel(u"Nom"), 1, 0)
        formbox.addWidget(self.name, 1, 1)
        butt = Button(u"Enregistrer")
        butt.clicked.connect(self.edit_prod)
        cancel_but = Button(u"Annuler")
        cancel_but.clicked.connect(self.cancel)
        formbox.addWidget(butt, 2, 1)
        formbox.addWidget(cancel_but, 2, 0)

        formbox.setColumnStretch(3, 3)
        formbox.setRowStretch(2, 2)
        vbox.addLayout(formbox)
        self.setLayout(vbox)

    def cancel(self):
        self.close()

    def isvalid(self):
        if unicode(self.name.text()) == "":
            return False

    def edit_prod(self):
        self.error_field.setStyleSheet("")
        name = unicode(self.name.text())
        if name == "":
            self.error_field.setStyleSheet("font-size:20px; color: red")
            self.error_field.setText(u"Ce champ est obligatoire.")
            return False

        group = Group()
        try:
            group.name = name
            group.save()
            self.cancel()
            self.parent.table_group.refresh_()
        except sqlite3.IntegrityError:
            self.error_field.setStyleSheet("font-size:20px; color: red")
            self.error_field.setText(u"%s existe déjà" % name)
