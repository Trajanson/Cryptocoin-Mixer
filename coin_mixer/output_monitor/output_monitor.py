# -*- coding: utf-8 -*-


class OutputMonitor(object):
    def __init__(self, database):
        self.db = database
        self.monitored_addresses = {}

    def add_target(self, address, goal_value):
        self.db.store_new_client_output_address(address,
                                                baseline_value=goal_value,
                                                value=0, max_value=goal_value)

        self.__store_target(address, goal_value)

    def release_address(self, address):
        """
        :type address: string
        :rtype: None
        """
        self.db.remove_address_from_ecosystem(address)
        self.__notify_user_of_released_address(address)
        self.__remove_target(address)

    def __notify_user_of_released_address(self, address):
        owner = self.__get_owner_of_address(address)
        print(f"{owner}'s funds at {address} have been released")

    def __get_owner_of_address(self, address):
        return self.monitored_addresses[address]

    def __store_target(self, address, goal_value):
        self.monitored_addresses[address] = goal_value

    def __remove_target(self, address):
        self.monitored_addresses.pop(address, None)
