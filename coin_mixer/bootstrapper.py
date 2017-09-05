from coin_mixer.constants import HyperParameters

from coin_mixer.utils.mock_cryptocoin_api import MockCryptocoinAPI
from coin_mixer.utils.cryptocoin_api import CryptocoinAPI
from coin_mixer.utils.cryptocoin_api_handler import Cryptocoin_API_Handler
from coin_mixer.utils.database_handler import Database_Handler


def run_bootstrapper(in_test=True):
    if in_test is True:
        coin_interface = Cryptocoin_API_Handler(MockCryptocoinAPI())
        database = Database_Handler(test_db=True)
    else:
        coin_interface = Cryptocoin_API_Handler(CryptocoinAPI())
        database = Database_Handler(test_db=False)

    create_seed_fund_addresses(coin_interface, database)
    # create_initial_ecosystem_addresses(coin_interface, database)


def create_seed_fund_addresses(coin_interface, database):
    seed_fund_addresses = []
    for num_coin_created in range(HyperParameters.NUM_INJECTION_ADDRESSES):
        address = coin_interface.create_address_with_coins()
        seed_fund_addresses.append(address)

        coins_per_address = HyperParameters.NUM_COINS_GIVEN_TO_NEW_ADDRESS
        database.store_new_decreasing_address(address, coins_per_address)


def create_initial_ecosystem_addresses(coin_interface, database):
    initial_ecosystem_addresses = []

    for num_coin in range(HyperParameters.NUM_INITIAL_ADDRESSES):
        address = coin_interface
        initial_ecosystem_addresses.append(address)

        database.store_new_address(address, 0)


if __name__ == '__main__':
    run_bootstrapper(in_test=False)
