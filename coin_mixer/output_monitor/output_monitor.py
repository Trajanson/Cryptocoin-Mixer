# -*- coding: utf-8 -*-


class OutputMonitor(object):
    def __init__(self, database):
        self.db = database
        self.monitored_addresses = {}

    def add_target(self, address, goal_value, user_callback=None):
        self.db.store_new_client_output_address(address,
                                                baseline_value=goal_value,
                                                value=0, max_value=goal_value)

        self.__store_target(address, goal_value, user_callback)

    def release_address(self, address):
        """
        :type address: string
        :rtype: None
        """
        self.db.remove_address_from_ecosystem(address)

        self.__notify_user_of_released_address(address)
        self.__remove_target(address)

    def __notify_user_of_released_address(self, address):
        callback = self.__get_address_user_callback(address)
        if callback is not None:
            callback()
        print("=================================================")
        print(f"Funds at {address} have been released")
        print(f"{len(self.monitored_addresses) - 1} request outstanding")
        print("=================================================")

    def __get_address_user_callback(self, address):
        return self.monitored_addresses[address]["user_callback"]

    def __get_address_goal_value(self, address):
        return self.monitored_addresses[address]["goal_value"]

    def __store_target(self, address, goal_value, user_callback):
        self.monitored_addresses[address] = {"goal_value": goal_value,
                                             "user_callback": user_callback}

    def __remove_target(self, address):
        self.monitored_addresses.pop(address, None)
