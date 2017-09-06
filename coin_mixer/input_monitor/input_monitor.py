class Input_Monitor(object):
    def __init__(self, database, cryptocoin_handler, tumbler):
        self.db = database
        self.cryptocoin_handler = cryptocoin_handler
        self.tumbler = tumbler

        """
            {address: address,
             target_goal: targetValue
            }
        """
        self.targets = []

    def check_inputs(self):
        remaining_targets = []
        for target_data in self.targets:
            if self.__target_goal_reached(target_data):
                self.push_coins_into_ecosystem(target_data)
            else:
                remaining_targets.append(target_data)

        self.targets = remaining_targets

    def push_coins_into_ecosystem(self, target_data):
        input_address = target_data.address
        new_ecosystem_address = self.cryptocoin_handler.selectNewAddressName()
        value = target_data.target_goal
        self.cryptocoin_handler.send_value(input_address,
                                           new_ecosystem_address,
                                           value)

        baseline_value = self.tumbler.select_baseline_values(0, True)[0]
        self.db.store_new_decreasing_address(new_ecosystem_address,
                                             baseline_value,
                                             value, isOnlyDecreasing=True,
                                             isOnlyIncreasing=False)

    def __target_goal_reached(self, target_data):
        target_goal = target_data.target_goal

        address = target_data.address
        address_balance = self.cryptocoin_handler.getBalanceAtAddress(address)

        return address_balance >= target_goal
