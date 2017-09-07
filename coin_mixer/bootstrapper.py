# -*- coding: utf-8 -*-
from coin_mixer.constants import HyperParameters
from coin_mixer.utils.cryptocoin_api import CryptocoinAPI
from coin_mixer.utils.cryptocoin_api_handler import CryptocoinAPIHandler
from coin_mixer.utils.database_handler import DatabaseHandler
from coin_mixer.tumbler.tumbler import Tumbler
from coin_mixer.transaction_engine.transaction_engine import TransactionEngine
from coin_mixer.output_monitor.output_monitor import OutputMonitor


def run_bootstrapper(coin_interface, database, output_monitor):
    create_seed_fund_addresses(coin_interface, database, output_monitor)
    create_initial_ecosystem_addresses(coin_interface, database,
                                       output_monitor)


def create_seed_fund_addresses(coin_interface, database, output_monitor):
    seed_fund_addresses = []
    for num_coin_created in range(HyperParameters.NUM_INJECTION_ADDRESSES):
        address = coin_interface.create_address_with_coins()
        seed_fund_addresses.append(address)

        coins_per_address = HyperParameters.NUM_COINS_GIVEN_TO_NEW_ADDRESS
        baseline_value = 0
        database.store_new_decreasing_address(address, baseline_value,
                                              coins_per_address)


def create_initial_ecosystem_addresses(coin_interface, database,
                                       output_monitor):
    transaction_engine = TransactionEngine(database, coin_interface,
                                           output_monitor)
    tumbler = Tumbler(database, transaction_engine, coin_interface)
    num_create = HyperParameters.NUM_INITIAL_ADDRESSES

    baseline_values = tumbler.select_baseline_values(num_create, True)

    for baseline_value in baseline_values:
        address = coin_interface.create_address_with_coins()

        database.store_new_address(address, baseline_value, 0)


if __name__ == '__main__':
    coin_interface = CryptocoinAPIHandler(CryptocoinAPI())
    database = DatabaseHandler(test_db=False)
    output_monitor = OutputMonitor(database)

    run_bootstrapper(coin_interface, database, output_monitor)
