#!/usr/bin/env python
# encoding=utf-8
# maintainer: fad

from PyQt4.QtGui import (QMessageBox, QMenuBar, QIcon, QAction, QPixmap)
from PyQt4.QtCore import SIGNAL, SLOT

from Common.ui.common import F_Widget
from Common.ui.cmenubar import F_MenuBar
from configuration import Config
from help import HTMLEditor
from ui.addressbook import ContactViewWidget


class MenuBar(F_MenuBar, F_Widget):

    def __init__(self, parent=None, *args, **kwargs):
        F_MenuBar.__init__(self, parent=parent, *args, **kwargs)

        self.parent = parent


        # Menu aller à
        goto_ = self.addMenu(u"&Aller a")

        # Records
        addressbook = QAction(QIcon("{}archive_add.png".format(Config.img_media)),
                         u"Gestion des documents", self)
        addressbook.setShortcut("Ctrl+C")
        self.connect(addressbook, SIGNAL("triggered()"), self.goto_addressbook)
        goto_.addAction(addressbook)

        # Menu Options
        menu_settings = self.addMenu(u"Options")
        menu_settings.addAction(QIcon('images/help.png'), u"Options",
                                    self.goto_settings)
        # Address Book
        #   > Add contact
        #   > Find contact
        #   > Delete contact
        adressbook = self.addMenu(u"Carnet d'adresse")
        adressbook.addAction(QIcon('images/help.png'), "Ajouter contact",
                                    self.goto_add_contact)
        adressbook.addAction(QIcon('images/help.png'),
                             "Recherher contact", self.goto_search_contact)


        # Help
        menu_help = self.addMenu(u"Aide")
        menu_help.addAction(QIcon('images/help.png'), "Aide",
                                    self.goto_help)


    def goto_addressbook(self):
        self.change_main_context(ContactViewWidget)

    #Add contact
    def goto_add_contact(self):
        QMessageBox.about(self, u"Ajouter contact",
                                u"<h3>Pour ajouter un contact</h3>")

    #Search contact
    def goto_search_contact(self):
        QMessageBox.about(self, u"Recherche contact",
                                u"<h3>Pour chercher un contact</h3>")

    #Delete contact
    def goto_delete_contact(self):
        QMessageBox.about(self, u"Supprimer contact",
                                u"<h3>Pour supprimer un contact</h3>")

    #Settings
    def goto_settings(self):
        QMessageBox.about(self, u"Options",
                                u"<h3>Settings</h3>")

    #Aide
    def goto_help(self):

        self.open_dialog(HTMLEditor, modal=True)
