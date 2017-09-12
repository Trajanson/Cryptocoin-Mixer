from abc import ABC, abstractmethod


class InterfaceCryptocoinAPI(ABC):

    @abstractmethod
    def get_address_info(self):
        pass

    @abstractmethod
    def create_address(self):
        pass

    @abstractmethod
    def get_transactions(self):
        pass

    @abstractmethod
    def post_transaction(self):
        pass
