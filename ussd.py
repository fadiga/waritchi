#!/usr/bin/env python

"""\
Demo: Simple USSD example

Simple demo app that initiates a USSD session, reads the string response and closes the session
(if it wasn't closed by the network)

Note: for this to work, a valid USSD string for your network must be used.
"""

from __future__ import print_function

import logging

from gsmmodem.modem import GsmModem
from models import Transfer, Contact

USSD_STRING = '#123#'
PIN = None # SIM card PIN (if any)

try:
    from models import LocalSetting
    sttg = LocalSetting.get()
    PORT = sttg.port
    BAUDRATE = sttg.baudrate
except:
    pass


def send_ussd(USSD_STRING):
    #logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    modem = GsmModem(PORT, BAUDRATE)
    modem.connect(PIN)
    modem.waitForNetworkCoverage(10)
    response = modem.sendUssd(USSD_STRING)
    # print('USSD reply received: {0}'.format(response.message))
    if response.sessionActive:
        # print('Closing USSD session.')
        response.cancel()
    else:
        pass
    modem.close()
    return response


def multiple_sender(data):
    """ data = {phone_num: [76027211, 76433890], code: 03944, amount: 100} """
    amount = data.get("amount")
    code = data.get("code")
    for phone_num in data.get("phone_num"):
        print("send for {}".format(phone_num))
        transfer = Transfer()
        transfer.amount = amount
        transfer.contact = Contact.get_or_create(phone_num)
        transfer.response = send_ussd(format_str(phone_num, amount, code)).message
        transfer.save()


def get_solde():
    return send_ussd(USSD_STRING).message.splitlines()[:-1]


def format_str(phone_num, amount, code):
    return "#144#1*{amount}*{phone_num}*{code}#".format(code=code, amount=amount,
                                                       phone_num=phone_num)
