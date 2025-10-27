"""
Unit tests for FakeInfo class - get_fake_persons() method
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
                {'firstName': 'John', 'lastName': 'Doe', 'gender': 'male'},
                {'firstName': 'Jane', 'lastName': 'Smith', 'gender': 'female'}
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

class TestGetFakePersonsBlackBox:
    """Black-box tests using Equivalence Partitioning (EP) and Boundary Value Analysis (BVA)"""

    # ========== EP1: Valid range (2-100) ==========

    @pytest.mark.parametrize("amount", [2, 50, 100])
    def test_valid_range_returns_correct_amount(self, amount):
        """EP1: Valid range (2-100) returns exact amount requested"""
        result = FakeInfo.get_fake_persons(amount)
        assert len(result) == amount, \
            f"Expected {amount} persons, got {len(result)}"
        assert isinstance(result, list), "Result should be a list"
        assert all(isinstance(p, dict) for p in result), \
            "All persons should be dictionaries"

    # ========== EP2: Under minimum (< 2) → clamped to 2 ==========

    @pytest.mark.parametrize("amount", [0, 1, -5])
    def test_under_minimum_clamped_to_2(self, amount):
        """EP2: Amount < 2 is clamped to 2"""
        result = FakeInfo.get_fake_persons(amount)
        assert len(result) == 2, \
            f"Amount {amount} should be clamped to 2, got {len(result)}"

    # ========== EP3: Over maximum (> 100) → clamped to 100 ==========

    @pytest.mark.parametrize("amount", [101, 200, 1000])
    def test_over_maximum_clamped_to_100(self, amount):
        """EP3: Amount > 100 is clamped to 100"""
        result = FakeInfo.get_fake_persons(amount)
        assert len(result) == 100, \
            f"Amount {amount} should be clamped to 100, got {len(result)}"

    # ========== BVA: Boundary values ==========

    # amount = 1   → limit (right under minimum)
    # amount = 2   → limit (exactly minimum)
    # amount = 100 → limit (exactly maximum)
    # amount = 101 → limit (right over maximum)

    def test_bva_amount_1_clamped_to_2(self):
        """BVA: amount=1 (under min) is clamped to 2"""
        result = FakeInfo.get_fake_persons(1)
        assert len(result) == 2, "Amount 1 should be clamped to 2"

    def test_bva_amount_2_lower_bound(self):
        """BVA: amount=2 (lower bound) returns exactly 2"""
        result = FakeInfo.get_fake_persons(2)
        assert len(result) == 2, "Amount 2 should return exactly 2"

    def test_bva_amount_100_upper_bound(self):
        """BVA: amount=100 (upper bound) returns exactly 100"""
        result = FakeInfo.get_fake_persons(100)
        assert len(result) == 100, "Amount 100 should return exactly 100"

    def test_bva_amount_101_clamped_to_100(self):
        """BVA: amount=101 (over max) is clamped to 100"""
        result = FakeInfo.get_fake_persons(101)
        assert len(result) == 100, "Amount 101 should be clamped to 100"

    # ========== Additional EP tests ==========

    def test_all_persons_have_required_structure(self):
        """All returned persons have correct dict structure"""
        result = FakeInfo.get_fake_persons(5)
        required_keys = {'CPR', 'firstName', 'lastName', 'gender', 'birthDate', 'address', 'phoneNumber'}

        for person in result:
            assert isinstance(person, dict), "Each person should be a dict"
            assert set(person.keys()) == required_keys, \
                f"Person missing keys: {required_keys - set(person.keys())}"

    def test_persons_are_unique(self):
        """Generated persons should have unique CPRs (high probability)"""
        result = FakeInfo.get_fake_persons(50)
        cprs = [p['CPR'] for p in result]
        unique_cprs = len(set(cprs))

        # With 50 persons, we expect at least 45 unique CPRs (90%)
        assert unique_cprs >= 45, \
            f"Expected at least 45 unique CPRs out of 50, got {unique_cprs}"


# ========== WHITE-BOX TESTS ==========

class TestGetFakePersonsWhiteBox:
    """White-box tests for Statement Coverage and Decision Coverage"""

    def test_statement_coverage_all_lines_executed(self):
        """
        White-box Statement Coverage: All lines in get_fake_persons() executed
        Lines covered:
        - if amount < 2:
        -     amount = 2
        - if amount > 100:
        -     amount = 100
        - bulk_info = []
        - for _ in range(amount):
        -     fake = FakeInfo()
        -     bulk_info.append(fake.get_fake_person())
        - return bulk_info
        """
        # Execute with amount that triggers no clamping
        result = FakeInfo.get_fake_persons(10)
        assert len(result) == 10
        assert isinstance(result, list)

    def test_decision_coverage_amount_less_than_2(self):
        """White-box Decision Coverage: Branch 'amount < 2' is True"""
        result = FakeInfo.get_fake_persons(0)  # Triggers: if amount < 2
        assert len(result) == 2, "Should clamp to 2 when amount < 2"

    def test_decision_coverage_amount_greater_than_100(self):
        """White-box Decision Coverage: Branch 'amount > 100' is True"""
        result = FakeInfo.get_fake_persons(150)  # Triggers: if amount > 100
        assert len(result) == 100, "Should clamp to 100 when amount > 100"

    def test_decision_coverage_amount_in_valid_range(self):
        """White-box Decision Coverage: Both branches False (no clamping)"""
        result = FakeInfo.get_fake_persons(50)  # No clamping needed
        assert len(result) == 50, "Should return exact amount when in valid range"

    def test_decision_coverage_both_clamps_cannot_trigger(self):
        """
        White-box Decision: Both clamp conditions cannot be true simultaneously
        (amount cannot be both < 2 AND > 100)
        """
        # This test documents that the two if-statements are independent
        # and cannot both execute in the same call

        # Test lower clamp
        result1 = FakeInfo.get_fake_persons(-10)
        assert len(result1) == 2

        # Test upper clamp
        result2 = FakeInfo.get_fake_persons(500)
        assert len(result2) == 100


# ========== EDGE CASE TESTS ==========

class TestGetFakePersonsEdgeCases:
    """Edge case tests for unusual but valid scenarios"""

    def test_negative_amount_clamped_to_2(self):
        """Edge case: Negative amounts are clamped to 2"""
        for amount in [-1, -10, -100]:
            result = FakeInfo.get_fake_persons(amount)
            assert len(result) == 2, \
                f"Negative amount {amount} should be clamped to 2"

    def test_zero_amount_clamped_to_2(self):
        """Edge case: Zero amount is clamped to 2"""
        result = FakeInfo.get_fake_persons(0)
        assert len(result) == 2, "Zero amount should be clamped to 2"

    def test_very_large_amount_clamped_to_100(self):
        """Edge case: Very large amounts are clamped to 100"""
        for amount in [1000, 10000, 999999]:
            result = FakeInfo.get_fake_persons(amount)
            assert len(result) == 100, \
                f"Large amount {amount} should be clamped to 100"

    def test_returns_list_not_other_types(self):
        """Edge case: Always returns list (not tuple, set, etc.)"""
        result = FakeInfo.get_fake_persons(10)
        assert type(result) is list, \
            f"Should return list, got {type(result).__name__}"

    def test_stress_test_maximum_persons(self):
        """Stress test: Generate maximum 100 persons successfully"""
        result = FakeInfo.get_fake_persons(100)

        assert len(result) == 100, "Should generate exactly 100 persons"
        assert all(isinstance(p, dict) for p in result), \
            "All 100 persons should be valid dicts"

        # Check all have valid structure
        for person in result:
            assert len(person) == 7, "Each person should have 7 fields"
            assert 'CPR' in person, "Each person should have CPR"

    def test_minimum_persons_have_correct_structure(self):
        """Edge case: Minimum 2 persons have correct structure"""
        result = FakeInfo.get_fake_persons(2)

        assert len(result) == 2
        required_keys = {'CPR', 'firstName', 'lastName', 'gender', 'birthDate', 'address', 'phoneNumber'}

        for person in result:
            assert set(person.keys()) == required_keys
            assert len(person['CPR']) == 10
            assert len(person['phoneNumber']) == 8
