import threading
import time

from coin_mixer.tumbler.tumbler import Tumbler
from coin_mixer.utils.database_handler import Database_Handler as DB
from coin_mixer.transaction_engine.transaction_engine import TransactionEngine
from coin_mixer.bootstrapper import run_bootstrapper
from coin_mixer.constants import HyperParameters

database = DB(test_db=True)
database.delete_database()

transaction_enginer = TransactionEngine(database)

tumbler = Tumbler(database, transaction_enginer)

run_bootstrapper(in_test=True)


def engage_tumbler():
    epoch_length = HyperParameters.TUMBLER_EPOCH_LENGTH
    threading.Timer(epoch_length, engage_tumbler).start()

    tumbler.generate_transactions()


def engage_transaction_engine():
    epoch_length = HyperParameters.TRANSACTION_ENGINE_EPOCH_LENGTH
    threading.Timer(epoch_length, engage_tumbler).start()

    transaction_enginer.execute_pending_transactions()


def engage_mixer(time_duration=float("inf")):
    engage_tumbler()
    engage_transaction_engine()


engage_mixer()

FIVE_MINUTES = 5 * 60
time.sleep(FIVE_MINUTES)
