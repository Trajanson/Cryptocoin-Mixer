# -*- coding: utf-8 -*-
"""
    Mock Cryptocoin API Tests
    ~~~~~~~~~~~~
    Tests the Mock Cryptocoin API
"""

import copy
import pytest

from coin_mixer.utils.mock_cryptocoin_api import MockCryptocoinAPI


@pytest.fixture()
def mock_api():
    mock_api = MockCryptocoinAPI()
    mock_api.create_address("1")
    mock_api.create_address("2")
    mock_api.create_address("3")
    yield mock_api


def test_get_transactions(mock_api):
    actual = mock_api.get_transactions()

    expected = [{'amount': '50',
                 'timestamp': '1',
                 'toAddress': '1'},
                {'amount': '50',
                 'timestamp': '2',
                 'toAddress': '2'},
                {'amount': '50',
                 'timestamp': '3',
                 'toAddress': '3'}]

    assert __match_transactions(expected, actual)


def test_get_address_info(mock_api):
    actual = mock_api.get_address_info('1')

    expected = {"balance": "50",
                "transactions": [{
                    "timestamp": "1",
                    "toAddress": "1",
                    "amount": "50"}]}

    assert __match_transactions(expected["transactions"],
                                actual["transactions"])


def test_get_address_info_for_non_existing_address(mock_api):
    actual = mock_api.get_address_info('98765432210')

    expected = {"balance": "0",
                "transactions": []}

    assert __match_transactions(expected["transactions"],
                                actual["transactions"])


def test_post_transaction(mock_api):
    fromAddress = "1"
    toAddress = "2"
    amount = 20
    mock_api.post_transaction(fromAddress, toAddress, amount)

    actual = mock_api.get_address_info('2')

    expected = {"balance": "70",
                "transactions": [{
                    "timestamp": "2",
                    "toAddress": "2",
                    "amount": "50"}, {
                    "timestamp": "4",
                    "fromAddress": "1",
                    "toAddress": "2",
                    "amount": "20"}]}

    assert __match_address_info(expected, actual)

    actual = mock_api.get_address_info('1')

    expected = {"balance": "30",
                "transactions": [{
                    "timestamp": "1",
                    "toAddress": "1",
                    "amount": "50"}, {
                    "timestamp": "4",
                    "fromAddress": "1",
                    "toAddress": "2",
                    "amount": "20"}]}

    assert __match_address_info(expected, actual)


def test_post_transaction_unchanged_with_no_value(mock_api):
    expected = copy.deepcopy(mock_api.get_address_info('3'))

    fromAddress = "1"
    toAddress = "3"
    amount = 0
    mock_api.post_transaction(fromAddress, toAddress, amount)

    actual = copy.deepcopy(mock_api.get_address_info('3'))

    assert __match_address_info(expected, actual)


def test_post_transaction_unchanged_with_error_value(mock_api):
    expected = copy.deepcopy(mock_api.get_address_info('3'))

    fromAddress = "1"
    toAddress = "3"
    amount = 1000000000
    mock_api.post_transaction(fromAddress, toAddress, amount)

    actual = copy.deepcopy(mock_api.get_address_info('3'))

    assert __match_address_info(expected, actual)


def __match_address_info(expected, actual):
    matches_balance = float(expected["balance"]) == float(actual["balance"])
    matches_transactions = __match_transactions(expected["transactions"],
                                                actual["transactions"])

    return matches_balance and matches_transactions


def __match_transactions(expected, actual):
    if len(expected) != len(actual):
        return False

    encountered_expected_transactions = {}
    matches = 0

    for (actual_index, actual_transaction) in enumerate(actual):
        for (expected_index, expected_transaction) in enumerate(expected):
            if expected_index not in encountered_expected_transactions:
                match = __match_transaction(expected_transaction,
                                            actual_transaction)
                if match:
                    encountered_expected_transactions[expected_index] = True
                    matches += 1
                    break

    return matches == len(expected)


def __match_transaction(expected, actual):
    matches_amount = float(expected["amount"]) == float(actual["amount"])

    if "toAddress" in expected or "toAddress" in actual:
        matches_toAddress = expected["toAddress"] == actual["toAddress"]
    else:
        matches_toAddress = True

    if "fromAddress" in expected or "fromAddress" in actual:
        matches_fromAddress = expected["fromAddress"] == actual["fromAddress"]
    else:
        matches_fromAddress = True

    return matches_amount and matches_toAddress and matches_fromAddress
