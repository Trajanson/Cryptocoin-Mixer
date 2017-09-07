# -*- coding: utf-8 -*-

from coin_mixer.utils.database_handler import DatabaseHandler
from coin_mixer.utils.cryptocoin_api import CryptocoinAPI
from coin_mixer.utils.mock_cryptocoin_api import MockCryptocoinAPI
from coin_mixer.utils.cryptocoin_api_handler import CryptocoinAPIHandler
from coin_mixer.output_monitor.output_monitor import OutputMonitor
from coin_mixer.input_monitor.input_monitor import InputMonitor
from coin_mixer.transaction_engine.transaction_engine import TransactionEngine
from coin_mixer.tumbler.tumbler import Tumbler
from coin_mixer.client_operator import ClientOperator


class MixService(object):
    def __init__(self, in_test=False):
        self.db = self.__get_database_handler(in_test)
        self.coin_interface = self.__get_coin_interface(in_test)
        self.output_monitor = OutputMonitor(self.db)
        self.transaction_engine = TransactionEngine(self.db,
                                                    self.coin_interface,
                                                    self.output_monitor)
        self.tumbler = Tumbler(self.db, self.transaction_engine,
                               self.coin_interface)
        self.input_monitor = InputMonitor(self.db, self.coin_interface,
                                          self.tumbler)
        self.client_operator = ClientOperator(self.input_monitor,
                                              self.output_monitor)

    def __get_coin_interface(self, in_test):
        if in_test:
            return CryptocoinAPIHandler(MockCryptocoinAPI())
        else:
            return CryptocoinAPIHandler(CryptocoinAPI())

    def __get_database_handler(self, in_test):
        if in_test:
            return DatabaseHandler(in_test)
        else:
            return DatabaseHandler(in_test)
