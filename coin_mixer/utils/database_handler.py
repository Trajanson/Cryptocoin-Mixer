import redis
import math

from coin_mixer.constants import Config
from coin_mixer.schemas import Address_Schema as schema
from coin_mixer.models.address import Address


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

    def store_new_decreasing_address(self, address, baseline_value, value=0,
                                     isForClientInput=False,
                                     isForClientOutput=False):
        self.store_new_address(address, baseline_value, value,
                               isOnlyDecreasing=True, isOnlyIncreasing=False,
                               isForClientInput=isForClientInput,
                               isForClientOutput=isForClientOutput)

    def store_new_increasing_address(self, address, baseline_value, value=0,
                                     isForClientInput=False,
                                     isForClientOutput=False):
        self.store_new_address(address, baseline_value, value,
                               isOnlyDecreasing=False, isOnlyIncreasing=True,
                               isForClientInput=isForClientInput,
                               isForClientOutput=isForClientOutput)

    def store_new_address(self, address, baseline_value, value=0,
                          isOnlyDecreasing=False, isOnlyIncreasing=False,
                          isForClientInput=False, isForClientOutput=False):
        if isOnlyDecreasing is True and isOnlyIncreasing is True:
            raise ValueError('Address cannot be increasing and decreasing')

        if isForClientInput is True and isForClientOutput is True:
            raise ValueError('Input address cannot be reused for output')

        if value < 0 or baseline_value < 0:
            raise ValueError('Value or intended value cannot be less than 0')

        addressHash = {schema.FIELD_BALANCE: value,
                       schema.FIELD_BASELINE: baseline_value}

        pipe = self.db.pipeline()

        pipe.sadd(schema.SET_ECOSYSTEM, address)
        pipe.hmset(address, addressHash)
        pipe.incrby(schema.KEY_TOTAL_BALANCE, value)

        if isOnlyDecreasing is True:
            pipe.sadd(schema.SET_ONLY_DECREASING, address)
        elif isOnlyIncreasing is True:
            pipe.sadd(schema.SET_ONLY_INCREASING, address)

        if isForClientInput is True:
            pipe.sadd(schema.SET_CLIENT_INPUT, address)
        else:
            pipe.sadd(schema.SET_CLIENT_OUTPUT, address)

        pipe.execute()

    def remove_address_from_ecosystem(self, address):
        value_at_address = self.db.hget(address, schema.FIELD_BALANCE) or 0
        is_output_address = self.db.sismember(schema, schema.SET_CLIENT_OUTPUT,
                                              address)

        if math.floor(value_at_address) > 0 and is_output_address is False:
            raise ValueError('Cannot remove an internal address with coins')

        pipe = self.db.pipeline()
        pipe.delete(address)
        pipe.incrby(schema.KEY_TOTAL_BALANCE, -1*math.floor(value_at_address))
        pipe.srem(schema.SET_ONLY_DECREASING, address)
        pipe.srem(schema.SET_ONLY_INCREASING, address)
        pipe.srem(schema.SET_ECOSYSTEM, address)
        pipe.srem(schema.SET_CLIENT_INPUT, address)
        pipe.srem(schema.SET_CLIENT_OUTPUT, address)
        pipe.execute()

    def total_value_in_ecosystem(self):
        return int(self.db.get(schema.KEY_TOTAL_BALANCE))

    def total_num_addresses_in_ecosystem(self):
        return int(self.db.scard(schema.SET_ECOSYSTEM))

    def delete_database(self):
        if self.is_test_db is False:
            raise PermissionError('Can only clear test database')
        else:
            self.db.flushdb()

    def get_random_ecosystem_addresses(self, num_addresses):
        addresses = self.db.srandmember(schema.SET_ECOSYSTEM, num_addresses)
        return list(map(lambda address: self.get_address_data(address),
                        addresses))

    def get_address_data(self, address):
        pipe = self.db.pipeline()

        # balance
        pipe.hget(address, schema.FIELD_BALANCE)

        # baseline
        pipe.hget(address, schema.FIELD_BASELINE)

        # isOnlyDecreasing
        pipe.sismember(schema.SET_ONLY_DECREASING, address)

        # isOnlyIncreasing
        pipe.sismember(schema.SET_ONLY_INCREASING, address)

        # isForClientInput
        pipe.sismember(schema.SET_CLIENT_INPUT, address)

        # isForClientOutput
        pipe.sismember(schema.SET_CLIENT_OUTPUT, address)

        responses = pipe.execute()
        balance, baseline, isOnlyDecreasing = responses[0:3]
        isOnlyIncreasing, isForClientInput, isForClientOutput = responses[3:6]

        return Address(address, balance, baseline, isOnlyDecreasing,
                       isOnlyIncreasing, isForClientInput, isForClientOutput)

    """
    =========
    """

    def __get_database(self):
        if self.is_test_db is True:
            db_number = Config.TEST_DB_NUMBER
            db_host = Config.TEST_DB_HOST
        else:
            db_number = Config.PRODUCTION_DB_NUMBER
            db_host = Config.PRODUCTION_DB_HOST

        return redis.StrictRedis(host=db_host, port=6379, db=db_number)
