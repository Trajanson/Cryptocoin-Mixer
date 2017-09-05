from random import choice
from string import ascii_letters


class Cryptocoin_API_Handler(object):
    def __init__(self, jobcoin_api):
        self.jobcoin_api = jobcoin_api

    def send_value(self, fromAddress, toAddress, value):
        self.jobcoin_api.post_transaction(fromAddress, toAddress,
                                          str(value))

    def create_address_with_coins(self, address=None):
        if address is None:
            address = self.selectNewAddressName()

        self.jobcoin_api.create_address(address)
        return address

    def selectNewAddressName(self):
        return ''.join(choice(ascii_letters) for i in range(10))
