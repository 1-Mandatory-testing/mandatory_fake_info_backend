"""
Unit tests for FakeInfo class - _set_phone() method

Black-box techniques: Equivalence Partitioning (EP), Boundary Value Analysis (BVA)
White-box techniques: Statement Coverage, Decision Coverage
"""
from unittest.mock import MagicMock, patch

import pytest

from fake_info import FakeInfo

# ========== FIXTURES ==========

@pytest.fixture(autouse=True)
def mock_dependencies():
    """Mock DB and file/json so FakeInfo.__init__ can run"""
    with patch('fake_info.DB') as mock_db, \
         patch('builtins.open', create=True), \
         patch('json.load') as mock_json_load:

        mock_json_load.return_value = {
            'persons': [
                {'firstName': 'Test', 'lastName': 'Person', 'gender': 'male'}
            ]
        }

        mock_db_instance = MagicMock()
        mock_db_instance.get_random_town.return_value = {
            'postal_code': '2100',
            'town_name': 'København Ø'
        }
        mock_db.return_value = mock_db_instance

        yield


# ========== BLACK-BOX TESTS ==========

class TestSetPhoneBlackBox:
    """Black-box tests using Equivalence Partitioning (EP) and Boundary Value Analysis (BVA)"""

    def test_length_is_8_digits(self):
        """EP1: Phone number is always exactly 8 digits"""
        for _ in range(100):
            fake = FakeInfo()
            assert len(fake.phone_number) == 8, \
                f"Phone number '{fake.phone_number}' is not 8 digits"

    def test_starts_with_valid_prefix(self):
        """EP2: Phone number starts with one of the valid prefixes"""
        for _ in range(100):
            fake = FakeInfo()
            phone = fake.phone_number

            valid_prefixes = FakeInfo.PHONE_PREFIXES
            assert any(phone.startswith(prefix) for prefix in valid_prefixes), \
                f"Phone '{phone}' does not start with valid prefix"

    def test_only_numeric_characters(self):
        """EP3: Phone number contains only digits (no letters/special chars)"""
        for _ in range(100):
            fake = FakeInfo()
            assert fake.phone_number.isdigit(), \
                f"Phone number '{fake.phone_number}' contains non-digit characters"

    def test_bva_shortest_prefix(self):
        """BVA: Shortest prefix '2' (1 digit) results in 7 additional digits"""
        fake = FakeInfo()
        with patch('fake_info.random.choice', return_value='2'):
            fake._set_phone()

        assert len(fake.phone_number) == 8, \
            f"Expected length 8, got {len(fake.phone_number)}"
        assert fake.phone_number.startswith('2'), \
            f"Expected prefix '2', got '{fake.phone_number}'"

    def test_bva_longest_prefix(self):
        """BVA: Longest prefix '342' (3 digits) results in 5 additional digits"""
        fake = FakeInfo()
        with patch('fake_info.random.choice', return_value='342'):
            fake._set_phone()

        assert len(fake.phone_number) == 8
        assert fake.phone_number.startswith('342')

    def test_bva_medium_prefix(self):
        """BVA: Medium prefix '30' (2 digits) results in 6 additional digits"""
        fake = FakeInfo()
        with patch('fake_info.random.choice', return_value='30'):
            fake._set_phone()

        assert len(fake.phone_number) == 8
        assert fake.phone_number.startswith('30')


# ========== WHITE-BOX TESTS ==========

class TestSetPhoneWhiteBox:
    """White-box tests for Statement Coverage and Decision Coverage"""

    def test_statement_coverage(self):
        """White-box Statement Coverage: All lines in _set_phone() executed"""
        fake = FakeInfo()

        assert hasattr(fake, 'phone_number')
        assert len(fake.phone_number) == 8
        assert fake.phone_number.isdigit()

    def test_decision_coverage_no_branches(self):
        """White-box Decision Coverage: No conditional branches in _set_phone()"""
        fake = FakeInfo()
        assert isinstance(fake.phone_number, str), \
            "Method should always return a string phone number"


# ========== EDGE CASE TESTS ==========

class TestSetPhoneEdgeCases:
    """Edge case tests for unusual but valid scenarios"""

    def test_all_prefixes_produce_valid_phones(self):
        """Edge case: Every prefix in PHONE_PREFIXES produces valid 8-digit phone"""
        fake = FakeInfo()

        for prefix in FakeInfo.PHONE_PREFIXES:
            with patch('fake_info.random.choice', return_value=prefix):
                fake._set_phone()

            assert len(fake.phone_number) == 8, \
                f"Prefix '{prefix}' length: {len(fake.phone_number)}"
            assert fake.phone_number.startswith(prefix), \
                f"Expected '{prefix}', got '{fake.phone_number}'"

    def test_phone_number_is_string_not_int(self):
        """Edge case: Phone number is stored as string (not int)"""
        fake = FakeInfo()
        assert isinstance(fake.phone_number, str), \
            f"Expected string, got {type(fake.phone_number).__name__}"

    def test_stress_test_many_phones(self):
        """Stress test: Generate many phone numbers to verify stability"""
        phones = []
        for _ in range(1000):
            fake = FakeInfo()
            phones.append(fake.phone_number)

        assert all(len(p) == 8 for p in phones), "Not all phones are 8 digits"
        assert all(p.isdigit() for p in phones), "Not all phones are numeric"

        unique_phones = len(set(phones))
        assert unique_phones > 900, \
            f"Only {unique_phones} unique phones out of 1000"
