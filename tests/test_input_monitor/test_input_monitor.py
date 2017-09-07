# -*- coding: utf-8 -*-
"""
    Input Monitor Tests
    ~~~~~~~~~~~~
    Tests the Input Monitor
"""

import unittest

from coin_mixer.constants import HyperParameters
from coin_mixer.utils.database_handler import DatabaseHandler
from coin_mixer.bootstrapper import run_bootstrapper
from coin_mixer.input_monitor.input_monitor import InputMonitor
from coin_mixer.output_monitor.output_monitor import OutputMonitor
from coin_mixer.utils.cryptocoin_api_handler import CryptocoinAPIHandler
from coin_mixer.tumbler.tumbler import Tumbler
from coin_mixer.utils.mock_cryptocoin_api import MockCryptocoinAPI
from coin_mixer.transaction_engine.transaction_engine import TransactionEngine


class InputMonitorTestCase(unittest.TestCase):

    def setUp(self):
        self.db = DatabaseHandler(test_db=True)
        self.db.delete_database()

        self.coin_interface = CryptocoinAPIHandler(MockCryptocoinAPI())
        self.output_monitor = OutputMonitor(self.db)
        self.transaction_engine = TransactionEngine(self.db,
                                                    self.coin_interface,
                                                    self.output_monitor)
        self.tumbler = Tumbler(self.db, self.transaction_engine,
                               self.coin_interface)

        self.input_monitor = InputMonitor(self.db, self.coin_interface,
                                           self.tumbler)

        run_bootstrapper(self.coin_interface, self.db, self.output_monitor)

    def test_input_monitor_does_not_pulls_coins_into_system(self):
        input_address = "FnUXvRSPtM"
        self.coin_interface.create_address_with_coins(input_address)
        target_goal = 1000

        self.input_monitor.add_target(input_address, target_goal)
        self.input_monitor.check_inputs()

        actual = self.db.total_value_in_ecosystem()
        expected = (HyperParameters.NUM_INJECTION_ADDRESSES * 50)

        assert actual == expected

        expected = HyperParameters.NUM_INJECTION_ADDRESSES
        expected += HyperParameters.NUM_INITIAL_ADDRESSES

        actual = self.db.total_num_addresses_in_ecosystem()

        assert actual == expected

    def test_input_monitor_pulls_coins_into_system(self):
        input_address = "qFrcRSIgOp"
        self.coin_interface.create_address_with_coins(input_address)
        target_goal = 20

        self.input_monitor.add_target(input_address, target_goal)
        self.input_monitor.check_inputs()

        actual = self.db.total_value_in_ecosystem()
        expected = (HyperParameters.NUM_INJECTION_ADDRESSES * 50) + target_goal

        assert actual == expected

        expected = HyperParameters.NUM_INJECTION_ADDRESSES
        expected += HyperParameters.NUM_INITIAL_ADDRESSES
        expected += 1

        actual = self.db.total_num_addresses_in_ecosystem()

        assert actual == expected

    def tearDown(self):
        self.db.delete_database()


if __name__ == '__main__':
    unittest.main()
