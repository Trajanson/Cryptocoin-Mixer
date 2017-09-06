import time


class TransactionEngine(object):
    def __init__(self, database):
        self.db = database
        self.upcoming_transactions = []

    def add(self, firstAddress, secondAddress):
        current_time = time.time()
        pass

    def __execute_transaction(self, firstAddress, secondAddress):
        pass
