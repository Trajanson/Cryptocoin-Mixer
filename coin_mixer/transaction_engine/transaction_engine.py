# -*- coding: utf-8 -*-
import time
import numpy as np

from coin_mixer.constants import HyperParameters
from coin_mixer.transaction_engine.strategy import TransactionStrategy


class TransactionEngine(object):
    def __init__(self, database, cryptocoin_handler, output_monitor):
        self.db = database
        self.cryptocoin_handler = cryptocoin_handler
        self.transaction_strategy = TransactionStrategy()
        self.output_monitor = output_monitor

        """
        TRANSACTION STRUCTURE:
            {'first_address': Address,
             'second_address': Address,
             'timestamp': timestamp
            }
        """
        self.upcoming_transactions = []

    def add(self, first_address, second_address, execution_time=None):
        """
        :type first_address: Address
        :type second_address: Address
        :rtype: None
        """
        if execution_time is None:
            execution_time = self.__get_transaction_execution_time()
        transaction = self.__form_transaction(first_address, second_address,
                                              execution_time)
        self.__insert_transaction_to_queue(transaction)

    def execute_pending_transactions(self):
        upcoming_transactions = self.__get_upcoming_transactions()
        time_now = time.time()

        num_to_process = 0
        while (num_to_process < len(upcoming_transactions) and
               upcoming_transactions[num_to_process]['timestamp'] <= time_now):
            num_to_process += 1

        pending_transactions = upcoming_transactions[:num_to_process]
        self.__remove_num_transactions_from_queue(num_to_process)

        for transaction in pending_transactions:
            self.__execute_transaction(transaction)

    def __execute_transaction(self, transaction):
        """
        :type transaction: {TRANSACTION} - see above
        :rtype: None
        """
        first_address_old_data = transaction['first_address']
        second_address_old_data = transaction['second_address']

        first_address_name = first_address_old_data.address
        second_address_name = second_address_old_data.address

        first_address_data = self.db.get_address_data_if_exists(
            first_address_name)
        second_address_data = self.db.get_address_data_if_exists(
            second_address_name)

        if first_address_data is None or second_address_data is None:
            return None

        address_has_been_removed = False
        if first_address_data.should_be_removed_from_ecosystem():
            self.__remove_address_from_ecosystem(first_address_name)
            address_has_been_removed = True
        if second_address_data.should_be_removed_from_ecosystem():
            self.__remove_address_from_ecosystem(second_address_name)
            address_has_been_removed = True

        if address_has_been_removed is False:
            transfer = self.transaction_strategy.determine_transfer(
                first_address_data, second_address_data)
            if transfer is not None:
                print("transfer: (sender, receiver, transfer_value)")
                print("transfer", transfer)
                self.__execute_transfer(transfer)

    def __execute_transfer(self, transfer):
        sender, receiver, transfer_value = transfer
        self.__notify_database_of_transfer(sender, receiver, transfer_value)
        self.__notify_cryptocoin_handler_of_transfer(sender, receiver,
                                                     transfer_value)

    def __notify_database_of_transfer(self, sender, receiver,
                                      transfer_value):
        self.db.increment_value_at_address(receiver, transfer_value)
        self.db.increment_value_at_address(sender, -1 * transfer_value)

        receiver_address_data = self.db.get_address_data(receiver)
        if (receiver_address_data.isForClientOutput):
            self.db.mark_address_as_compromised(sender)

            if receiver_address_data.is_at_max_value():
                self.output_monitor.release_address(receiver)

    def __notify_cryptocoin_handler_of_transfer(self, sender, receiver,
                                                transfer_value):
        self.cryptocoin_handler.send_value(sender, receiver, transfer_value)

    def __form_transaction(self, first_address, second_address, timestamp):
        return {'first_address': first_address,
                'second_address': second_address,
                'timestamp': timestamp}

    def __get_transaction_execution_time(self):
        current_time = time.time()
        tumbler_epoch = HyperParameters.TUMBLER_EPOCH_LENGTH
        time_until_execution = np.random.random() * tumbler_epoch

        return current_time + time_until_execution

    def __get_upcoming_transactions(self):
        return self.upcoming_transactions

    def __insert_transaction_to_queue(self, transaction):
        self.upcoming_transactions.append(transaction)
        self.upcoming_transactions = (
            sorted(self.upcoming_transactions,
                   key=lambda transaction: int(transaction['timestamp'])))
        return self.upcoming_transactions

    def __remove_num_transactions_from_queue(self, num):
        self.upcoming_transactions = self.upcoming_transactions[num:]

    def __remove_address_from_ecosystem(self, address):
        self.db.remove_address_from_ecosystem(address)
