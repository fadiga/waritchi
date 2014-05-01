#!/usr/bin/env python
# -*- coding: utf8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# maintainer: Fad
from __future__ import (unicode_literals, absolute_import, division, print_function)

import os, sys; sys.path.append(os.path.abspath('../'))
import locale
import gettext, gettext_windows

from PyQt4.QtGui import QApplication, QDialog

from database import setup
from configuration import Config

from Common.ui.window import F_Window
from Common.ui.login import LoginWidget, john_doe
from ui.mainwindow import MainWindow


app = QApplication(sys.argv)

def main():

    gettext_windows.setup_env()
    locale.setlocale(locale.LC_ALL, '')
    gettext.install('main_mb', localedir='locale', unicode=True)
    window = MainWindow()
    setattr(F_Window, 'window', window)
    window.show()
    # window.showMaximized()
    sys.exit(app.exec_())

if __name__ == '__main__':
    setup()

    from models import SettingsAdmin
    if (not Config.LOGIN and
        SettingsAdmin().get(SettingsAdmin.id==1).can_use()):
        john_doe()
        main()
    elif LoginWidget().exec_() == QDialog.Accepted:
        main()
self.emit(MYSIGNAL, "jacek")