# -*- coding: utf-8 -*-
import requests


class CryptocoinAPI():
    def get_address_info(self, address):
        url = "http://jobcoin.gemini.com/undecided/api/addresses/"
        url += address
        cryptocoin_response = requests.get(url).json()
        return cryptocoin_response

    def create_address(self, address):
        url = "https://jobcoin.gemini.com/undecided/create"
        data = {'address': address}

        cryptocoin_response = requests.post(url, data).json()
        return cryptocoin_response

    def get_transactions(self):
        url = "http://jobcoin.gemini.com/undecided/api/transactions"
        cryptocoin_response = requests.get(url).json()
        return cryptocoin_response

    def post_transaction(self, fromAddress, toAddress, amount):
        url = "http://jobcoin.gemini.com/undecided/api/transactions"
        data = {'fromAddress': fromAddress,
                'toAddress': toAddress,
                'amount': amount}

        cryptocoin_response = requests.post(url, data).json()
        return cryptocoin_response
