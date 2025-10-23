import re
import pytest
from unittest.mock import patch, MagicMock
from fake_info import FakeInfo


@pytest.fixture
def mock_dependencies_for_address():
    """
    Gør FakeInfo uafhængig af filsystem og DB, så __init__ og _set_address() kan køre.
    - DB().get_random_town() -> fast mock-værdi
    - open/json.load -> returnerer en lille persons-liste
    """
    with patch('fake_info.DB') as mock_db, \
         patch('builtins.open', create=True), \
         patch('json.load') as mock_json_load:

        # JSON: sørg for at _set_full_name_and_gender kan vælge en person
        mock_json_load.return_value = {
            'persons': [
                {'firstName': 'Hugo', 'lastName': 'Ekitike', 'gender': 'male'},
                {'firstName': 'Pernille', 'lastName': 'Harder', 'gender': 'female'}
            ]
        }

        # DB: fast town/postnummer
        mock_db_instance = MagicMock()
        mock_db_instance.get_random_town.return_value = {
            'postal_code': '2100',
            'town_name': 'København Ø'
        }
        mock_db.return_value = mock_db_instance

        yield


class TestSetAddress:
    """Tests for _set_address() method"""

    # ==================== BLACK-BOX: EP ====================

    def test_street_format_and_length(self, mock_dependencies_for_address):
        """EP1: Street is 40 chars, starts not with space, only valid chars"""
        person = FakeInfo()
        street = person.address['street']
        assert len(street) == 40, "Street length is not 40 characters"
        assert street[0] != ' ', "Street starts with a space"
        assert re.fullmatch(r'[A-Za-zÆØÅæøå ]+', street), "Street contains invalid characters"

    def test_number_format(self, mock_dependencies_for_address):
        """EP2: Number matches r'^\d{1,3}[A-Z]?$' og 1 <= number_part <= 999"""
        person = FakeInfo()

        number = person.address['number']

        assert re.match(r'^\d{1,3}[A-Z]?$', number), f"Number '{number}' doesnt match expected format"

        number_match = re.match(r'^(\d{1,3})', number)
        assert number_match is not None, "Could not extract numeric part from number"
        numeric_part = int(number_match.group(1))
        assert 1 <= numeric_part <= 999, f"Numeric part {numeric_part} is out of range 1..999"

    def test_floor_format(self, mock_dependencies_for_address):
        """EP3: Floor is 'st' or number 1..99 (strings)"""
        # 1. Opret FakeInfo objekt
        # 2. floor = person.address['floor']
        # 3. Hvis floor == 'st': OK
        # 4. Ellers: assert regex r'^\d{1,2}$' og 1 <= int(floor) <= 99
        person = FakeInfo()
        floor = person.address['floor']
        if floor == 'st':
            pass  # OK
        else:
            assert re.match(r'^\d{1,2}$', floor), f"Floor '{floor}' doesnt match expected format"
            floor_number = int(floor)
            assert 1 <= floor_number <= 99, f"Floor number {floor_number} is out of range 1..99"


    def test_door_format(self, mock_dependencies_for_address):
        """EP4: Door is 'th'/'tv'/'mf', or 1..50, or letter(+optional dash)+1..999"""
        person = FakeInfo()
        door = person.address['door']
        if door in {'th', 'tv', 'mf'}:
            pass  # OK
        elif re.match(r'^\d{1,2}$', door):
            assert 1 <= int(door) <= 50, f"Door number {door} is out of range 1..50"
        elif re.match(r'^[a-zæøå](?:-\d{1,3}|\d{1,3})$', door):
            number_part = re.search(r'(\d{1,3})$', door).group(1)
            assert 1 <= int(number_part) <= 999, f"Door letter-number part {number_part} is out of range 1..999"
        else:
            pytest.fail(f"Door '{door}' does not match any expected format")
        
        
        
    def test_postal_code_and_town_from_db(self, mock_dependencies_for_address):
        """EP5: postal_code 4 cifre, town_name ikke tom, matcher mock-DB værdier"""
        # 1. Opret FakeInfo objekt
        person = FakeInfo()

    # 2. Ekstraher felter
        postal_code = person.address['postal_code']
        town_name = person.address['town_name']

    # 3. Assert postal_code er præcis 4 cifre
        assert re.match(r'^\d{4}$', postal_code), f"Postal code '{postal_code}' matcher ikke 4-cifret format"

    # 4. Assert town_name er non-empty string
        assert isinstance(town_name, str) and town_name.strip() != "", "town_name skal være en ikke-tom string"

    # 5. Assert at de matcher mock’ens return value
        assert postal_code == "2100", f"Postal code '{postal_code}' matcher ikke forventet værdi '2100'"
        assert town_name == "København Ø", f"Town name '{town_name}' matcher ikke forventet værdi 'København Ø'"

        

    # ==================== BLACK-BOX: BVA ====================
#   No boundaries to test in this case, since it doesnt take input parameters and it is random
#   so EP tests cover the necessary cases.

    # ==================== WHITE-BOX: DECISION COVERAGE ====================

    def test_decision_number_with_and_without_letter(self, mock_dependencies_for_address):
        """Decision: number with letter vs without letter"""
        person = FakeInfo()

        # A) With letter (randint(1,10) < 3) + choice -> 'E'
        with patch('fake_info.FakeInfo._get_random_text', return_value='Some Street'), \
             patch('fake_info.random.randint', side_effect=[42, 1, 1, 8]), \
             patch('fake_info.random.choice', return_value='E'):
            person._set_address()
            assert re.fullmatch(r'\d{1,3}E', person.address['number'])

        # B) Without letter (randint(1,10) >= 3)
        with patch('fake_info.FakeInfo._get_random_text', return_value='Some Street'), \
             patch('fake_info.random.randint', side_effect=[42, 5, 1, 8]):
            person._set_address()
            assert person.address['number'] == '42'

    def test_decision_floor_st_vs_number(self, mock_dependencies_for_address):
        """Decision: floor 'st' vs number"""
        person = FakeInfo()

        # A) <4 -> 'st'
        with patch('fake_info.FakeInfo._get_random_text', return_value='Some Street'), \
             patch('fake_info.random.randint', side_effect=[123, 5, 1, 8]):
            person._set_address()
            assert person.address['floor'] == 'st'

        # B) >=4 + floor number = 42
        with patch('fake_info.FakeInfo._get_random_text', return_value='Some Street'), \
             patch('fake_info.random.randint', side_effect=[123, 5, 4, 42, 8]):
            person._set_address()
            assert person.address['floor'] == '42'

    def test_decision_door_all_five_branches(self, mock_dependencies_for_address):
        """Decision: all 5 door-branches (th, tv, mf, number, letter[/dash])"""
        person = FakeInfo()

        # th: door_type < 8
        with patch('fake_info.FakeInfo._get_random_text', return_value='Some Street'), \
             patch('fake_info.random.randint', side_effect=[100, 5, 1, 3]):
            person._set_address()
            assert person.address['door'] == 'th'

        # tv: door_type < 15
        with patch('fake_info.FakeInfo._get_random_text', return_value='Some Street'), \
             patch('fake_info.random.randint', side_effect=[100, 5, 1, 10]):
            person._set_address()
            assert person.address['door'] == 'tv'

        # mf: door_type < 17
        with patch('fake_info.FakeInfo._get_random_text', return_value='Some Street'), \
             patch('fake_info.random.randint', side_effect=[100, 5, 1, 16]):
            person._set_address()
            assert person.address['door'] == 'mf'

        # number: door_type < 19 -> number = 37
        with patch('fake_info.FakeInfo._get_random_text', return_value='Some Street'), \
             patch('fake_info.random.randint', side_effect=[100, 5, 1, 18, 37]):
            person._set_address()
            assert person.address['door'] == '37'

        # letter no dash: door_type 19 -> 'b123'
        with patch('fake_info.FakeInfo._get_random_text', return_value='Some Street'), \
             patch('fake_info.random.randint', side_effect=[100, 5, 1, 19, 123]), \
             patch('fake_info.random.choice', return_value='b'):
            person._set_address()
            assert person.address['door'] == 'b123'

        # letter with dash: door_type 20 -> 'b-123'
        with patch('fake_info.FakeInfo._get_random_text', return_value='Some Street'), \
             patch('fake_info.random.randint', side_effect=[100, 5, 1, 20, 123]), \
             patch('fake_info.random.choice', return_value='b'):
            person._set_address()
            assert person.address['door'] == 'b-123'

    def test_statement_all_key_assignments(self, mock_dependencies_for_address):
        """Statement: all address keys are assigned"""
        person = FakeInfo()
        addr = person.address
        for key in ['street', 'number', 'floor', 'door', 'postal_code', 'town_name']:
            assert key in addr, f"Missing key: {key}"
            assert isinstance(addr[key], str) and addr[key] != "", f"Key '{key}' is empty or not a string"
