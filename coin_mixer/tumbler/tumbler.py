# -*- coding: utf-8 -*-
import numpy as np

from coin_mixer.constants import HyperParameters


class Tumbler(object):

    def __init__(self, database, transaction_engine, cryptocoin_handler):
        self.db = database
        self.transaction_engine = transaction_engine
        self.cryptocoin_handler = cryptocoin_handler

    def operate(self):
        self.__generate_transactions()

    def select_baseline_values(self, num_to_select, for_new_addresses=False):
        total_value_in_ecosystem = self.db.total_value_in_ecosystem()

        num_addresses_in_ecosystem = self.db.total_num_addresses_in_ecosystem()
        if for_new_addresses is True:
            num_addresses_in_ecosystem += num_to_select

        mean = total_value_in_ecosystem / num_addresses_in_ecosystem
        std_dev = HyperParameters.calculate_std_dev_of_baselines(mean)

        return HyperParameters.select_random_baseline_values(mean, std_dev,
                                                             num_to_select)

    def __pull_addresses_into_ecosystem(self):
        num_addresses_in_ecosystem = self.db.total_num_addresses_in_ecosystem()
        num_compromised = (
            self.db.total_num_compromised_addresses_in_ecosystem())
        num_client_output = (
            self.db.total_num_client_output_addresses_in_ecosystem())

        num_fully_active_addresses = (num_addresses_in_ecosystem -
                                      num_compromised - num_client_output)

        node_multiplier = (1.0 * num_fully_active_addresses /
                           HyperParameters.NUM_INITIAL_ADDRESSES)

        probability_of_increase = (1 - (1 / (1 + np.exp(-node_multiplier))))

        if num_fully_active_addresses < HyperParameters.NUM_INITIAL_ADDRESSES:
            self.__pull_address_into_ecosystem()
        elif probability_of_increase > np.random.random(1)[0]:
            self.__pull_address_into_ecosystem()

    def __pull_address_into_ecosystem(self):
        self.cryptocoin_handler.selectNewAddressName()


    def __generate_transactions(self):
        transacting_addresses = self.__generate_transaction_addresses()
        np.random.shuffle(transacting_addresses)

        zipList = zip(*[iter(transacting_addresses)]*2)
        for firstAddress, secondAddress in zipList:
            self.transaction_engine.add(firstAddress, secondAddress)

    def __generate_transaction_addresses(self):
        num_addresses_in_ecosystem = self.db.total_num_addresses_in_ecosystem()

        pct = HyperParameters.PERCENT_OF_ECOSYSTEM_TRANSACTING_PER_EPOCH
        num_transacting = (int((pct/100.) * num_addresses_in_ecosystem) // 2)*2

        return self.db.get_random_ecosystem_addresses(num_transacting)
