"""
Unit tests for FakeInfo class - get_fake_person() method

Black-box techniques: Equivalence Partitioning (EP)
White-box techniques: Statement Coverage, Decision Coverage
"""

import re
from unittest.mock import MagicMock, patch

import pytest

from fake_info import FakeInfo

# ========== FIXTURES ==========

@pytest.fixture(autouse=True)
def mock_dependencies_for_module():
    """
    Mock DB and file/json so FakeInfo.__init__ and _set_address() can run
    without real filesystem/DB access. Applied autouse so tests don't need
    to accept the fixture explicitly.
    """
    with patch('fake_info.DB') as mock_db, \
         patch('builtins.open', create=True), \
         patch('json.load') as mock_json_load:

        # Provide minimal persons list so _set_full_name_and_gender works
        mock_json_load.return_value = {
            'persons': [
                {'firstName': 'John', 'lastName': 'Doe', 'gender': 'male'},
                {'firstName': 'Jane', 'lastName': 'Doe', 'gender': 'female'}
            ]
        }

        # DB: fixed town/postal code
        mock_db_instance = MagicMock()
        mock_db_instance.get_random_town.return_value = {
            'postal_code': '1970',
            'town_name': 'Frederiksberg'
        }
        mock_db.return_value = mock_db_instance

        yield


# ========== BLACK-BOX TESTS ==========

class TestGetFakePersonBlackBox:
    """Black-box tests using Equivalence Partitioning (EP)"""

    def test_returns_dict(self):
        """EP1: Returns a dictionary with all required fields"""
        fake = FakeInfo()
        result = fake.get_fake_person()
        assert isinstance(result, dict), f"Expected dict, got {type(result).__name__}"

    def test_contains_all_required_keys(self):
        """EP1: Dict contains all 7 required keys"""
        fake = FakeInfo()
        result = fake.get_fake_person()
        required_keys = {'CPR', 'firstName', 'lastName', 'gender', 'birthDate', 'address', 'phoneNumber'}
        actual_keys = set(result.keys())
        assert actual_keys == required_keys, \
            f"Missing keys: {required_keys - actual_keys}, Extra keys: {actual_keys - required_keys}"

    def test_cpr_format_valid(self):
        """EP2: CPR has valid format (10 digits)"""
        for _ in range(10):
            fake = FakeInfo()
            result = fake.get_fake_person()
            assert re.match(r'^\d{10}$', result['CPR']), \
                f"CPR '{result['CPR']}' does not match format (10 digits)"

    def test_gender_is_valid(self):
        """EP2: Gender is either 'female' or 'male'"""
        for _ in range(10):
            fake = FakeInfo()
            result = fake.get_fake_person()
            assert result['gender'] in ['female', 'male'], \
                f"Gender '{result['gender']}' is not 'female' or 'male'"

    def test_birth_date_format_valid(self):
        """EP2: BirthDate has format YYYY-MM-DD"""
        for _ in range(10):
            fake = FakeInfo()
            result = fake.get_fake_person()
            assert re.match(r'^\d{4}-\d{2}-\d{2}$', result['birthDate']), \
                f"BirthDate '{result['birthDate']}' does not match YYYY-MM-DD format"

    def test_names_not_empty(self):
        """EP2: First name and last name are not empty"""
        for _ in range(10):
            fake = FakeInfo()
            result = fake.get_fake_person()
            assert len(result['firstName']) > 0, "firstName should not be empty"
            assert len(result['lastName']) > 0, "lastName should not be empty"

    def test_phone_format_valid(self):
        """EP2: Phone number has valid format (8 digits)"""
        for _ in range(10):
            fake = FakeInfo()
            result = fake.get_fake_person()
            assert re.match(r'^\d{8}$', result['phoneNumber']), \
                f"phoneNumber '{result['phoneNumber']}' does not match format (8 digits)"

    def test_address_structure_valid(self):
        """EP2: Address has correct structure (nested dict with required keys)"""
        fake = FakeInfo()
        result = fake.get_fake_person()

        # Check address is dict
        assert isinstance(result['address'], dict), \
            f"Address should be dict, got {type(result['address']).__name__}"

        # Check all required address keys
        address_keys = {'street', 'number', 'floor', 'door', 'postal_code', 'town_name'}
        actual_address_keys = set(result['address'].keys())
        assert actual_address_keys == address_keys, \
            f"Address missing keys: {address_keys - actual_address_keys}"

    def test_values_match_instance_attributes(self):
        """EP3: Dict values match instance attributes"""
        fake = FakeInfo()
        result = fake.get_fake_person()

        assert result['CPR'] == fake.cpr
        assert result['firstName'] == fake.first_name
        assert result['lastName'] == fake.last_name
        assert result['gender'] == fake.gender
        assert result['birthDate'] == fake.birth_date
        assert result['address'] == fake.address
        assert result['phoneNumber'] == fake.phone_number


# ========== WHITE-BOX TESTS ==========

class TestGetFakePersonWhiteBox:
    """White-box tests for Statement and Decision Coverage"""

    def test_statement_coverage_all_lines_executed(self):
        """
        White-box Statement Coverage: All lines in get_fake_person() executed

        Lines covered:
        - return {
        - 'CPR': self.cpr,
        - 'firstName': self.first_name,
        - ... (all dict entries)
        - }
        """
        fake = FakeInfo()
        result = fake.get_fake_person()

        # Verify all lines were executed (dict created and returned)
        assert result is not None
        assert isinstance(result, dict)
        assert len(result) == 7

    def test_decision_coverage_no_branches(self):
        """
        White-box Decision Coverage: No conditional branches in get_fake_person()

        The method has no if/else statements, so decision coverage = statement coverage.
        This test documents that fact.
        """
        fake = FakeInfo()
        result = fake.get_fake_person()
        assert isinstance(result, dict), "Method should always return a dict"


# ========== EDGE CASE TESTS ==========

class TestGetFakePersonEdgeCases:
    """Edge case tests for unusual but valid scenarios"""

    def test_all_string_values_are_non_empty(self):
        """Edge case: All string fields are non-empty"""
        for _ in range(10):
            fake = FakeInfo()
            result = fake.get_fake_person()

            assert len(result['CPR']) > 0, "CPR should not be empty"
            assert len(result['firstName']) > 0, "firstName should not be empty"
            assert len(result['lastName']) > 0, "lastName should not be empty"
            assert len(result['gender']) > 0, "gender should not be empty"
            assert len(result['birthDate']) > 0, "birthDate should not be empty"
            assert len(result['phoneNumber']) > 0, "phoneNumber should not be empty"

    def test_stress_test_many_persons(self):
        """Stress test: Generate many persons and verify consistency"""
        persons = []
        for _ in range(100):
            fake = FakeInfo()
            person = fake.get_fake_person()
            persons.append(person)

        # All should be valid dicts
        assert all(isinstance(p, dict) for p in persons), \
            "All results should be dictionaries"
        assert all(len(p) == 7 for p in persons), \
            "All results should have exactly 7 keys"

        # Verify uniqueness (persons should be different)
        unique_cprs = len({p['CPR'] for p in persons})
        assert unique_cprs > 90, \
            f"Only {unique_cprs} unique CPRs out of 100 persons (expected >90)"
