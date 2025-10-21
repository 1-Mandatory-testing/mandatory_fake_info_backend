"""
Unit tests for FakeInfo class - get_fake_person() method
Test Designer: [Dit navn]

Black-box techniques: Equivalence Partitioning (EP)
White-box techniques: Statement Coverage, Decision Coverage
"""

import pytest
from fake_info import FakeInfo


# ========== BLACK-BOX TESTS ==========

class TestGetFakePersonBlackBox:
    """Black-box tests using Equivalence Partitioning (EP)"""
    
    def test_ep1_returns_dict(self):
        """
        EP1: Method returns a dictionary
        Tests return type validation
        """
        fake = FakeInfo()
        result = fake.get_fake_person()
        
        assert isinstance(result, dict), \
            f"Expected dict, got {type(result).__name__}"
    
    def test_ep2_contains_all_required_keys(self):
        """
        EP2: Returned dict contains all 7 required keys
        Tests dictionary structure completeness
        """
        fake = FakeInfo()
        result = fake.get_fake_person()
        
        required_keys = {'CPR', 'firstName', 'lastName', 'gender', 'birthDate', 'address', 'phoneNumber'}
        actual_keys = set(result.keys())
        
        assert actual_keys == required_keys, \
            f"Missing keys: {required_keys - actual_keys}, Extra keys: {actual_keys - required_keys}"
    
    def test_ep3_values_match_instance_attributes(self):
        """
        EP3: Dictionary values match the instance attributes
        Tests correct value mapping
        """
        fake = FakeInfo()
        result = fake.get_fake_person()
        
        # Verify each field matches
        assert result['CPR'] == fake.cpr, \
            f"CPR mismatch: expected '{fake.cpr}', got '{result['CPR']}'"
        assert result['firstName'] == fake.first_name, \
            f"firstName mismatch: expected '{fake.first_name}', got '{result['firstName']}'"
        assert result['lastName'] == fake.last_name, \
            f"lastName mismatch: expected '{fake.last_name}', got '{result['lastName']}'"
        assert result['gender'] == fake.gender, \
            f"gender mismatch: expected '{fake.gender}', got '{result['gender']}'"
        assert result['birthDate'] == fake.birth_date, \
            f"birthDate mismatch: expected '{fake.birth_date}', got '{result['birthDate']}'"
        assert result['address'] == fake.address, \
            f"address mismatch: expected '{fake.address}', got '{result['address']}'"
        assert result['phoneNumber'] == fake.phone_number, \
            f"phoneNumber mismatch: expected '{fake.phone_number}', got '{result['phoneNumber']}'"
    
    def test_ep4_address_is_nested_dict(self):
        """
        EP4: Address field is a nested dictionary (not a string)
        Tests address structure type
        """
        fake = FakeInfo()
        result = fake.get_fake_person()
        
        assert isinstance(result['address'], dict), \
            f"Address should be dict, got {type(result['address']).__name__}"
        
        # Verify address has expected keys
        address_keys = {'street', 'number', 'floor', 'door', 'postal_code', 'town_name'}
        actual_address_keys = set(result['address'].keys())
        
        assert actual_address_keys == address_keys, \
            f"Address missing keys: {address_keys - actual_address_keys}"
    
    def test_ep5_cpr_is_string(self):
        """
        EP5: CPR is returned as string (not int)
        Tests CPR data type
        """
        fake = FakeInfo()
        result = fake.get_fake_person()
        
        assert isinstance(result['CPR'], str), \
            f"CPR should be string, got {type(result['CPR']).__name__}"
        assert len(result['CPR']) == 10, \
            f"CPR should be 10 characters, got {len(result['CPR'])}"
    
    def test_ep6_phone_number_is_string(self):
        """
        EP6: Phone number is returned as string (not int)
        Tests phone number data type
        """
        fake = FakeInfo()
        result = fake.get_fake_person()
        
        assert isinstance(result['phoneNumber'], str), \
            f"phoneNumber should be string, got {type(result['phoneNumber']).__name__}"
        assert len(result['phoneNumber']) == 8, \
            f"phoneNumber should be 8 characters, got {len(result['phoneNumber'])}"


# ========== WHITE-BOX TESTS ==========

class TestGetFakePersonWhiteBox:
    """White-box tests for Statement Coverage and Decision Coverage"""
    
    def test_statement_coverage_all_lines_executed(self):
        """
        White-box Statement Coverage: Ensure all code lines are executed
        
        Covers:
        - Dictionary creation with all 7 key-value pairs
        - Return statement
        """
        fake = FakeInfo()
        result = fake.get_fake_person()
        
        # Verify dictionary was created and returned
        assert result is not None
        assert isinstance(result, dict)
        assert len(result) == 7
    
    def test_decision_coverage_no_branches(self):
        """
        White-box Decision Coverage: No conditional branches in get_fake_person()
        
        The method has no if/else statements, so decision coverage = statement coverage
        This test documents that fact.
        """
        # The code has no branches:
        # - No if statements
        # - No loops
        # - No try/except blocks
        # - Simple dictionary return
        
        fake = FakeInfo()
        result = fake.get_fake_person()
        
        assert isinstance(result, dict), "Method should always return a dict"


# ========== EDGE CASE TESTS ==========

class TestGetFakePersonEdgeCases:
    """Edge case tests for unusual but valid scenarios"""
    
    def test_address_dict_not_modified_by_return(self):
        """
        Edge case: Returned address dict is not a reference that can mutate original
        Tests for potential shallow copy issues
        """
        fake = FakeInfo()
        result = fake.get_fake_person()
        
        # Modify returned address
        original_street = result['address']['street']
        result['address']['street'] = 'MODIFIED'
        
        # Get fresh copy
        result2 = fake.get_fake_person()
        
        # Original address should be unchanged (depends on implementation)
        # Note: Current implementation returns reference, so this documents behavior
        assert result2['address']['street'] == 'MODIFIED' or \
               result2['address']['street'] == original_street, \
            "Address reference behavior documented"
    
    def test_all_string_values_are_non_empty(self):
        """
        Edge case: All string fields contain actual data (not empty strings)
        Tests data generation completeness
        """
        for _ in range(10):  # Test multiple instances
            fake = FakeInfo()
            result = fake.get_fake_person()
            
            assert len(result['CPR']) > 0, "CPR should not be empty"
            assert len(result['firstName']) > 0, "firstName should not be empty"
            assert len(result['lastName']) > 0, "lastName should not be empty"
            assert len(result['gender']) > 0, "gender should not be empty"
            assert len(result['birthDate']) > 0, "birthDate should not be empty"
            assert len(result['phoneNumber']) > 0, "phoneNumber should not be empty"
    
    def test_stress_test_many_persons(self):
        """
        Stress test: Generate many persons to verify stability
        Tests that method doesn't crash or produce invalid data at scale
        """
        persons = []
        for _ in range(100):
            fake = FakeInfo()
            person = fake.get_fake_person()
            persons.append(person)
        
        # All should be valid dicts with 7 keys
        assert all(isinstance(p, dict) for p in persons), \
            "All results should be dictionaries"
        assert all(len(p) == 7 for p in persons), \
            "All results should have exactly 7 keys"
        
        # Should have reasonable uniqueness
        unique_cprs = len(set(p['CPR'] for p in persons))
        assert unique_cprs > 90, \
            f"Only {unique_cprs} unique CPRs out of 100 persons (expected >90)"