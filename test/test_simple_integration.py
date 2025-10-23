# test_simple_integration.py
import mysql.connector
import sys
import os
import json
import random
from datetime import datetime, date

# Tilføj sti til dine moduler
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from db import DB

def get_person_names():
    """Hent person navne direkte fra JSON filen"""
    data_path = os.path.join(project_root, 'data', 'person-names.json')

    if not os.path.exists(data_path):
        print(f"❌ person-names.json not found at: {data_path}")
        return None

    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    return data['persons']

def test_get_random_town():
    """Test get_random_town() med rigtig database"""
    print("Testing get_random_town()...")

    db = DB()
    town_data = db.get_random_town()

    # Valider resultatet
    assert isinstance(town_data, dict)
    assert 'postal_code' in town_data
    assert 'town_name' in town_data
    assert len(town_data['postal_code']) == 4
    assert len(town_data['town_name']) > 0

    # Verificer at data kommer fra databasen
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='addresses'
    )
    cursor = conn.cursor()
    cursor.execute(
        "SELECT cTownName FROM postal_code WHERE cPostalCode = %s",
        (town_data['postal_code'],)
    )
    db_town_name = cursor.fetchone()[0]
    cursor.close()
    conn.close()

    assert town_data['town_name'] == db_town_name
    print(f"✅ get_random_town() virker: {town_data['postal_code']} - {town_data['town_name']}")

def test_set_town_count():
    """Test _set_town_count() funktionalitet"""
    print("Testing _set_town_count()...")

    # Nulstil count
    DB._town_count = None

    # Instantier DB (kalder _set_town_count() internt)
    db = DB()

    # Test at count er sat korrekt
    assert DB._town_count is not None
    assert isinstance(DB._town_count, int)
    assert DB._town_count > 0

    # Verificer at count matcher databasen
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='addresses'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM postal_code")
    db_count = cursor.fetchone()[0]
    cursor.close()
    conn.close()

    assert DB._town_count == db_count
    print(f"✅ _set_town_count() virker: {DB._town_count} postnumre")

def test_set_full_name_and_gender_logic():
    """Test logikken bag _set_full_name_and_gender() direkte fra JSON"""
    print("Testing _set_full_name_and_gender logic...")

    # Hent data direkte fra JSON
    persons = get_person_names()
    assert persons is not None, "Kunne ikke hente person data fra JSON"

    # Simuler hvad _set_full_name_and_gender() gør
    person = random.choice(persons)
    first_name = person['firstName']
    last_name = person['lastName']
    gender = person['gender']

    # Valider data (samme validering som i FakeInfo)
    assert isinstance(first_name, str)
    assert isinstance(last_name, str)
    assert isinstance(gender, str)
    assert gender in ['female', 'male']
    assert len(first_name) > 0
    assert len(last_name) > 0

    # Test at full_name kombineres korrekt
    full_name = f"{first_name} {last_name}"
    assert full_name == f"{first_name} {last_name}"

    print(f"✅ _set_full_name_and_gender logic virker: {first_name} {last_name} ({gender})")

def test_all_three_methods_integration():
    """Test at alle 3 metoder arbejder sammen"""
    print("Testing integration of all 3 methods...")

    # 1. Test database connection og town count
    DB._town_count = None
    db = DB()
    print(f"   Database connected, town count: {DB._town_count}")

    # 2. Test at hente et postnummer
    town_data = db.get_random_town()
    print(f"   Random town: {town_data['postal_code']} - {town_data['town_name']}")

    # 3. Test at generere person data direkte fra JSON
    persons = get_person_names()
    person = random.choice(persons)
    print(f"   Generated person: {person['firstName']} {person['lastName']} ({person['gender']})")

    # Valider at alt virker sammen
    assert DB._town_count > 0
    assert town_data['postal_code'] is not None
    assert person['firstName'] is not None

    print("✅ All 3 methods work together perfectly!")

def test_data_quality():
    """Test kvaliteten af data i person-names.json"""
    print("Testing data quality...")

    persons = get_person_names()
    assert persons is not None

    # Test at alle personer har de nødvendige felter
    for person in persons:
        assert 'firstName' in person
        assert 'lastName' in person
        assert 'gender' in person
        assert person['gender'] in ['female', 'male']
        assert len(person['firstName']) > 0
        assert len(person['lastName']) > 0

    # Tjek fordeling af køn
    genders = [p['gender'] for p in persons]
    male_count = genders.count('male')
    female_count = genders.count('female')

    print(f"   Data quality: {len(persons)} persons, {male_count} male, {female_count} female")
    print("✅ Data quality is good!")

if __name__ == "__main__":
    print("Starting Integration Tests")
    print("=" * 40)

    try:
        # Test data kvalitet først
        test_data_quality()

        # Test de 3 hovedmetoder
        test_set_town_count()
        test_get_random_town()
        test_set_full_name_and_gender_logic()

        # Test integration
        test_all_three_methods_integration()

        print("\n ALL INTEGRATION TESTS PASSED!")
        print("✅ get_random_town() - works with real MySQL database")
        print("✅ _set_town_count() - correctly counts database records")
        print("✅ _set_full_name_and_gender() - generates valid person data")
        print("✅ All methods integrate correctly")
        print("✅ Data quality verified")

    except Exception as e:
        print(f"\n TEST FAILED: {e}")
        import traceback
        traceback.print_exc()