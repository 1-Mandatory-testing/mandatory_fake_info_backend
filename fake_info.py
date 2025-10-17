import json
import random
from datetime import date, datetime
from typing import Dict, List

from db import DB


class FakeInfo:
    GENDER_FEMININE = "female"
    GENDER_MASCULINE = "male"

    PHONE_PREFIXES = [
        '2', '30', '31', '40', '41', '42', '50', '51', '52', '53', '60', '61', '71', '81', '91', '92', '93', '342',
        '344', '345', '346', '347', '348', '349', '356', '357', '359', '362', '365', '366', '389', '398', '431',
        '441', '462', '466', '468', '472', '474', '476', '478', '485', '486', '488', '489', '493', '494', '495',
        '496', '498', '499', '542', '543', '545', '551', '552', '556', '571', '572', '573', '574', '577', '579',
        '584', '586', '587', '589', '597', '598', '627', '629', '641', '649', '658', '662', '663', '664', '665',
        '667', '692', '693', '694', '697', '771', '772', '782', '783', '785', '786', '788', '789', '826', '827', '829'
    ]

    FILE_PERSON_NAMES = "data/person-names.json"

    def __init__(self):
        self._set_full_name_and_gender()
        self._set_birth_date()
        self._set_cpr()
        self._set_address()
        self._set_phone()

    def _set_full_name_and_gender(self):
        """Generate fake full name and gender from JSON file"""
        with open(self.FILE_PERSON_NAMES, encoding='utf-8') as f:
            data = json.load(f)

        person = random.choice(data['persons'])
        self.first_name = person['firstName']
        self.last_name = person['lastName']
        self.gender = person['gender']

    def _set_birth_date(self):
        """Generate fake date of birth from 1900 to current year"""
        year = random.randint(1900, datetime.now().year)
        month = random.randint(1, 12)

        # Days per month (simplified, no leap year logic)
        if month in [1, 3, 5, 7, 8, 10, 12]:
            day = random.randint(1, 31)
        elif month in [4, 6, 9, 11]:
            day = random.randint(1, 30)
        else:
            day = random.randint(1, 28)

        self.birth_date = date(year, month, day).strftime('%Y-%m-%d')

    def _set_cpr(self):
        """Generate fake CPR based on birth date and gender"""
        # Extract date parts
        date_obj = datetime.strptime(self.birth_date, '%Y-%m-%d')
        dd = date_obj.strftime('%d')
        mm = date_obj.strftime('%m')
        yy = date_obj.strftime('%y')

        # Generate last 4 digits
        # Last digit must be even for female, odd for male
        final_digit = random.randint(0, 9)
        if self.gender == self.GENDER_FEMININE and final_digit % 2 == 1:
            final_digit = (final_digit + 1) % 10
        elif self.gender == self.GENDER_MASCULINE and final_digit % 2 == 0:
            final_digit = (final_digit + 1) % 10

        middle_digits = ''.join([str(random.randint(0, 9)) for _ in range(3)])

        self.cpr = f"{dd}{mm}{yy}{middle_digits}{final_digit}"

    def _set_address(self):
        """Generate fake Danish address"""
        self.address = {}

        # Street: random alphabetic characters
        self.address['street'] = self._get_random_text(40)

        # Number: 1-999 optionally followed by uppercase letter
        self.address['number'] = str(random.randint(1, 999))
        if random.randint(1, 10) < 3:  # ~20% chance
            self.address['number'] += random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

        # Floor: "st" or 1-99
        if random.randint(1, 10) < 4:  # ~30% chance
            self.address['floor'] = 'st'
        else:
            self.address['floor'] = str(random.randint(1, 99))

        # Door: th, tv, mf, 1-50, or letter + optional dash + 1-999
        door_type = random.randint(1, 20)
        if door_type < 8:  # 35%
            self.address['door'] = 'th'
        elif door_type < 15:  # 35%
            self.address['door'] = 'tv'
        elif door_type < 17:  # 10%
            self.address['door'] = 'mf'
        elif door_type < 19:  # 10%
            self.address['door'] = str(random.randint(1, 50))
        else:  # 10%
            lower_letters = 'abcdefghijklmnopqrstuvwxyzøæå'
            self.address['door'] = random.choice(lower_letters)
            if door_type == 20:  # 5% with dash
                self.address['door'] += '-'
            self.address['door'] += str(random.randint(1, 999))

        # Postal code and town from database
        db = DB()
        town_data = db.get_random_town()
        self.address['postal_code'] = town_data['postal_code']
        self.address['town_name'] = town_data['town_name']

    def _get_random_text(self, length: int = 1, include_danish: bool = True) -> str:
        """Generate random text with alphabetic characters"""
        valid_chars = list(' abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
        if include_danish:
            valid_chars.extend(list('æøåÆØÅ'))

        # First character cannot be space
        text = random.choice([c for c in valid_chars if c != ' '])
        for _ in range(length - 1):
            text += random.choice(valid_chars)

        return text

    def _set_phone(self):
        """Generate fake Danish phone number"""
        prefix = random.choice(self.PHONE_PREFIXES)
        remaining_digits = 8 - len(prefix)
        suffix = ''.join([str(random.randint(0, 9)) for _ in range(remaining_digits)])
        self.phone_number = prefix + suffix

    def get_fake_person(self) -> Dict:
        """Return all fake person information"""
        return {
            'CPR': self.cpr,
            'firstName': self.first_name,
            'lastName': self.last_name,
            'gender': self.gender,
            'birthDate': self.birth_date,
            'address': self.address,
            'phoneNumber': self.phone_number
        }

    @staticmethod
    def get_fake_persons(amount: int) -> List[Dict]:
        """Return information about multiple fake persons"""
        if amount < 2:
            amount = 2
        if amount > 100:
            amount = 100

        bulk_info = []
        for _ in range(amount):
            fake = FakeInfo()
            bulk_info.append(fake.get_fake_person())

        return bulk_info
