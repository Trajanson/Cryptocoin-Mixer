class Address(object):
    def __init__(self, address, balance, baseline, isOnlyDecreasing=False,
                 isOnlyIncreasing=False, isForClientInput=False,
                 isForClientOutput=False):

        if balance is None:
            raise ValueError('Address balance is missing')
        if int(balance) < 0:
            raise ValueError('Address balance is negative')
        if baseline is None:
            raise ValueError('Address baseline is missing')

        self.address = str(address)
        self.balance = int(balance)
        self.baseline = float(baseline)
        self.isOnlyDecreasing = bool(isOnlyDecreasing)
        self.isOnlyIncreasing = bool(isOnlyIncreasing)
        self.isForClientInput = bool(isForClientInput)
        self.isForClientOutput = bool(isForClientOutput)
