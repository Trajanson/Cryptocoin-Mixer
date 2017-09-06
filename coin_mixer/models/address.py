class Address(object):
    def __init__(self, address, balance, baseline, isOnlyDecreasing=False,
                 isOnlyIncreasing=False, isForClientInput=False,
                 isForClientOutput=False):
        self.address = address
        self.balance = balance
        self.baseline = baseline
        self.isOnlyDecreasing = isOnlyDecreasing
        self.isOnlyIncreasing = isOnlyIncreasing
        self.isForClientInput = isForClientInput
        self.isForClientOutput = isForClientOutput
