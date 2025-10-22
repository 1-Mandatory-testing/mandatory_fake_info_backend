import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock
from fake_info import FakeInfo  

@pytest.fixture
def mock_dependencies():
    """Mock all external dependencies for FakeInfo"""
    with patch('fake_info.DB') as mock_db, \
         patch('builtins.open', create=True), \
         patch('json.load') as mock_json_load:
        
        mock_json_load.return_value = {
            'persons': [
                {'firstName': 'Hugo', 'lastName': 'Ekitike', 'gender': 'male'},
                {'firstName': 'Pernille', 'lastName': 'Harder', 'gender': 'female'} 
            ]
        }
        
        mock_db_instance = MagicMock()
        mock_db_instance.get_random_town.return_value = {
            'postal_code': '1000',
            'town_name': 'København'
        }
        mock_db.return_value = mock_db_instance
        
        yield

class TestSetCPR:
    """Tests for _set_cpr() method"""
    
    # ==================== BLACK-BOX TESTS - Equivalence Partitioning ====================
    
    def test_cpr_format_10_digits(self, mock_dependencies):
        """EP1: CPR format (10 digits, all numeric)"""
        person = FakeInfo()
        
        assert len(person.cpr) == 10
        assert person.cpr.isdigit()      
    
    def test_cpr_date_part_matches_birth_date(self, mock_dependencies):
        """EP2: Date part of CPR matches birth_date"""
        person = FakeInfo()
        dd = person.cpr[0:2]
        mm = person.cpr[2:4]
        yy = person.cpr[4:6]

        formatted_birthdate = datetime.strptime(person.birth_date, "%Y-%m-%d")
        birth_dd = formatted_birthdate.strftime("%d")
        birth_mm = formatted_birthdate.strftime("%m")
        birth_yy = formatted_birthdate.strftime("%y")
        assert dd == birth_dd
        assert mm == birth_mm
        assert yy == birth_yy
    
    def test_cpr_middle_digits_are_3_digits(self, mock_dependencies):
        """EP3: Middle 3 digits exist (position 6-8)"""

        person = FakeInfo()
        middle_digits = person.cpr[6:9]
        assert len(middle_digits) == 3
        assert middle_digits.isdigit()
    
    def test_cpr_last_digit_even_for_female(self, mock_dependencies):
        """EP4: Last digit is even for female"""
        found_female = False
        for x in range(50):
            person = FakeInfo()
            if person.gender == FakeInfo.GENDER_FEMININE:
                found_female = True
                last_digit = int(person.cpr[-1])
                assert last_digit % 2 == 0
        assert found_female, "Test did not encounter any female persons"

    
    def test_cpr_last_digit_odd_for_male(self, mock_dependencies):
        """EP5: Last digit is odd for male"""
        found_male = False
        for x in range(50):
            person = FakeInfo()
            if person.gender == FakeInfo.GENDER_MASCULINE:
                found_male = True
                last_digit = int(person.cpr[-1])
                assert last_digit % 2 == 1
        assert found_male, "Test did not encounter any male persons"


    # # ==================== BLACK-BOX TESTS - Boundary Value Analysis ====================
#   No boundaries to test in this case, since it doesnt take input parameters and it is random
#   so EP tests cover the necessary cases.

    # # ==================== WHITE-BOX TESTS - Decision Coverage ====================
    
    @pytest.mark.parametrize("gender, initial_digit, expected_digit", [
        (FakeInfo.GENDER_FEMININE, 1, 2),
        (FakeInfo.GENDER_FEMININE, 2, 2),  
        (FakeInfo.GENDER_MASCULINE, 2, 3), 
        (FakeInfo.GENDER_MASCULINE, 3, 3), 
    ])
    def test_cpr_whitebox_final_digit_logic(self, mock_dependencies, gender, initial_digit, expected_digit):
        """White-box: Test all 4 decision branches for final_digit logic"""
        person = FakeInfo()
        person.gender = gender
        person.birth_date = "2000-07-13"
        with patch('random.randint', side_effect=[initial_digit, 1, 2, 3]):
            person._set_cpr()
            assert int(person.cpr[-1]) == expected_digit
    
    
    #  Technically this these tests are already covered by the EP tests above, but we put them here for just 
    #  clarity that all statements are executed.
    def test_cpr_whitebox_statement_coverage(self, mock_dependencies):
        """White-box: Verify all statements execute (date parsing, middle_digits, final assignment)"""
        person = FakeInfo()
        person.birth_date = "1985-03-21"
        person.gender = FakeInfo.GENDER_FEMININE
        
        with patch('fake_info.random.randint', side_effect=[4, 7, 8, 9]):  
            person._set_cpr()
        
        assert person.cpr is not None
        assert len(person.cpr) == 10
        assert person.cpr[:6] == "210385" 
        assert person.cpr[6:9] == "789"    
        assert person.cpr[9] == "4" 