# -*- coding: utf-8 -*-
import threading
import time

from coin_mixer.bootstrapper import run_bootstrapper
from coin_mixer.constants import HyperParameters
from coin_mixer.integrated_mix_service import MixService
from coin_mixer.models.user import User


class MonteCarloSimulation():
    def execute(self, num_runs):
        self.__execute_run()

    def __execute_run(self):
        self.__initialize_run()
        self.__engage_tumbler()
        self.__engage_transaction_engine()

        for i in range(20):
            self.__simulate_client_request()

    def __initialize_run(self):
        self.mix_service = MixService(in_test=True)

        self.mix_service.db.delete_database()

        run_bootstrapper(self.mix_service.coin_interface, self.mix_service.db,
                         self.mix_service.output_monitor)

    def __engage_tumbler(self):
        epoch_length = HyperParameters.TUMBLER_EPOCH_LENGTH
        threading.Timer(epoch_length, self.__engage_tumbler).start()

        self.mix_service.tumbler.operate()

    def __engage_transaction_engine(self):
        epoch_length = HyperParameters.TRANSACTION_ENGINE_EPOCH_LENGTH
        threading.Timer(epoch_length, self.__engage_transaction_engine).start()

        self.mix_service.transaction_engine.execute_pending_transactions()

    def __simulate_client_request(self):
        coin_interface = self.mix_service.coin_interface
        client_operator = self.mix_service.client_operator

        new_input_address = coin_interface.select_new_address_name()
        new_output_address = coin_interface.select_new_address_name()

        coin_interface.create_address_with_coins(new_input_address)

        user = User()
        request_value = 1

        client_operator.add_request(new_input_address, [new_output_address],
                                    request_value, user)
        print("Client Request Added")


simulation = MonteCarloSimulation()
simulation.execute(1)

FIVE_MINUTES = 5 * 60
time.sleep(FIVE_MINUTES)
print("SIMULATION EPOCH CONCLUDED")
