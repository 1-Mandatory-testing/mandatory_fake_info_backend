"""
Unit tests for FakeInfo.get_fake_persons()

Black-box: Equivalence Partitioning (EP), Boundary Value Analysis (BVA)
White-box: Decision coverage for clamping logic
"""
from unittest.mock import patch

import pytest

from fake_info import FakeInfo


@pytest.fixture(autouse=True)
def mock_fake_info():
    """Mock FakeInfo constructor and get_fake_person to isolate logic"""
    with patch.object(FakeInfo, '__init__', return_value=None), \
         patch.object(FakeInfo, 'get_fake_person', return_value={'test': 'person'}):
        yield


# ========== BLACK-BOX: EQUIVALENCE PARTITIONING ==========

@pytest.mark.parametrize("amount,expected", [
    (2, 2),      # Valid range: minimum
    (50, 50),    # Valid range: middle
    (100, 100),  # Valid range: maximum
], ids=['min-valid', 'mid-valid', 'max-valid'])
def test_valid_range_returns_exact_amount(amount, expected):
    """EP1: For 2 <= amount <= 100, returns exactly 'amount' persons"""
    result = FakeInfo.get_fake_persons(amount)

    assert len(result) == expected
    assert isinstance(result, list)
    assert all(isinstance(p, dict) for p in result)


@pytest.mark.parametrize("amount", [0, 1, -5], ids=['zero', 'one', 'negative'])
def test_under_minimum_is_clamped_to_two(amount):
    """EP2: For amount < 2, result is clamped to 2"""
    result = FakeInfo.get_fake_persons(amount)

    assert len(result) == 2


@pytest.mark.parametrize("amount", [101, 200, 1000], ids=['101', '200', '1000'])
def test_over_maximum_is_clamped_to_hundred(amount):
    """EP3: For amount > 100, result is clamped to 100"""
    result = FakeInfo.get_fake_persons(amount)

    assert len(result) == 100


# ========== BLACK-BOX: BOUNDARY VALUE ANALYSIS ==========

@pytest.mark.parametrize("amount,expected", [
    (1, 2),      # Just below min -> clamp to 2
    (2, 2),      # Lower bound
    (3, 3),      # Just above lower bound
    (99, 99),    # Just below upper bound
    (100, 100),  # Upper bound
    (101, 100),  # Just above max -> clamp to 100
], ids=['below-min', 'min', 'min+1', 'max-1', 'max', 'above-max'])


def test_boundaries_and_clamping(amount, expected):
    """BVA: Test boundary values and clamping behavior"""
    result = FakeInfo.get_fake_persons(amount)

    assert len(result) == expected


# ========== WHITE-BOX: DECISION COVERAGE ==========

def test_branch_amount_less_than_two():
    """White-box: Decision branch amount < 2 triggers clamp to 2"""
    result = FakeInfo.get_fake_persons(0)

    assert len(result) == 2


def test_branch_amount_in_range_no_clamp():
    """White-box: Decision branch 2 <= amount <= 100 does not clamp"""
    result = FakeInfo.get_fake_persons(50)

    assert len(result) == 50


def test_branch_amount_greater_than_hundred():
    """White-box: Decision branch amount > 100 triggers clamp to 100"""
    result = FakeInfo.get_fake_persons(150)

    assert len(result) == 100

