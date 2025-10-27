import pytest

from db import DB
from fake_info import FakeInfo


@pytest.fixture(scope="class")
def db_instance():
    """Fixture to provide a shared DB instance for the test class"""
    db = DB()
    yield db


@pytest.mark.integration
class TestDBIntegration:
    """Integration tests for DB class with real MySQL database"""

    def test_db_connection_successful(self, db_instance):
        """Verify we can connect to the database"""
        assert db_instance.connection is not None
        assert db_instance.connection.is_connected()

    def test_get_random_town_returns_valid_data(self, db_instance):
        """Verify get_random_town returns correctly structured data"""
        town = db_instance.get_random_town()

        assert town is not None
        assert 'postal_code' in town
        assert 'town_name' in town

    def test_postal_code_format(self, db_instance):
        """Verify postal code is 4 digits"""
        town = db_instance.get_random_town()

        assert len(town['postal_code']) == 4
        assert town['postal_code'].isdigit()

    def test_town_name_not_empty(self, db_instance):
        """Verify town name is not empty"""
        town = db_instance.get_random_town()

        assert town['town_name']
        assert len(town['town_name']) > 0

    def test_multiple_calls_return_data(self, db_instance):
        """Verify multiple calls work and return valid data"""
        towns = [db_instance.get_random_town() for _ in range(5)]

        assert len(towns) == 5
        for town in towns:
            assert 'postal_code' in town
            assert 'town_name' in town
            assert len(town['postal_code']) == 4
            assert town['postal_code'].isdigit()

    def test_town_count_is_cached(self, db_instance):
        """Verify town count is set and cached as class variable"""
        assert db_instance._town_count is not None
        assert db_instance._town_count > 0


@pytest.mark.integration
class TestFakeInfoDBIntegration:
    """Component integration tests - FakeInfo with real DB data"""

    def test_fake_info_uses_real_postal_codes(self):
        """Verify FakeInfo retrieves real postal codes from database"""
        person = FakeInfo()

        # Verify address has postal code and town data from real db
        assert 'postal_code' in person.address
        assert 'town_name' in person.address
        assert len(person.address['postal_code']) == 4
        assert person.address['postal_code'].isdigit()
        assert len(person.address['town_name']) > 0
