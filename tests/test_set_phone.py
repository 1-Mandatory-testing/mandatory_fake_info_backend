"""
Unit tests for FakeInfo class - _set_phone() method
Test Designer: Asbjørn

Black-box techniques: Equivalence Partitioning (EP), Boundary Value Analysis (BVA)
White-box techniques: Statement Coverage, Decision Coverage
"""

import pytest
from fake_info import FakeInfo

# ========== TEST DATA ==========

# Prefix lengths for BVA testing
PREFIX_LENGTHS = ('prefix_length', [1, 2, 3])  # Min, Middle, Max


# ========== BLACK-BOX TESTS ==========

class TestSetPhoneBlackBox:
    """Black-box tests using Equivalence Partitioning (EP) and Boundary Value Analysis (BVA)"""
    
    def test_ep1_phone_length_always_8(self):
        """
        EP1: Phone number length is always 8 digits
        Tests that total length (prefix + suffix) = 8
        """
        for _ in range(50):  # Multiple runs due to randomness
            fake = FakeInfo()
            assert len(fake.phone_number) == 8, \
                f"Phone number '{fake.phone_number}' length is not 8"
    
    def test_ep2_phone_only_numeric(self):
        """
        EP2: Phone number contains only numeric digits (0-9)
        Tests character validity
        """
        for _ in range(50):
            fake = FakeInfo()
            assert fake.phone_number.isdigit(), \
                f"Phone number '{fake.phone_number}' contains non-numeric characters"
    
    def test_ep3_phone_starts_with_valid_prefix(self):
        """
        EP3: Phone number starts with a valid prefix from PHONE_PREFIXES
        Tests prefix validity
        """
        for _ in range(50):
            fake = FakeInfo()
            # Check if phone starts with any valid prefix
            valid_prefix_found = any(
                fake.phone_number.startswith(prefix) 
                for prefix in FakeInfo.PHONE_PREFIXES
            )
            assert valid_prefix_found, \
                f"Phone number '{fake.phone_number}' does not start with a valid prefix"
            
    PREFIX_LENGTHS = ('prefix_length', [1, 2, 3])  # Min, Middle, Max
    
    @pytest.mark.parametrize(*PREFIX_LENGTHS)
    def test_bva_prefix_lengths(self, prefix_length):
        """
        BVA: Test all prefix length categories (1, 2, 3 digits)
        Ensures correct suffix length calculation for each prefix length
        """
        prefixes_by_length = {
            1: [p for p in FakeInfo.PHONE_PREFIXES if len(p) == 1],
            2: [p for p in FakeInfo.PHONE_PREFIXES if len(p) == 2],
            3: [p for p in FakeInfo.PHONE_PREFIXES if len(p) == 3],
        }
        
        # Generate multiple phones to likely hit this prefix length
        found_matching_prefix = False
        for _ in range(100):  # Increased iterations for better coverage
            fake = FakeInfo()
            # Check if this phone uses a prefix of target length
            for prefix in prefixes_by_length[prefix_length]:
                if fake.phone_number.startswith(prefix):
                    found_matching_prefix = True
                    # Verify correct total length
                    assert len(fake.phone_number) == 8
                    # Verify suffix length calculation
                    expected_suffix_length = 8 - prefix_length
                    actual_suffix = fake.phone_number[len(prefix):]
                    assert len(actual_suffix) == expected_suffix_length, \
                        f"Prefix '{prefix}' (len={prefix_length}), suffix '{actual_suffix}' " \
                        f"(len={len(actual_suffix)}), expected suffix len={expected_suffix_length}"
                    break
            
            if found_matching_prefix:
                break
        
        # With 100 iterations, we should find at least one example
        assert found_matching_prefix, \
            f"Could not find phone number with prefix length {prefix_length} in 100 attempts"
    
    def test_ep4_phone_suffix_is_random(self):
        """
        EP4: Suffix digits are random (different calls produce different results)
        Tests randomness by generating multiple phones and checking for variation
        """
        phone_numbers = set()
        for _ in range(50):
            fake = FakeInfo()
            phone_numbers.add(fake.phone_number)
        
        # With 50 calls, we should have many unique phone numbers
        # (Theoretically could have duplicates, but very unlikely)
        assert len(phone_numbers) > 40, \
            f"Only {len(phone_numbers)} unique phone numbers in 50 generations (expected >40)"


# ========== WHITE-BOX TESTS ==========

class TestSetPhoneWhiteBox:
    """White-box tests for Statement Coverage and Decision Coverage"""
    
    def test_statement_coverage_all_lines_executed(self):
        """
        White-box Statement Coverage: Ensure all code lines are executed
        
        Covers:
        - random.choice(PHONE_PREFIXES)
        - remaining_digits calculation
        - suffix generation loop
        - phone_number assignment
        """
        fake = FakeInfo()
        
        # Verify phone_number was set
        assert hasattr(fake, 'phone_number')
        assert len(fake.phone_number) == 8
        assert fake.phone_number.isdigit()
    
    def test_decision_coverage_no_branches(self):
        """
        White-box Decision Coverage: No conditional branches in _set_phone()
        
        The method has no if/else statements, so decision coverage = statement coverage
        This test documents that fact.
        """
        # The code has no branches:
        # - No if statements
        # - No loops with conditions (range() is deterministic)
        # - No try/except blocks
        
        fake = FakeInfo()
        assert hasattr(fake, 'phone_number')


# ========== EDGE CASE TESTS ==========

class TestSetPhoneEdgeCases:
    """Edge case tests for boundary and stress scenarios"""
    
    def test_edge_case_shortest_prefix(self):
        """
        Edge case: Shortest prefix (1 digit) produces longest suffix (7 digits)
        Tests minimum prefix length boundary
        """
        # Find phone with 1-digit prefix
        found = False
        for _ in range(100):
            fake = FakeInfo()
            one_digit_prefixes = [p for p in FakeInfo.PHONE_PREFIXES if len(p) == 1]
            for prefix in one_digit_prefixes:
                if fake.phone_number.startswith(prefix):
                    # Verify suffix is 7 digits
                    suffix = fake.phone_number[1:]
                    assert len(suffix) == 7, f"1-digit prefix should have 7-digit suffix"
                    assert suffix.isdigit()
                    found = True
                    break
            if found:
                break
        
        assert found, "Could not generate phone with 1-digit prefix"
    
    def test_edge_case_longest_prefix(self):
        """
        Edge case: Longest prefix (3 digits) produces shortest suffix (5 digits)
        Tests maximum prefix length boundary
        """
        # Find phone with 3-digit prefix
        found = False
        for _ in range(100):
            fake = FakeInfo()
            three_digit_prefixes = [p for p in FakeInfo.PHONE_PREFIXES if len(p) == 3]
            for prefix in three_digit_prefixes:
                if fake.phone_number.startswith(prefix):
                    # Verify suffix is 5 digits
                    suffix = fake.phone_number[3:]
                    assert len(suffix) == 5, f"3-digit prefix should have 5-digit suffix"
                    assert suffix.isdigit()
                    found = True
                    break
            if found:
                break
        
        assert found, "Could not generate phone with 3-digit prefix"
    
    def test_stress_test_generate_many_phones(self):
        """
        Stress test: Generate many phone numbers to verify stability
        Tests that method doesn't crash or produce invalid data at scale
        """
        phone_numbers = []
        for _ in range(1000):
            fake = FakeInfo()
            phone_numbers.append(fake.phone_number)
        
        # All should be 8 digits
        assert all(len(phone) == 8 for phone in phone_numbers)
        # All should be numeric
        assert all(phone.isdigit() for phone in phone_numbers)
        # Should have high uniqueness
        unique_count = len(set(phone_numbers))
        assert unique_count > 950, f"Only {unique_count} unique phones out of 1000"
    
    def test_prefix_distribution_reasonable(self):
        """
        Statistical test: All prefix lengths should appear in large sample
        Verifies that random.choice() produces reasonable distribution
        """
        prefix_length_counts = {1: 0, 2: 0, 3: 0}
        
        for _ in range(300):
            fake = FakeInfo()
            # Determine prefix length
            for length in [3, 2, 1]:  # Check longest first to avoid false matches
                prefixes = [p for p in FakeInfo.PHONE_PREFIXES if len(p) == length]
                for prefix in prefixes:
                    if fake.phone_number.startswith(prefix):
                        prefix_length_counts[length] += 1
                        break
                else:
                    continue
                break
        
        # All lengths should appear at least once in 300 generations
        assert prefix_length_counts[1] > 0, "No 1-digit prefixes found"
        assert prefix_length_counts[2] > 0, "No 2-digit prefixes found"
        assert prefix_length_counts[3] > 0, "No 3-digit prefixes found"
        
        # No length should dominate completely (basic sanity check)
        assert prefix_length_counts[1] < 280, "1-digit prefixes dominate (>93%)"
        assert prefix_length_counts[2] < 280, "2-digit prefixes dominate (>93%)"
        assert prefix_length_counts[3] < 280, "3-digit prefixes dominate (>93%)"