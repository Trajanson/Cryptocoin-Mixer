import time


class MockCryptocoinAPI(object):
    def __init__(self):
        self.addresses = {}
        self.transactions = []

    def create_address(self, address):
        if address in self.addresses:
            return {"error": "Address already exists"}
        else:
            new_transaction = {"timestamp": self.__getTimestamp(),
                               "toAddress": address,
                               "amount": "50"}
            self.transactions.append(new_transaction)
            self.addresses[address] = {
                "balance": "50",
                "transactions": [new_transaction]
                }

    def get_transactions(self):
        return self.transactions

    def get_address_info(self, address):
        if address not in self.addresses:
            return {'balance': '0', 'transactions': []}
        else:
            return self.addresses[address]

    def post_transaction(self, fromAddress, toAddress, amount):
        """
        :type fromAddress: str
        :type toAddress: str
        :type amount: str
        :rtype: {str: str}
        """
        if amount <= 0:
            return {"error": "AMOUNT MUST BE OVER 0"}

        elif fromAddress == "" or toAddress == "":
            error = {}
            if fromAddress == "":
                error['fromAddress'] = ['This field is required']
            if toAddress == "":
                error['toAddress'] = ['This field is required']
            return {'error': error}

        elif fromAddress not in self.addresses:
            name = fromAddress
            error = f"{name} has no jobcoins!  Is it a new or unused address?"
            return {"error": error}
        else:
            fromAddressBalance = float(self.addresses[fromAddress]["balance"])

            if fromAddressBalance - float(amount) <= 0:
                num_coins = self.addresses[fromAddress]["balance"]
                error = f'{fromAddress} only has {num_coins} jobcoins!'
                return {'error': error}

            else:
                self.__transfer_coins(fromAddress, toAddress, amount)
                return {"status": "OK"}

    def __transfer_coins(self, fromAddress, toAddress, amount):
        """
        :type fromAddress: str
        :type toAddress: str
        :type amount: str
        :rtype: None
        """
        new_transaction = {"timestamp": self.__getTimestamp(),
                           "fromAddress": fromAddress,
                           "toAddress": toAddress,
                           "amount": amount}

        self.transactions.append(new_transaction)

        self.__add_transaction_to_address(new_transaction, fromAddress, False)
        self.__add_transaction_to_address(new_transaction, toAddress, True)

    def __add_transaction_to_address(self, transaction, address, is_receiving):
        if address not in self.addresses:
            self.addresses[address] = {'balance': '0', 'transactions': []}

        address_info = self.addresses[address]

        old_balance = float(address_info["balance"])

        value_received = float(transaction["amount"])
        if is_receiving is False:
            value_received *= -1

        address_info["balance"] = str(old_balance + value_received)

        address_info["transactions"].append(transaction)

    # UNIX Timestamp
    def __getTimestamp(self):
        return time.time()
