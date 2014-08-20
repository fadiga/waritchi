#!/usr/bin/env python
# -*- coding: utf8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# maintainer: Fad

from __future__ import (unicode_literals, absolute_import, division, print_function)

"""\
Demo: Simple USSD example

Simple demo app that initiates a USSD session, reads the string response and closes the session
(if it wasn't closed by the network)

Note: for this to work, a valid USSD string for your network must be used.
"""
import sys
import glob
import serial

# import logging

from gsmmodem.modem import GsmModem
from models import Transfer, Contact, LocalSetting
from Common.ui.util import normalize

PIN = None # SIM card PIN (if any)
PIN = 0000
try:
    sttg = LocalSetting.get(LocalSetting.slug==1)
    PORT = sttg.port
    BAUDRATE = sttg.baudrate
    USSD_STRING = sttg.code_consultation
except Exception , e:
    print(e)
    pass


def send_ussd(USSD_STRING):
    print('Initializing modem...')
    #logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    modem = GsmModem(PORT, BAUDRATE)
    modem.connect(PIN)
    modem.waitForNetworkCoverage(10)
    print('Sending USSD string: {0}'.format(USSD_STRING))
    response = modem.sendUssd(USSD_STRING) # response type: gsmmodem.modem.Ussd
    print('USSD reply received: {0}'.format(response.message))
    if response.sessionActive:
        print('Closing USSD session.')
        # At this point, you could also reply to the USSD message by using response.reply()
        response.cancel()
    else:
        print('USSD session was ended by network.')
    modem.close()
    return response


def multiple_sender(data):
    """ data = {phone_num: [76027211, 76433890], code: 03944, amount: 100} """
    amount = data.get("amount")
    code = data.get("code")
    for phone_num in data.get("phone_num"):
        transfer = Transfer()
        transfer.amount = amount
        transfer.contact = Contact.get_or_create(phone_num)
        transfer.response = u"{}".format(send_ussd(format_str(phone_num, amount, code)).message)
        transfer.save()


def get_solde():
    # print(send_ussd(USSD_STRING).message)
    try:
        response = send_ussd(USSD_STRING).message
    except UnicodeDecodeError:
        response = "UnicodeDecodeError"
    except Exception , e:
        # raise
        response = "<h4>Veuillez changé le port dans la config </h4>\n{} \n {}".format(normalize(e), serial_ports())
    return response


def format_str(phone_num, amount, code):
    return "#145#1*{amount}*{phone_num}*{code}#".format(code=code, amount=amount,
                                                        phone_num=phone_num)


def serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM' + str(i + 1) for i in range(256)]
    elif sys.platform.startswith('linux'):
        # this is to exclude your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('platform non supportée')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
        except UnicodeDecodeError:
            pass
    print(result)
    return result
