import pytest
from datetime import datetime
from fake_info import FakeInfo  
from unittest.mock import patch, MagicMock


@pytest.fixture
def mock_dependencies():
    """Mock all external dependencies for FakeInfo"""
    with patch('fake_info.DB') as mock_db, \
         patch('builtins.open', create=True), \
         patch('json.load') as mock_json_load:
        
        mock_json_load.return_value = {
            'persons': [
                {'firstName': 'Hugo', 'lastName': 'Ekitike', 'gender': 'male'}
            ]
        }
        
        mock_db_instance = MagicMock()
        mock_db_instance.get_random_town.return_value = {
            'postal_code': '1000',
            'town_name': 'København'
        }
        mock_db.return_value = mock_db_instance
        
        yield

class TestSetBirthDate:
    """Tests for _set_birth_date() method"""
    
    # ==================== BLACK-BOX TESTS - Equivalence Partitioning ====================

    def test_year_valid_range_middle_value(self, mock_dependencies):
        """EP1: Test year in valid range (middle value: 1980)"""
        person = FakeInfo()
        
        for _ in range(100):
            person._set_birth_date()
            year = int(person.birth_date.split('-')[0])
            assert 1900 <= year <= datetime.now().year
    

    def test_month_valid_range_middle_value(self, mock_dependencies):
        """EP2: Test month in valid range (middle value: 6)"""
        person = FakeInfo() 
        for _ in range(100):
            person._set_birth_date()
            month = int(person.birth_date.split('-')[1])
            assert 1 <= month <= 12
            
    
    def test_days_for_31_day_months(self, mock_dependencies):
        """EP3: Test days for months with 31 days (January)"""

        person = FakeInfo()
        months_with_31_days = [1, 3, 5, 7, 8, 10, 12]
        found_31_day_month = False

        for _ in range(50):
            person._set_birth_date()
            year, month, day = map(int, person.birth_date.split('-'))
            if (month in months_with_31_days ):
                found_31_day_month = True
                assert 1 <= day <= 31
        assert found_31_day_month, "Test did not encounter any 31-day months"

    def test_days_for_30_day_months(self, mock_dependencies):
        """EP3: Test days for months with 30 days (April)"""
        person = FakeInfo()
        months_with_30_days = [4, 6, 9, 11]
        found_30_day_month = False

        for _ in range(50):
            person._set_birth_date()
            year, month, day = map(int, person.birth_date.split('-'))
            if (month in months_with_30_days ):
                found_30_day_month = True
                assert 1 <= day <= 30
        assert found_30_day_month, "Test did not encounter any 30-day months"

    def test_days_for_february(self, mock_dependencies):
        """EP3: Test days for February (28 days)"""
        person = FakeInfo()
        found_28_day_month = False

        for _ in range(50):
            person._set_birth_date()
            year, month, day = map(int, person.birth_date.split('-'))
            if (month == 2 ):
              found_28_day_month = True
              assert 1 <= day <= 28
        assert found_28_day_month, "Test did not encounter any 28-day months"
    
        
    
    
    # # ==================== BLACK-BOX TESTS - Boundary Value Analysis ====================
#   No boundaries to test in this case, since it doesnt take input parameters and it is random
#   so EP tests cover the necessary cases.
#   Any mocking of random would be white-box testing.


    # # ==================== WHITE-BOX TESTS - Statement and Decision Coverage ====================

    @pytest.mark.parametrize("month,max_day", [(1, 31), (4, 30), (2, 28)])
    
    def test_set_birth_date_whitebox_branches(self, mock_dependencies, month, max_day):
        person = FakeInfo()
        with patch('fake_info.random.randint', side_effect=[1980, month, max_day]):
            person._set_birth_date()
        assert person.birth_date == f"1980-{month:02d}-{max_day:02d}"