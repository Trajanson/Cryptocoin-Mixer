# -*- coding: utf-8 -*-
import numpy as np


class TransactionStrategy(object):

    @staticmethod
    def determine_transfer(first_address_data,
                           second_address_data):
        if TransactionStrategy.__is_illegal_transaction(first_address_data,
                                                        second_address_data):
            transfer_value = 0
        else:
            transfer_value = TransactionStrategy.__select_transfer(
                first_address_data, second_address_data)

        return TransactionStrategy.__organize_transfer(first_address_data,
                                                       second_address_data,
                                                       transfer_value)

    @staticmethod
    def __select_transfer(first_address_data, second_address_data):
        transfer_range = TransactionStrategy.__get_range_of_transfer_values(
            first_address_data, second_address_data)

        selection = int(np.random.choice(transfer_range, 1, replace=False)[0])
        return selection

    @staticmethod
    def __is_illegal_transaction(first_address_data, second_address_data):
        if (first_address_data.isOnlyDecreasing and
                second_address_data.isOnlyDecreasing):
            return True
        elif (first_address_data.isOnlyIncreasing and
                second_address_data.isOnlyIncreasing):
            return True
        elif (first_address_data.balance == 0 and
                second_address_data.balance == 0):
            return True
        elif (first_address_data.hasBeenCompromised and
                second_address_data.isForClientOutput):
            return True
        elif (first_address_data.isForClientOutput and
                second_address_data.hasBeenCompromised):
            return True
        else:
            return False

    def __get_range_of_transfer_values(first_address_data,
                                       second_address_data):
        """
        :type first_address_data: Address
        :type second_address_data: Address
        :rtype: [int]
        """
        first_address_max_payout = first_address_data.balance
        second_address_max_payout = second_address_data.balance

        if first_address_data.isOnlyIncreasing:
            first_address_max_payout = 0
        if second_address_data.isOnlyIncreasing:
            second_address_max_payout = 0

        if first_address_data.maxValue < float("inf"):
            first_address_max_accept = (int(first_address_data.maxValue) -
                                        first_address_data.balance)
            second_address_max_payout = min(second_address_max_payout,
                                            first_address_max_accept)

        if second_address_data.maxValue < float("inf"):
            second_address_max_accept = (int(second_address_data.maxValue) -
                                         second_address_data.balance)
            first_address_max_payout = min(first_address_max_payout,
                                           second_address_max_accept)

        rnge = range(-1*first_address_max_payout, second_address_max_payout+1)
        return list(rnge)

    @staticmethod
    def __organize_transfer(first_address_data, second_address_data,
                            transfer_value):
        """
        :type first_address_data: Address
        :type second_address_data: Address
        :type transfer_value: int
        :rtype: Maybe[(sender: string, receiver: string, transfer_value: int)]
         """
        first_address_name = first_address_data.address
        second_address_name = second_address_data.address
        if transfer_value < 0:
            return (first_address_name, second_address_name,
                    abs(transfer_value))
        elif transfer_value == 0:
            return None
        if transfer_value > 0:
            return (second_address_name, first_address_name, transfer_value)
