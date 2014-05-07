#!/usr/bin/env python
# encoding=utf-8
# maintainer: fad

from PyQt4.QtGui import (QMessageBox, QIcon, QAction)
from PyQt4.QtCore import SIGNAL

from Common.ui.common import F_Widget
from Common.ui.cmenubar import F_MenuBar
from configuration import Config
from ui.addressbook import ContactViewWidget
from ui.contact_add import ContactNewViewWidget
from ui.settings import SettgViewWidget


class MenuBar(F_MenuBar, F_Widget):
    def __init__(self, parent=None, *args, **kwargs):
        F_MenuBar.__init__(self, parent=parent, *args, **kwargs)

        self.parent = parent

        # Menu aller à
        goto_ = self.addMenu(u"&Aller a")

        # Address Book
        #   > Add contact
        #   > Find contact
        #   > Delete contact
        addressbook = QAction(QIcon("{}archive_add.png".format(Config.img_media)),
                              u"Carnet d'adresse", self)
        addressbook.setShortcut("Ctrl+C")
        self.connect(addressbook, SIGNAL("triggered()"), self.goto_addressbook)
        goto_.addAction(addressbook)

        addcontact = QAction(QIcon("{}addcontact.png".format(Config.img_media)),
                             u"Nouvel contact", self)
        addcontact.setShortcut("Ctrl+N")
        self.connect(addcontact, SIGNAL("triggered()"), self.goto_add_contact)
        goto_.addAction(addcontact)

        dashboard = QAction(QIcon("{}dashboard.png".format(Config.img_media)),
                             u"Tableau de bord", self)
        dashboard.setShortcut("Ctrl+T")
        self.connect(dashboard, SIGNAL("triggered()"), self.dashboard)
        goto_.addAction(dashboard)

        # adressbook.addAction(QIcon('images/help.png'),
        #                      "Recherher contact", self.goto_search_contact)
        # Menu Options
        menu_settings = self.addMenu(u"Options")
        solde = QAction(QIcon("{}solde.png".format(Config.img_media)),
                             u"Solde du compte", self)
        solde.setShortcut("Ctrl+S")
        self.connect(solde, SIGNAL("triggered()"), self.show_solde)
        menu_settings.addAction(solde)

        config = QAction(QIcon("{}config.png".format(Config.img_media)),
                             u"Préference", self)
        config.setShortcut("Ctrl+I")
        self.connect(config, SIGNAL("triggered()"), self.show_config)
        menu_settings.addAction(config)

        # Help
        menu_help = self.addMenu(u"Aide")
        menu_help.addAction(QIcon('images/help.png'), "Aide",
                                    self.goto_help)


    def dashboard(self):
        from ui.home import HomeViewWidget
        self.change_main_context(HomeViewWidget)

    def goto_addressbook(self):
        self.change_main_context(ContactViewWidget)

    #Add contact
    def goto_add_contact(self):
        self.open_dialog(ContactNewViewWidget, modal=True)

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

    def show_config(self):
        self.open_dialog(SettgViewWidget, modal=True)

    # Solde
    def show_solde(self):
        from ussd import get_solde
        try:
            mgs = u"""<h4>{}</h4>""".format(get_solde())
        except Exception as e:
            raise
            print(e)
            mgs = u"Veuillez branché le modem (cléf 3g)"
        QMessageBox.about(self, u"Solde", mgs)

    #Aide
    def goto_help(self):

        from help import HTMLEditor
        self.open_dialog(HTMLEditor, modal=True)
