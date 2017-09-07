# -*- coding: utf-8 -*-
import threading
import time

from coin_mixer.tumbler.tumbler import Tumbler
from coin_mixer.utils.database_handler import DatabaseHandler as DB
from coin_mixer.transaction_engine.transaction_engine import TransactionEngine
from coin_mixer.input_monitor.input_monitor import InputMonitor
from coin_mixer.output_monitor.output_monitor import OutputMonitor
from coin_mixer.client_operator import ClientOperator
from coin_mixer.bootstrapper import run_bootstrapper
from coin_mixer.constants import HyperParameters
from coin_mixer.utils.mock_cryptocoin_api import MockCryptocoinAPI
from coin_mixer.utils.cryptocoin_api_handler import CryptocoinAPIHandler


database = DB(test_db=True)
database.delete_database()

cryptocoin_handler = CryptocoinAPIHandler(MockCryptocoinAPI())

output_monitor = OutputMonitor(database)

transaction_enginer = TransactionEngine(database, cryptocoin_handler,
                                        output_monitor)

tumbler = Tumbler(database, transaction_enginer, cryptocoin_handler)

input_monitor = InputMonitor(database, cryptocoin_handler, tumbler)

run_bootstrapper(cryptocoin_handler, database, output_monitor)

client_operator = ClientOperator(input_monitor, output_monitor)


def engage_tumbler():
    epoch_length = HyperParameters.TUMBLER_EPOCH_LENGTH
    threading.Timer(epoch_length, engage_tumbler).start()

    tumbler.operate()


def engage_transaction_engine():
    epoch_length = HyperParameters.TRANSACTION_ENGINE_EPOCH_LENGTH
    threading.Timer(epoch_length, engage_tumbler).start()

    transaction_enginer.execute_pending_transactions()


def engage_mixer(time_duration=float("inf")):
    engage_tumbler()
    engage_transaction_engine()


def simulate_client_request():
    # client_operator.add_request()
    pass


engage_mixer()

FIVE_MINUTES = 5 * 60
time.sleep(FIVE_MINUTES)
