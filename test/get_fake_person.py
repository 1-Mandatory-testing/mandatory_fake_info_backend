"""
Unit tests for FakeInfo class - get_fake_person() method
Test Designer: [Dit navn]

Black-box techniques: Equivalence Partitioning (EP)
White-box techniques: Statement Coverage, Decision Coverage
"""

import pytest
from unittest.mock import patch, MagicMock
from fake_info import FakeInfo


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
                {'firstName': 'Hugo', 'lastName': 'Ekitike', 'gender': 'male'},
                {'firstName': 'Pernille', 'lastName': 'Harder', 'gender': 'female'}
            ]
        }

        # DB: fixed town/postal code
        mock_db_instance = MagicMock()
        mock_db_instance.get_random_town.return_value = {
            'postal_code': '2100',
            'town_name': 'København Ø'
        }
        mock_db.return_value = mock_db_instance

        yield


# ========== BLACK-BOX TESTS ==========

class TestGetFakePersonBlackBox:
    """Black-box tests using Equivalence Partitioning (EP)"""
    
    def test_ep1_returns_dict(self):
        fake = FakeInfo()
        result = fake.get_fake_person()
        assert isinstance(result, dict), f"Expected dict, got {type(result).__name__}"
    
    def test_ep2_contains_all_required_keys(self):
        fake = FakeInfo()
        result = fake.get_fake_person()
        required_keys = {'CPR', 'firstName', 'lastName', 'gender', 'birthDate', 'address', 'phoneNumber'}
        actual_keys = set(result.keys())
        assert actual_keys == required_keys, f"Missing keys: {required_keys - actual_keys}, Extra keys: {actual_keys - required_keys}"
    
    def test_ep3_values_match_instance_attributes(self):
        fake = FakeInfo()
        result = fake.get_fake_person()
        assert result['CPR'] == fake.cpr, f"CPR mismatch: expected '{fake.cpr}', got '{result['CPR']}'"
        assert result['firstName'] == fake.first_name, f"firstName mismatch: expected '{fake.first_name}', got '{result['firstName']}'"
        assert result['lastName'] == fake.last_name, f"lastName mismatch: expected '{fake.last_name}', got '{result['lastName']}'"
        assert result['gender'] == fake.gender, f"gender mismatch: expected '{fake.gender}', got '{result['gender']}'"
        assert result['birthDate'] == fake.birth_date, f"birthDate mismatch: expected '{fake.birth_date}', got '{result['birthDate']}'"
        assert result['address'] == fake.address, f"address mismatch: expected '{fake.address}', got '{result['address']}'"
        assert result['phoneNumber'] == fake.phone_number, f"phoneNumber mismatch: expected '{fake.phone_number}', got '{result['phoneNumber']}'"
    
    def test_ep4_address_is_nested_dict(self):
        fake = FakeInfo()
        result = fake.get_fake_person()
        assert isinstance(result['address'], dict), f"Address should be dict, got {type(result['address']).__name__}"
        address_keys = {'street', 'number', 'floor', 'door', 'postal_code', 'town_name'}
        actual_address_keys = set(result['address'].keys())
        assert actual_address_keys == address_keys, f"Address missing keys: {address_keys - actual_address_keys}"
    
    def test_ep5_cpr_is_string(self):
        fake = FakeInfo()
        result = fake.get_fake_person()
        assert isinstance(result['CPR'], str), f"CPR should be string, got {type(result['CPR']).__name__}"
        assert len(result['CPR']) == 10, f"CPR should be 10 characters, got {len(result['CPR'])}"
    
    def test_ep6_phone_number_is_string(self):
        fake = FakeInfo()
        result = fake.get_fake_person()
        assert isinstance(result['phoneNumber'], str), f"phoneNumber should be string, got {type(result['phoneNumber']).__name__}"
        assert len(result['phoneNumber']) == 8, f"phoneNumber should be 8 characters, got {len(result['phoneNumber'])}"


# ========== WHITE-BOX TESTS ==========

class TestGetFakePersonWhiteBox:
    def test_statement_coverage_all_lines_executed(self):
        fake = FakeInfo()
        result = fake.get_fake_person()
        assert result is not None
        assert isinstance(result, dict)
        assert len(result) == 7
    
    def test_decision_coverage_no_branches(self):
        fake = FakeInfo()
        result = fake.get_fake_person()
        assert isinstance(result, dict), "Method should always return a dict"


# ========== EDGE CASE TESTS ==========

class TestGetFakePersonEdgeCases:
    def test_all_string_values_are_non_empty(self):
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
        persons = []
        for _ in range(100):
            fake = FakeInfo()
            person = fake.get_fake_person()
            persons.append(person)
        assert all(isinstance(p, dict) for p in persons), "All results should be dictionaries"
        assert all(len(p) == 7 for p in persons), "All results should have exactly 7 keys"
        unique_cprs = len(set(p['CPR'] for p in persons))
        assert unique_cprs > 90, f"Only {unique_cprs} unique CPRs out of 100 persons (expected >90)"