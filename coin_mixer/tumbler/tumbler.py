from coin_mixer.constants import HyperParameters


class Tumbler(object):

    def __init__(self, database):
        self.db = database

    def select_baseline_values(self, num_to_select, for_new_addresses=False):
        total_value_in_ecosystem = self.db.total_value_in_ecosystem()

        num_addresses_in_ecosystem = self.db.total_num_addresses_in_ecosystem()
        if for_new_addresses is True:
            num_addresses_in_ecosystem += num_to_select

        mean = total_value_in_ecosystem / num_addresses_in_ecosystem
        std_dev = HyperParameters.calculate_std_dev_of_baselines(mean)

        return HyperParameters.select_random_baseline_values(mean, std_dev,
                                                             num_to_select)
