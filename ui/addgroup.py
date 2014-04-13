#!/usr/bin/env python
# encoding=utf-8
# maintainer: Fadiga

import sqlite3

from PyQt4 import QtGui

from models import Group
from Common.ui.common import F_Widget, F_BoxTitle


class GroupViewWidget(QtGui.QDialog, F_Widget):
    def __init__(self, table_group, parent, *args, **kwargs):
        QtGui.QDialog.__init__(self, parent, *args, **kwargs)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(F_BoxTitle(u"Ajout d'un nouveau groupe"))
        self.parent = table_group

        self.name = QtGui.QLineEdit()
        editbox = QtGui.QGridLayout()

        self.error_field = QtGui.QLabel(u"")
        editbox.addWidget(self.error_field, 0, 1)
        editbox.addWidget(QtGui.QLabel(u"Nom"), 1, 0)
        editbox.addWidget(self.name, 1, 1)
        bicon = QtGui.QIcon.fromTheme('document-save',
                                       QtGui.QIcon(''))
        butt = QtGui.QPushButton(bicon, u"Enregistrer")
        butt.clicked.connect(self.edit_prod)
        cancel_but = QtGui.QPushButton(u"Annuler")
        cancel_but.clicked.connect(self.cancel)
        editbox.addWidget(butt, 2, 1)
        editbox.addWidget(cancel_but, 2, 0)

        vbox.addLayout(editbox)
        self.setLayout(vbox)

    def cancel(self):
        self.close()

    def isvalid(self):
        if unicode(self.name.text()) == "":
            return False

    def edit_prod(self):
        self.error_field.setStyleSheet("")
        self.error_field.setText(u"")

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
