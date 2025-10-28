"""
Unit tests for FakeInfo.get_fake_person()

Black-box: Equivalence Partitioning (EP) for structure and formats
White-box: No branches - statement coverage only
"""
import pytest

from fake_info import FakeInfo


@pytest.fixture
def fake_instance():
    """Create FakeInfo instance with pre-set attributes"""
    fake = object.__new__(FakeInfo)

    fake.cpr = "0101901234"
    fake.first_name = "Female"
    fake.last_name = "Person"
    fake.gender = "female"
    fake.birth_date = "1990-01-01"
    fake.address = {
        'street': 'Testgade',
        'number': '42',
        'floor': '3',
        'door': 'th',
        'postal_code': '2000',
        'town_name': 'Frederiksberg'
    }
    fake.phone_number = "23445678"

    return fake


# ========== HELPERS ==========

REQUIRED_KEYS = {'CPR', 'firstName', 'lastName', 'gender', 'birthDate', 'address', 'phoneNumber'}
ADDRESS_KEYS  = {'street', 'number', 'floor', 'door', 'postal_code', 'town_name'}


# ========== BLACK-BOX: EQUIVALENCE PARTITIONING ==========

def test_returns_dict(fake_instance):
    """EP: Returns a dictionary"""
    result = fake_instance.get_fake_person()
    assert isinstance(result, dict)


def test_contains_all_required_keys(fake_instance):
    """EP: Dictionary contains exactly the 7 required keys"""
    result = fake_instance.get_fake_person()
    assert set(result.keys()) == REQUIRED_KEYS


def test_maps_cpr_correctly(fake_instance):
    """EP: CPR field maps to cpr attribute"""
    result = fake_instance.get_fake_person()
    assert result['CPR'] == fake_instance.cpr


def test_maps_first_name_correctly(fake_instance):
    """EP: firstName field maps to first_name attribute"""
    result = fake_instance.get_fake_person()
    assert result['firstName'] == fake_instance.first_name


def test_maps_last_name_correctly(fake_instance):
    """EP: lastName field maps to last_name attribute"""
    result = fake_instance.get_fake_person()
    assert result['lastName'] == fake_instance.last_name


def test_maps_gender_correctly(fake_instance):
    """EP: gender field maps to gender attribute"""
    result = fake_instance.get_fake_person()
    assert result['gender'] == fake_instance.gender


def test_maps_birth_date_correctly(fake_instance):
    """EP: birthDate field maps to birth_date attribute"""
    result = fake_instance.get_fake_person()
    assert result['birthDate'] == fake_instance.birth_date


def test_maps_address_correctly(fake_instance):
    """EP: address field maps to address attribute"""
    result = fake_instance.get_fake_person()
    assert result['address'] == fake_instance.address
    assert result['address'] is fake_instance.address


def test_maps_phone_number_correctly(fake_instance):
    """EP: phoneNumber field maps to phone_number attribute"""
    result = fake_instance.get_fake_person()
    assert result['phoneNumber'] == fake_instance.phone_number


def test_address_is_dict_with_required_keys(fake_instance):
    """EP: address value is a dictionary with expected keys"""
    result = fake_instance.get_fake_person()
    assert isinstance(result['address'], dict)
    assert set(result['address'].keys()) == ADDRESS_KEYS


# ========== WHITE-BOX: no branches ==========

def test_method_has_fixed_structure(fake_instance):
    """White-box: Method returns fixed dict with exactly 7 fields (no branches)"""
    result = fake_instance.get_fake_person()
    assert isinstance(result, dict)
    assert len(result) == 7
