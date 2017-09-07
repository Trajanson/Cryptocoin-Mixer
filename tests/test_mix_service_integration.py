# -*- coding: utf-8 -*-
"""
    Mix Service Integration Tests
    ~~~~~~~~~~~~
    Tests that the Mix Services Operate Together As Intended
"""

import time
import unittest

from coin_mixer.bootstrapper import run_bootstrapper
from coin_mixer.constants import HyperParameters
from coin_mixer.integrated_mix_service import MixService


class MixServiceIntegrationTestCase(unittest.TestCase):

    def setUp(self):
        self.mix_service = MixService(in_test=True)

        self.mix_service.db.delete_database()

        run_bootstrapper(self.mix_service.coin_interface, self.mix_service.db,
                         self.mix_service.output_monitor)

    def test_transaction_engine_adds_to_queue(self):
        transaction_engine = self.mix_service.transaction_engine
        db = self.mix_service.db
        random_addresses = db.get_random_ecosystem_addresses(2)

        first_address, second_address = random_addresses
        transaction_engine.add(first_address, second_address, 0)
        assert (len(transaction_engine.upcoming_transactions) == 1)

    def test_transaction_engine_operates(self):
        transaction_engine = self.mix_service.transaction_engine
        db = self.mix_service.db
        random_addresses = db.get_random_ecosystem_addresses(2)

        first_address, second_address = random_addresses
        transaction_engine.add(first_address, second_address, 0)

        transaction_engine.execute_pending_transactions()

        assert (len(transaction_engine.upcoming_transactions) == 0)

    def test_transaction_engine_handles_wait(self):
        transaction_engine = self.mix_service.transaction_engine
        db = self.mix_service.db
        random_addresses = db.get_random_ecosystem_addresses(2)

        first_address, second_address = random_addresses
        transaction_engine.add(first_address, second_address)

        time.sleep(HyperParameters.TUMBLER_EPOCH_LENGTH)
        transaction_engine.execute_pending_transactions()

        assert (len(transaction_engine.upcoming_transactions) == 0)
        

    def test_tumbler_creates_transactions(self):
        self.mix_service.tumbler.operate()

        transaction_engine = self.mix_service.transaction_engine

        assert (len(transaction_engine.upcoming_transactions) > 0)

    def tearDown(self):
        self.mix_service.db.delete_database()


if __name__ == '__main__':
    unittest.main()
