class HyperParameters(object):
    # Average number of addresses that will
    # engage in transactions per epoch
    EXPECTED_PERCENT_OF_ADDRESSES_TO_ENGAGE = 0.20

    # Number of Nodes Used to Inject Currency Into Ecosystem
    # (1000 Jobcoins total)
    NUM_INJECTION_ADDRESSES = 20

    # Number of Empty Addresses Used to Begin Internal Ecosystem
    NUM_INITIAL_ADDRESSES = 50

    NUM_COINS_GIVEN_TO_NEW_ADDRESS = 50


class Constants(object):
    pass


class Config(object):
    TEST_DB_HOST = 'localhost'
    TEST_DB_NUMBER = 6

    PRODUCTION_DB_HOST = 'localhost'
    PRODUCTION_DB_NUMBER = 7
