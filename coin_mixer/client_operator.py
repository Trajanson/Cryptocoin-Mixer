# -*- coding: utf-8 -*-
import numpy as np


class ClientOperator(object):
    def __init__(self, input_monitor, output_monitor):
        self.input_monitor = input_monitor
        self.output_monitor = output_monitor

    def add_request(self, input_address, output_addresses, request_value,
                    user_callback=None):
        assert(isinstance(output_addresses, list))

        self.input_monitor.add_target(input_address, request_value)

        for allocation in self.__allocate(output_addresses, request_value):
            address, goal_value = allocation
        self.output_monitor.add_target(address, goal_value, user_callback)

    def __allocate(self, output_addresses, request_value):
        """
        :type output_addresses: [String]
        :type request_value: int
        :rtype: [(String, Int)] - [(Address, goal_value)]
        """
        allocations = [[address, 0] for address in output_addresses]
        a = range(len(allocations))
        size = len(allocations)
        for address_index in np.random.choice(a, size, replace=True):
            allocations[address_index][1] += 1

        return allocations
