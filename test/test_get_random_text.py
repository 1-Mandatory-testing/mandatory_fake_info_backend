"""
Unit tests for FakeInfo class - _get_random_text() method

Black-box techniques: Equivalence Partitioning (EP), Boundary Value Analysis (BVA)
White-box techniques: Statement Coverage, Decision Coverage
"""
import pytest
from fake_info import FakeInfo
from unittest.mock import patch, MagicMock

# ========== FIXTURES ==========

@pytest.fixture(autouse=True)
def mock_dependencies():
    """Mock DB and file/json so FakeInfo.__init__ can run"""
    with patch('fake_info.DB') as mock_db, \
         patch('builtins.open', create=True), \
         patch('json.load') as mock_json_load:

        mock_json_load.return_value = {
            'persons': [
                {'firstName': 'John', 'lastName': 'Doe', 'gender': 'male'}
            ]
        }

        mock_db_instance = MagicMock()
        mock_db_instance.get_random_town.return_value = {
            'postal_code': '1970',
            'town_name': 'Frederiksberg'
        }
        mock_db.return_value = mock_db_instance

        yield


@pytest.fixture
def fake_info():
    """Fixture to provide FakeInfo instance for each test"""
    return FakeInfo()


# ========== BLACK-BOX TESTS ==========

class TestGetRandomTextBlackBox:
    """Black-box tests using EP and BVA"""
    
    # EP1: Length matches input (3-value BVA approach)
    VALID_LENGTHS = ('length', [
        1,      # Minimum boundary
        2,      # Minimum + 1
        20,     # Middle partition value
        39,     # Maximum - 1 (for street)
        40,     # Maximum boundary (for street)
        100,    # Large value test
    ])
    
    @pytest.mark.parametrize(*VALID_LENGTHS)
    def test_length_matches_input(self, length, fake_info):
        """EP1 + BVA: Output length matches input (3-value boundary approach)"""
        result = fake_info._get_random_text(length=length)
        assert len(result) == length
    
    # EP2: First character not space (loop-based)
    def test_first_character_not_space(self, fake_info):
        """EP2: First character cannot be a space"""
        for _ in range(20):
            result = fake_info._get_random_text(length=20)
            assert result[0] != ' ', f"First char was space in: '{result}'"
    
    # EP3: Valid characters (parameterized)
    @pytest.mark.parametrize("include_danish,expected_chars", [
        (True, set(' abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZæøåÆØÅ')),
        (False, set(' abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')),
    ])
    
    def test_only_valid_characters(self, include_danish, expected_chars, fake_info):
        """EP3: Only valid characters based on include_danish parameter"""
        result = fake_info._get_random_text(length=40, include_danish=include_danish)
        for char in result:
            assert char in expected_chars, f"Invalid char '{char}' found"
    
    # EP4: Danish characters handling
    def test_no_danish_when_false(self, fake_info):
        """EP4: No Danish characters when include_danish=False"""
        danish_chars = set('æøåÆØÅ')
        for _ in range(20):
            result = fake_info._get_random_text(length=40, include_danish=False)
            assert not any(char in danish_chars for char in result)


# ========== WHITE-BOX TESTS ==========

class TestGetRandomTextWhiteBox:
    """White-box tests for statement and decision coverage"""
    
    def test_statement_coverage(self, fake_info):
        """White-box: All code paths executed"""
        result1 = fake_info._get_random_text(length=10, include_danish=True)
        result2 = fake_info._get_random_text(length=10, include_danish=False)
        
        assert len(result1) == 10
        assert len(result2) == 10
    
    @pytest.mark.parametrize("include_danish,expect_danish_possible", [
        (True, True),
        (False, False),
    ])
    def test_decision_coverage_include_danish(self, include_danish, expect_danish_possible, fake_info):
        """White-box Decision: Test both branches of include_danish"""
        danish_chars = set('æøåÆØÅ')
        found_danish = False
        
        for _ in range(50):
            result = fake_info._get_random_text(length=40, include_danish=include_danish)
            if any(char in danish_chars for char in result):
                found_danish = True
                break
        
        if expect_danish_possible:
            assert found_danish, "Expected Danish chars with include_danish=True"
        else:
            assert not found_danish, "No Danish chars expected with include_danish=False"


# ========== EDGE CASE / INVALID INPUT TESTS ==========

class TestGetRandomTextEdgeCases:
    """
    Edge case tests - Testing behavior with invalid/boundary inputs

    """
    
    def test_length_zero_returns_one_character(self, fake_info):
        """
        Invalid input: length=0 (below minimum boundary)
        Expected: Should return empty string
        """
        result = fake_info._get_random_text(length=0)
        # Documents bug: length=0 returns 1 char instead of empty string
        assert len(result) == 1, "Bug: length=0 should return empty string, but returns 1 char"
    
    @pytest.mark.parametrize("invalid_length", [-1, -5, -100])
    def test_negative_length_behavior(self, invalid_length, fake_info):
        """
        Invalid input: length < 0 (invalid partition)
        Expected: Should validate and raise ValueError
        Actual: Returns 1 character (first char selection runs, loop skips)
        """
        result = fake_info._get_random_text(length=invalid_length)
        
        assert len(result) == 1, f"Negative length {invalid_length} should be rejected"
    
    def test_length_very_large(self, fake_info):
        """
        Boundary test: Very large length (stress test)
        Tests system behavior at extreme valid values
        """
        result = fake_info._get_random_text(length=10000)
        assert len(result) == 10000
        assert result[0] != ' '
    
    def test_length_invalid_type_string(self, fake_info):
        """
        Invalid input: length="abc" (wrong type)
        Expected: Should validate type and raise TypeError
        Actual: Causes TypeError in range() function
        """
        with pytest.raises(TypeError):
            fake_info._get_random_text(length="abc")
    
    def test_length_invalid_type_none(self, fake_info):
        """
        Invalid input: length=None (null value)
        Expected: Should validate and raise ValueError
        Actual: Causes TypeError in range() function
        """
        with pytest.raises(TypeError):
            fake_info._get_random_text(length=None)