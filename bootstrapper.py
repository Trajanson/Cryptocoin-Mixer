from coin_mixer.constants import HyperParameters

from coin_mixer.utils.mock_cryptocoin_api import MockCryptocoinAPI
from coin_mixer.utils.cryptocoin_api import CryptocoinAPI
from coin_mixer.utils.cryptocoin_api_handler import Cryptocoin_API_Handler
from coin_mixer.utils.database_handler import Database_Handler

IN_TEST = True

if IN_TEST is True:
    cryptocoin_interface = Cryptocoin_API_Handler(MockCryptocoinAPI())
    database_handler = Database_Handler(test_db=True)
else:
    cryptocoin_interface = Cryptocoin_API_Handler(CryptocoinAPI())
    database_handler = Database_Handler(test_db=False)


addresses_with_initial_wealth = []
addresses_in_ecosystem = []

# Create initial address with seed coins
for num_coin_created in range(HyperParameters.NUM_INJECTION_ADDRESSES):
    address = cryptocoin_interface.create_address_with_coins()
    addresses_with_initial_wealth.push(address)

    coins_per_address = HyperParameters.NUM_COINS_GIVEN_TO_NEW_ADDRESS
    database_handler.store_new_decreasing_address(address, coins_per_address)

# Randomly determine addresses to place in eco-system
for num_coin in range(HyperParameters.NUM_INITIAL_ADDRESSES):
    address_to_create = cryptocoin_interface
    addresses_in_ecosystem.push(address_to_create)

    database_handler.store_new_address(address, 0)
