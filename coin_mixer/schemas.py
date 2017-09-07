# -*- coding: utf-8 -*-


class AddressSchema(object):
    # Addresses #
    FIELD_BALANCE = 'Balance'
    FIELD_BASELINE = 'MeanRevertingBalance'
    FIELD_MAX_VALUE = 'MaxValue'

    SET_ONLY_DECREASING = 'RestrictedToDecreasing'
    SET_ONLY_INCREASING = 'RestrictedToIncreasing'

    SET_ECOSYSTEM = 'EcosystemAddresses'

    SET_CLIENT_INPUT = 'AddressesGivenByClientForMixing'
    SET_CLIENT_OUTPUT = 'AddressesRequestedByClientForMixedCoins'

    SET_COMPROMISED = 'AddressesThatHaveBeenCompromised'

    KEY_TOTAL_BALANCE = 'TotalBalance'
