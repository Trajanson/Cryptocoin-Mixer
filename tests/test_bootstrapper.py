# -*- coding: utf-8 -*-
"""
    Bootstrapper Tests
    ~~~~~~~~~~~~
    Tests that the Bootstrapper successfully injects coins into the system
    and that empty addresses are reserved for future use
"""

import unittest

from coin_mixer.utils.database_handler import DatabaseHandler
from coin_mixer.constants import HyperParameters
from coin_mixer.utils.mock_cryptocoin_api import MockCryptocoinAPI
from coin_mixer.utils.cryptocoin_api_handler import CryptocoinAPIHandler
from coin_mixer.output_monitor.output_monitor import OutputMonitor

from coin_mixer.bootstrapper import run_bootstrapper

class BootstrapperTestCase(unittest.TestCase):

    def setUp(self):
        self.db = DatabaseHandler(test_db=True)
        self.db.delete_database()
        self.output_monitor = OutputMonitor(self.db)

        coin_interface = CryptocoinAPIHandler(MockCryptocoinAPI())

        run_bootstrapper(coin_interface, self.db, self.output_monitor)

    def test_seed_fund(self):
        expected = HyperParameters.NUM_INJECTION_ADDRESSES * 50

        actual = self.db.total_value_in_ecosystem()
        assert actual == expected

    def test_address_count(self):
        expected = HyperParameters.NUM_INJECTION_ADDRESSES
        expected += HyperParameters.NUM_INITIAL_ADDRESSES

        actual = self.db.total_num_addresses_in_ecosystem()
        assert actual == expected

    # Checks that no exceptions called from within called method
    # for invalid input
    def test_random_addresses_for_valid_fields(self):
        self.db.get_random_ecosystem_addresses(3)

    def tearDown(self):
        self.db.delete_database()


if __name__ == '__main__':
    unittest.main()
