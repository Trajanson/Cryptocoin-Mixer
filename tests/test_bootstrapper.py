# -*- coding: utf-8 -*-
"""
    Bootstrapper Tests
    ~~~~~~~~~~~~
    Tests that the Bootstrapper successfully injects coins into the system
    and that empty addresses are reserved for future use
"""

import unittest

from coin_mixer.utils.database_handler import Database_Handler
from coin_mixer.constants import HyperParameters

from coin_mixer.bootstrapper import run_bootstrapper


class BootstrapperTestCase(unittest.TestCase):

    def setUp(self):
        self.db = Database_Handler(test_db=True)
        self.db.delete_database()

        run_bootstrapper(in_test=True)

    def test_seed_fund(self):
        expected = HyperParameters.NUM_INJECTION_ADDRESSES * 50

        actual = self.db.total_value_in_ecosystem()
        assert actual == expected

    def tearDown(self):
        self.db.delete_database()


if __name__ == '__main__':
    unittest.main()
