# -*- coding: utf-8 -*-
import numpy as np


class HyperParameters(object):
    # Average number of addresses that will
    # engage in transactions per epoch
    EXPECTED_PERCENT_OF_ADDRESSES_TO_ENGAGE = 0.20

    # Number of Nodes Used to Inject Currency Into Ecosystem
    # (2000 Jobcoins total)
    NUM_INJECTION_ADDRESSES = 40

    # Number of Empty Addresses Used to Begin Internal Ecosystem
    NUM_INITIAL_ADDRESSES = 100

    NUM_COINS_GIVEN_TO_NEW_ADDRESS = 50

    PERCENT_OF_ECOSYSTEM_TRANSACTING_PER_EPOCH = 30

    # In Seconds
    TUMBLER_EPOCH_LENGTH = 3

    # In Seconds
    TRANSACTION_ENGINE_EPOCH_LENGTH = 1

    """
    FUNCTIONS FOR DEFINING POPULATION PARAMETERS
    """

    @staticmethod
    def select_random_baseline_values(mean, std_dev, size):
        values = np.random.normal(loc=mean, scale=std_dev, size=size)
        return list(map(lambda value: max(value, 0), values))

    @staticmethod
    def calculate_std_dev_of_baselines(mean):
        return HyperParameters.calculate_std_dev_of_baselines_alg1(mean)

    @staticmethod
    def calculate_std_dev_of_baselines_alg1(mean):
        return (mean - 0) / 4


class Constants(object):
    pass


class Config(object):
    TEST_DB_HOST = 'localhost'
    TEST_DB_NUMBER = 6

    PRODUCTION_DB_HOST = 'localhost'
    PRODUCTION_DB_NUMBER = 7
