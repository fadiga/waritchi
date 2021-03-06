#!/usr/bin/env python
# -*- coding: utf8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# maintainer: Fad
from __future__ import (
    unicode_literals, absolute_import, division, print_function)

from PyQt4.QtGui import QStatusBar

from Common.models import Owner
from configuration import Config
from Common.ui.common import (FLabel)
# from ussd import get_solde


class GStatusBar(QStatusBar):

    def __init__(self, parent):

        QStatusBar.__init__(self, parent)

        self.setWindowOpacity(1.50)
        self.compt = 0
        self.timerEvent(self.compt)
        self.startTimer(5000)

    def timerEvent(self, event):
        msg = "Les solde est: {solde}  "
        if self.compt == 0:
            self.showMessage(u"Bienvenue! sur {}. Un outil rapide et facile à "
                             u"utiliser".format(Config.APP_NAME), 14000)
        if self.compt == 1:
            try:
                user = Owner.get(islog=True)
                mss = u"Votez connecté en tant que {user}" \
                      u" et les droits de {group}.".format(user=user.username,
                                                           group=user.group)
            except:
                mss = u"Vos identifiants"
            self.showMessage(mss, 15000)

        if self.compt == 2:
            self.showMessage(u"Seul l'organisation {} est autorisée ce logiciel".format(
                Config.NAME_ORGA), 15000)

        if self.compt > 4:
            self.compt = 0
        self.compt += 1

        try:
            solde = get_solde()
            mgs = u"""Dernier Solde: {cpt_p}  {bonus_SMS}{bonus_orange}
                      """.format(cpt_p=solde[0], bonus_SMS=solde[1],
                                 bonus_orange=solde[2])
        except Exception as e:
            mgs = u"Veuillez branché le modem (cléf 3g)"

        # self.showMessage(mgs, 15000)
