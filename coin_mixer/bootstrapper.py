# -*- coding: utf-8 -*-
from coin_mixer.constants import HyperParameters
from coin_mixer.utils.cryptocoin_api import CryptocoinAPI
from coin_mixer.utils.cryptocoin_api_handler import CryptocoinAPIHandler
from coin_mixer.utils.database_handler import Database_Handler
from coin_mixer.tumbler.tumbler import Tumbler
from coin_mixer.transaction_engine.transaction_engine import TransactionEngine


def run_bootstrapper(coin_interface, database):
    create_seed_fund_addresses(coin_interface, database)
    create_initial_ecosystem_addresses(coin_interface, database)


def create_seed_fund_addresses(coin_interface, database):
    seed_fund_addresses = []
    for num_coin_created in range(HyperParameters.NUM_INJECTION_ADDRESSES):
        address = coin_interface.create_address_with_coins()
        seed_fund_addresses.append(address)

        coins_per_address = HyperParameters.NUM_COINS_GIVEN_TO_NEW_ADDRESS
        baseline_value = 0
        database.store_new_decreasing_address(address, baseline_value,
                                              coins_per_address)


def create_initial_ecosystem_addresses(coin_interface, database):
    tumbler = Tumbler(database, TransactionEngine(database))
    num_create = HyperParameters.NUM_INITIAL_ADDRESSES

    baseline_values = tumbler.select_baseline_values(num_create, True)

    for baseline_value in baseline_values:
        address = coin_interface.create_address_with_coins()

        database.store_new_address(address, baseline_value, 0)


if __name__ == '__main__':
    coin_interface = CryptocoinAPIHandler(CryptocoinAPI())
    database = Database_Handler(test_db=False)

    run_bootstrapper(coin_interface, database)
