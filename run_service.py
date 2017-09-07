# -*- coding: utf-8 -*-

import threading

from coin_mixer.constants import HyperParameters
from coin_mixer.web_service.flask import WebService
from coin_mixer.integrated_mix_service import MixService
from coin_mixer.bootstrapper import run_bootstrapper


class Operators(object):
    def __init__(self, mix_service):
        self.mix_service = mix_service

    def run(self):
        self.__engage_tumbler()
        self.__engage_transaction_engine()

    def __engage_tumbler(self):
        epoch_length = HyperParameters.TUMBLER_EPOCH_LENGTH

        threading.Timer(epoch_length, self.__engage_tumbler).start()
        self.mix_service.tumbler.operate()

    def __engage_transaction_engine(self):
        epoch_length = HyperParameters.TRANSACTION_ENGINE_EPOCH_LENGTH

        threading.Timer(epoch_length, self.__engage_transaction_engine).start()

        self.mix_service.transaction_engine.execute_pending_transactions()

    def __engage_input_monitor(self):
        epoch_length = HyperParameters.INPUT_MONITOR_EPOCH_LENGTH

        threading.Timer(epoch_length, self.__engage_input_monitor).start()

        self.mix_service.input_monitor.check_inputs()


if __name__ == "__main__":
    in_test = False

    mix_service = MixService(in_test)

    if in_test:
        mix_service.db.delete_database()
        run_bootstrapper(mix_service.coin_interface, mix_service.db,
                         mix_service.output_monitor)

    operators = Operators(mix_service)
    operators.run()

    web_service = WebService(mix_service)
    web_service.run()
