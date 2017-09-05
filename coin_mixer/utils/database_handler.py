import redis

from coin_mixer.constants import Config
from coin_mixer.schemas import Address_Schema as schema


class Database_Handler(object):
    ECOSYSTEM_ADDRESSES_SET = 'ecosystem addresses'

    def __init__(self, test_db=True):
        self.is_test_db = test_db
        self.db = self.__get_database()

    """
    =========
    INTERFACE
    =========
    """

    def store_new_decreasing_address(self, address, baseline_value, value=0):
        self.store_new_address(address, baseline_value, value,
                               isOnlyDecreasing=True, isOnlyIncreasing=False)

    def store_new_increasing_address(self, address, baseline_value, value=0):
        self.store_new_address(address, baseline_value, value,
                               isOnlyDecreasing=False, isOnlyIncreasing=True)

    def store_new_address(self, address, baseline_value, value=0,
                          isOnlyDecreasing=False, isOnlyIncreasing=False):
        if isOnlyDecreasing is False and isOnlyIncreasing is False:
            raise ValueError('Address cannot be increasing and decreasing')

        if value <= 0 or baseline_value <= 0:
            raise ValueError('Value or intended value cannot be less than 0')

        addressHash = {schema.FIELD_BALANCE: value,
                       schema.FIELD_BALANCE: baseline_value}

        pipe = self.db.pipeline()

        pipe.sadd(schema.SET_ECOSYSTEM, address)
        pipe.hmset(address, addressHash)
        pipe.incrby(schema.KEY_TOTAL_BALANCE, value)

        if isOnlyDecreasing is True:
            pipe.sadd(schema.SET_ONLY_DECREASING, address)
        elif isOnlyIncreasing is True:
            pipe.sadd(schema.SET_ONLY_INCREASING, address)

        pipe.execute()

    def remove_address_from_ecosystem(self):
        pass
        pipe = self.db.pipeline()
        pipe.execute()

    def total_value_in_ecosystem(self):
        return self.db.get(schema.KEY_TOTAL_BALANCE)

    def delete_database(self):
        if self.is_test_db is False:
            raise PermissionError('Can only clear test database')
        else:
            self.db.flushdb()

    def __get_database(self):
        if self.is_test_db is True:
            db_number = Config.TEST_DB_NUMBER
            db_host = Config.TEST_DB_HOST
        else:
            db_number = Config.PRODUCTION_DB_NUMBER
            db_host = Config.PRODUCTION_DB_HOST

        return redis.StrictRedis(host=db_host, port=6379, db=db_number)
