import numpy as np

from coin_mixer.constants import HyperParameters


class Tumbler(object):

    def __init__(self, database, transaction_engine):
        self.db = database
        self.transaction_engine = transaction_engine

    def generate_transactions(self):
        transacting_addresses = self.generate_transaction_addresses()
        np.random.shuffle(transacting_addresses)

        zipList = zip(*[iter(transacting_addresses)]*2)
        for firstAddress, secondAddress in zipList:
            self.transaction_engine.add(firstAddress, secondAddress)

    def select_baseline_values(self, num_to_select, for_new_addresses=False):
        total_value_in_ecosystem = self.db.total_value_in_ecosystem()

        num_addresses_in_ecosystem = self.db.total_num_addresses_in_ecosystem()
        if for_new_addresses is True:
            num_addresses_in_ecosystem += num_to_select

        mean = total_value_in_ecosystem / num_addresses_in_ecosystem
        std_dev = HyperParameters.calculate_std_dev_of_baselines(mean)

        return HyperParameters.select_random_baseline_values(mean, std_dev,
                                                             num_to_select)

    def generate_transaction_addresses(self):
        num_addresses_in_ecosystem = self.db.total_num_addresses_in_ecosystem()

        pct = HyperParameters.PERCENT_OF_ECOSYSTEM_TRANSACTING_PER_EPOCH
        num_transacting = (int((pct/100.) * num_addresses_in_ecosystem) // 2)*2

        return self.db.get_random_ecosystem_addresses(num_transacting)
