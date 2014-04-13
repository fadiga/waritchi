#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Fadiga


from PyQt4 import QtGui, QtCore

from models import Contact, Transfer, ContactGroup, Group, PhoneNumber

from Common.ui.common import F_Widget, F_BoxTitle
from Common.ui.table import F_TableWidget
from addgroup import GroupViewWidget

ALL_CONTACTS = -1


class ContactViewWidget(F_Widget):
    """ Shows the home page  """

    def __init__(self, parent=0, *args, **kwargs):
        super(ContactViewWidget, self).__init__(parent=parent,
                                                        *args, **kwargs)
        self.parent = parent
        self.parentWidget().setWindowTitle(u"Carnet d'adresse")

        hbox = QtGui.QHBoxLayout(self)

        self.table_contact = ContactTableWidget(parent=self)
        self.table_info = InfoTableWidget(parent=self)
        self.table_group = GroupTableWidget(parent=self)
        self.table_transf = TransfTableWidget(parent=self)
        self.operation = OperationWidget(parent=self)

        splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)

        self.splitter_left = QtGui.QSplitter(QtCore.Qt.Vertical)

        self.splitter_left.addWidget(F_BoxTitle(u"Les groupes"))
        self.splitter_left.addWidget(self.table_group)

        splitter_details = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter_details.addWidget(self.table_info)

        splitter_down = QtGui.QSplitter(QtCore.Qt.Vertical)
        splitter_down.addWidget(self.operation)

        splitter_transf = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter_transf.addWidget(self.table_transf)

        splt_contact = QtGui.QSplitter(QtCore.Qt.Vertical)
        splt_contact.addWidget(F_BoxTitle(u"Les contactes"))
        splt_contact.addWidget(self.table_contact)
        splt_contact.resize(900, 1000)

        self.splitter_left.addWidget(splitter_down)
        splitter_details.addWidget(splitter_transf)
        splt_contact.addWidget(splitter_details)
        splitter.addWidget(self.splitter_left)
        splitter.addWidget(splt_contact)

        hbox.addWidget(splitter)
        self.setLayout(hbox)


class OperationWidget(F_Widget):
    """docstring for OperationWidget"""

    def __init__(self, parent, *args, **kwargs):
        F_Widget.__init__(self, parent=parent, *args, **kwargs)

        vbox = QtGui.QVBoxLayout()
        editbox = QtGui.QGridLayout()
        self.parent = parent

        self.search_field = QtGui.QLineEdit()
        self.search_field.textChanged.connect(self.finder)
        self.search_field.setToolTip(u"Taper le nom ou le numéro de "
                                     u"téléphone à chercher")
        self.empty = QtGui.QLabel(u"")
        editbox.addWidget(self.search_field, 0, 0)

        bicon = QtGui.QIcon.fromTheme('search', QtGui.QIcon(''))
        search_but = QtGui.QPushButton(bicon, u"")
        search_but.clicked.connect(self.search)
        editbox.addWidget(search_but, 0, 1)
        editbox.addWidget(self.empty, 1, 0)

        bicon = QtGui.QIcon.fromTheme('document-new', QtGui.QIcon(''))
        addgroup_but = QtGui.QPushButton(bicon, u"Nouveau groupe")
        addgroup_but.clicked.connect(self.addgroup)

        editbox.addWidget(addgroup_but, 2, 0)

        vbox.addLayout(editbox)
        self.setLayout(vbox)

    def finder(self):
        completion_values = []
        search_term = self.search_field.text()
        try:
            contacts = PhoneNumber.filter(number__icontains=int(search_term))
        except ValueError:
            contacts = Contact.filter(name__icontains=search_term)

        for contact in contacts:
            completion_values.append(contact.__unicode__())
        completer = QtGui.QCompleter(completion_values, parent=self)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        completer.setCompletionMode(QtGui.QCompleter.UnfilteredPopupCompletion)

        self.search_field.setCompleter(completer)

    def search(self):

        value = self.search_field.text()
        self.empty.setStyleSheet("")
        self.empty.setText(u"")
        contacts = []

        try:
            contacts = PhoneNumber.filter(number__icontains=int(value))
        except ValueError:
            contacts = PhoneNumber.filter(contact__name__icontains=value)
            pass

        try:
            value = contacts.get()
            self.parent.table_contact.refresh_(search=value)
            self.search_field.clear()
        except AttributeError:
            pass
        except:
            self.empty.setStyleSheet("font-size:20px; color: red")
            self.empty.setText(u"%s n'existe pas" % value)

    def addgroup(self):
        """ Affiche un QDialog qui permet d'ajouter un nouveau groupe """
        try:
            self.parent.open_dialog(GroupViewWidget, modal=True,
                                                      table_group=self.parent)
        except:
            raise


class GroupTableWidget(QtGui.QListWidget):
    """affiche tout le nom de tous les groupes"""

    def __init__(self, parent, *args, **kwargs):
        super(GroupTableWidget, self).__init__(parent)
        self.parent = parent
        self.setAutoScroll(True)
        self.setAutoFillBackground(True)
        self.itemSelectionChanged.connect(self.handleClicked)
        self.refresh_()

    def refresh_(self):
        """ Rafraichir la liste des groupes"""
        self.clear()
        self.addItem(GroupQListWidgetItem(ALL_CONTACTS))
        for group in Group.filter():
            self.addItem(GroupQListWidgetItem(group))

    def handleClicked(self):
        group = self.currentItem()
        self.parent.table_contact.refresh_(group_id=group.group_id)


class GroupQListWidgetItem(QtGui.QListWidgetItem):

    def __init__(self, group):
        super(GroupQListWidgetItem, self).__init__()

        self.group = group

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/group.png"),
                                      QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setIcon(icon)
        self.init_text()

    def init_text(self):
        try:
            self.setText(self.group.name)
        except AttributeError:
            font = QtGui.QFont()
            font.setBold(True)
            self.setFont(font)
            self.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
            self.setText(u"Tous")

    @property
    def group_id(self):
        try:
            return self.group.id
        except AttributeError:
            return self.group


class ContactTableWidget(F_TableWidget):
    """ Reçoit un groupe et affiche ses contactes et affiche tous les
        contactes par defaut"""

    def __init__(self, parent, *args, **kwargs):
        F_TableWidget.__init__(self, parent=parent, *args, **kwargs)

        self.parent = parent

        self.header = [u'', u"Nom"]
        self.max_width = 500

        self.set_data_for()
        self.refresh(True)

    def refresh_(self, group_id=None, search=None):
        self._reset()
        self.set_data_for(group_id=group_id, search=search)
        self.refresh(True)

    def set_data_for(self, group_id=None, search=None):

        if search:
            self.data = [("", tel.contact.name)
                          for tel in PhoneNumber.filter().group_by('contact')
                                            if search.contact == tel.contact]
        else:
            self.data = [("", contact.name) for contact in Contact.all()]

        if group_id:
            if group_id == ALL_CONTACTS:
                qs = ContactGroup.filter().group_by('contact')
            else:
                qs = ContactGroup.filter(group__id=group_id)
            self.data = [("", contact_gp.contact.name) for contact_gp in qs]

    def _item_for_data(self, row, column, data, context=None):
        if column == 0:
            return QtGui.QTableWidgetItem(QtGui.QIcon("images/info.png"), "")
        return super(ContactTableWidget, self)._item_for_data(row, column,
                                                               data, context)

    def click_item(self, row, column, *args):

        number = PhoneNumber.filter(contact__name=self.data[row][1]).get()
        self.parent.table_info.refresh_(number)
        self.parent.table_transf.refresh_(number)


class InfoTableWidget(F_TableWidget):

    def __init__(self, parent=0, *args, **kwargs):
        super(InfoTableWidget, self).__init__(parent=parent, *args, **kwargs)
        self.parent = parent
        self.max_width = 400

        self.header = [u"Nom", u"Telephone"]

    def refresh_(self, number):
        self._reset()
        self.set_data_for(number)
        self.refresh(True)

    def set_data_for(self, number):
        self.data = [(tel.contact.name, tel.number)
                      for tel in PhoneNumber.all()
                                            if number.contact == tel.contact]


class TransfTableWidget(F_TableWidget):
    """ Reçoit un numero de telephone et Affiche dans un tableau tout
       les transfers effectué par ce numero """

    def __init__(self, parent, *args, **kwargs):
        F_TableWidget.__init__(self, parent=parent, *args, **kwargs)

        self.max_width = 400

        self.header = [u"Numero", u"Date du transfert", u"Montant(FCFA)"]
        self.set_data_for("")
        self.refresh(True)

    def refresh_(self, number):
        self._reset()
        self.set_data_for(number)
        self.refresh(True)

    def set_data_for(self, number):

        try:
            self.data = [(transf.number,
                          transf.date.strftime(u"%d/%m/%Y a %Hh:%Mmn"),
                          transf.amount) for transf in Transfer.all()\
                           if transf.number.contact == number.contact]
        except AttributeError:
            pass
