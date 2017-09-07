# -*- coding: utf-8 -*-
import numpy as np
import threading
import time

from coin_mixer.bootstrapper import run_bootstrapper
from coin_mixer.constants import HyperParameters
from coin_mixer.integrated_mix_service import MixService


class MonteCarloSimulation():
    def __init__(self, num_runs, num_requests_per_run, max_timeout):
        self.num_runs = num_runs
        self.num_requests_per_run = num_requests_per_run
        self.max_timeout = max_timeout

        self.seconds_per_run = []
        self.current_run_num = 0
        self.current_run_start_time = None

        self.is_waiting_at_barrier = False

        self.tumbler_is_halted = False
        self.transaction_engine_is_halted = False

    def execute(self):
        print("=================")
        print("Beginning run #%i" % (self.current_run_num + 1))

        if (self.current_run_num < self.num_runs):
            self.current_run_start_time = time.time()
            self.__execute_run()

            self.__check_for_run_completion()
        else:
            self.__print_exit_message()

    def __check_for_run_completion(self):
        interval = max(HyperParameters.TUMBLER_EPOCH_LENGTH,
                       HyperParameters.TRANSACTION_ENGINE_EPOCH_LENGTH)

        duration = time.time() - self.current_run_start_time

        timeout_condition = duration > self.max_timeout
        completion_condition = self.__has_completed_client_requests()

        if timeout_condition or completion_condition:
            if self.is_waiting_at_barrier is False:
                if timeout_condition:
                    self.seconds_per_run.append(float("inf"))
                if completion_condition:
                    self.seconds_per_run.append(duration)

                self.is_waiting_at_barrier = True
                threading.Timer(interval,
                                self.__check_for_run_completion).start()
            else:
                if (self.tumbler_is_halted is True and
                        self.transaction_engine_is_halted is True):
                    self.tumbler_is_halted = False
                    self.transaction_engine_is_halted = False

                    self.current_run_num += 1
                    self.execute()
        else:
            threading.Timer(interval, self.__check_for_run_completion).start()

    def __execute_run(self):
        self.__initialize_run()

        self.__engage_tumbler()
        self.__engage_transaction_engine()

        for i in range(self.num_requests_per_run):
            self.__simulate_client_request()

    def __engage_tumbler(self):
        epoch_length = HyperParameters.TUMBLER_EPOCH_LENGTH

        if self.is_waiting_at_barrier is True:
            self.tumbler_is_halted = True
        else:
            threading.Timer(epoch_length, self.__engage_tumbler).start()
            self.mix_service.tumbler.operate()

    def __engage_transaction_engine(self):
        epoch_length = HyperParameters.TRANSACTION_ENGINE_EPOCH_LENGTH

        if self.is_waiting_at_barrier is True:
            self.transaction_engine_is_halted = True
        else:
            threading.Timer(epoch_length,
                            self.__engage_transaction_engine).start()

            self.mix_service.transaction_engine.execute_pending_transactions()

    def __initialize_run(self):
        self.mix_service = MixService(in_test=True)

        self.mix_service.db.delete_database()

        run_bootstrapper(self.mix_service.coin_interface, self.mix_service.db,
                         self.mix_service.output_monitor)

    def __has_completed_client_requests(self):
        output_monitor = self.mix_service.output_monitor
        return len(output_monitor.monitored_addresses) == 0

    def __simulate_client_request(self):
        coin_interface = self.mix_service.coin_interface
        client_operator = self.mix_service.client_operator

        new_input_address = coin_interface.select_new_address_name()
        new_output_address = coin_interface.select_new_address_name()

        coin_interface.create_address_with_coins(new_input_address)

        request_value = 1

        client_operator.add_request(new_input_address, [new_output_address],
                                    request_value)

    def __print_exit_message(self):
        failed_runs = 0
        for run_time in self.seconds_per_run:
            if run_time == float("inf"):
                failed_runs += 1

        if failed_runs > 0:
            print("%i runs failed" % failed_runs)
        else:
            total = np.sum(self.seconds_per_run)
            mean = np.mean(self.seconds_per_run)
            print("{self.num_runs} executed in %f seconds" % total)
            print("with an average run time of %f seconds" % mean)


num_runs = 5
num_requests_per_run = 3
max_timeout = 60 * 30
simulation = MonteCarloSimulation(num_runs, num_requests_per_run, max_timeout)
simulation.execute()
