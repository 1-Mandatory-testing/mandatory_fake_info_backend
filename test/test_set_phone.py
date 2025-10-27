"""
Unit tests for FakeInfo._set_phone() method

Black-box: Equivalence Partitioning (EP), Boundary Value Analysis (BVA)
White-box: Statement Coverage (no branches in method)
"""
import re
from unittest.mock import patch

import pytest

from fake_info import FakeInfo


@pytest.fixture
def fake_instance():
    """Create FakeInfo instance"""
    return object.__new__(FakeInfo)


PHONE_RE = re.compile(r'^\d{8}$')
PREFIXES = FakeInfo.PHONE_PREFIXES


# ========== BLACK-BOX: EQUIVALENCE PARTITIONING ==========

def test_phone_length_is_always_8_digits(fake_instance):
    """Valid output partition - all phone numbers are 8 digits"""
    for _ in range(10):
        fake_instance._set_phone()
        assert PHONE_RE.fullmatch(fake_instance.phone_number)


def test_phone_starts_with_valid_prefix(fake_instance):
    """Valid prefix partition - must match allowed prefixes"""
    for _ in range(10):
        fake_instance._set_phone()
        assert any(fake_instance.phone_number.startswith(p) for p in PREFIXES)


def test_phone_contains_only_digits(fake_instance):
    """Valid characters partition - only numeric digits allowed"""
    for _ in range(10):
        fake_instance._set_phone()
        assert fake_instance.phone_number.isdigit()


# ========== BLACK-BOX: BOUNDARY VALUE ANALYSIS (Deterministic) ==========

def test_prefix_length_1_minimum(fake_instance):
    with patch('fake_info.random.choice', return_value='2'):
        fake_instance._set_phone()
    assert fake_instance.phone_number.startswith('2')
    assert len(fake_instance.phone_number) == 8
    assert PHONE_RE.fullmatch(fake_instance.phone_number)

def test_prefix_length_2_medium(fake_instance):
    with patch('fake_info.random.choice', return_value='30'):
        fake_instance._set_phone()
    assert fake_instance.phone_number.startswith('30')
    assert len(fake_instance.phone_number) == 8
    assert PHONE_RE.fullmatch(fake_instance.phone_number)

def test_prefix_length_3_maximum(fake_instance):
    with patch('fake_info.random.choice', return_value='342'):
        fake_instance._set_phone()
    assert fake_instance.phone_number.startswith('342')
    assert len(fake_instance.phone_number) == 8
    assert PHONE_RE.fullmatch(fake_instance.phone_number)


# ========== WHITE-BOX: STATEMENT COVERAGE ==========

def test_all_statements_executed(fake_instance):
    """White-box: Executes all statements in _set_phone (no branches)"""
    # Mock for deterministic output
    with patch('fake_info.random.choice', return_value='50'), \
         patch('fake_info.random.randint', return_value=0):
        fake_instance._set_phone()

    # Verify all steps executed: prefix choice, suffix generation, concatenation
    assert hasattr(fake_instance, 'phone_number')
    assert isinstance(fake_instance.phone_number, str)
    assert fake_instance.phone_number == '50000000'
    assert PHONE_RE.fullmatch(fake_instance.phone_number)
