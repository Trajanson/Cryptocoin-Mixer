# -*- coding: utf-8 -*-
import math


class Address(object):
    def __init__(self, address, balance, baseline, isOnlyDecreasing=False,
                 isOnlyIncreasing=False, isForClientInput=False,
                 isForClientOutput=False, hasBeenCompromised=False,
                 maxValue=float("inf")):

        adr = address
        if balance is None:
            raise ValueError(f'Address balance at {adr} is missing')
        if int(balance.decode('utf-8')) < 0:
            bal = balance.decode('utf-8')
            raise ValueError(
                f'Address balance at {adr} is negative with a value of {bal}')
        if baseline is None:
            raise ValueError(f'Address baseline at {adr} is missing')

        self.address = str(address)
        self.balance = int(balance.decode('utf-8'))
        self.baseline = float(baseline.decode('utf-8'))
        self.isOnlyDecreasing = bool(isOnlyDecreasing)
        self.isOnlyIncreasing = bool(isOnlyIncreasing)
        self.isForClientInput = bool(isForClientInput)
        self.isForClientOutput = bool(isForClientOutput)
        self.hasBeenCompromised = bool(hasBeenCompromised)
        self.maxValue = float(maxValue.decode('utf-8'))

    def calculate_charge(self):
        return (self.balance - self.baseline) / self.baseline

    def should_be_removed_from_ecosystem(self):
        return self.isOnlyDecreasing and (math.floor(self.balance) == 0)

    def is_at_max_value(self):
        if self.maxValue == float("inf"):
            return False
        return self.balance == math.floor(self.maxValue)
