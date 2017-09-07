# -*- coding: utf-8 -*-


class AddressSchema(object):
    # Addresses #
    FIELD_BALANCE = 'Balance'
    FIELD_BASELINE = 'Mean Reverting Balance'
    FIELD_MAX_VALUE = 'Max Value'

    SET_ONLY_DECREASING = 'Restricted to Decreasing'
    SET_ONLY_INCREASING = 'Restricted to Increasing'

    SET_ECOSYSTEM = 'Ecosystem Addresses'

    SET_CLIENT_INPUT = 'Addresses Given By Client For Mixing'
    SET_CLIENT_OUTPUT = 'Addresses Requested By Client For Mixed Coins'

    SET_COMPROMISED = 'Addresses That Have Been Compromised'

    KEY_TOTAL_BALANCE = 'Total Balance'
