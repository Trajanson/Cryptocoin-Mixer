# -*- coding: utf-8 -*-
from random import choice
from string import ascii_letters


class CryptocoinAPIHandler(object):
    def __init__(self, jobcoin_api):
        self.jobcoin_api = jobcoin_api

    def send_value(self, fromAddress, toAddress, value):
        self.jobcoin_api.post_transaction(fromAddress, toAddress,
                                          str(value))

    def create_address_with_coins(self, address=None):
        if address is None:
            address = self.select_new_address_name()

        self.jobcoin_api.create_address(address)
        return address

    def select_new_address_name(self):
        return ''.join(choice(ascii_letters) for i in range(10))

    def get_balance_at_address(self, address):
        addressInfo = self.jobcoin_api.get_address_info(address)
        return int(float(addressInfo['balance']))
