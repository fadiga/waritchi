#!/usr/bin/env python
# -*- coding: utf8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# maintainer: Fad

from __future__ import (unicode_literals, absolute_import, division, print_function)

from PyQt4.QtGui import QIcon

from Common.ui.common import FMainWindow

from Common.models import Owner
from configuration import Config

from ui.menubar import MenuBar
from ui.statusbar import GStatusBar


class MainWindow(FMainWindow):
    def __init__(self):
        FMainWindow.__init__(self)

        self.setWindowIcon(QIcon.fromTheme('logo',
                                           QIcon(u"{}".format(Config.APP_LOGO))))
        self.statusbar = GStatusBar(self)
        self.setStatusBar(self.statusbar)
        self.active_menu()
        from ui.home import HomeViewWidget
        self.page = HomeViewWidget
        self.change_context(self.page)

    def restart(self):
        self.logout()
        from main_record import main
        self.close()
        main()

    def exit(self):
        self.logout()
        self.close()

    def active_menu(self):
        self.menubar = MenuBar(self)
        self.setMenuBar(self.menubar)

    def logout(self):
        try:
            self.menubar.setEnabled(False)
        except:
            pass

        for ur in Owner.all():
            ur.islog = False
            ur.save()
