# test_connection.py
import mysql.connector

def test_database():
    try:
        print("Testing database connection...")

        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='addresses'
        )

        if conn.is_connected():
            print("✅ SUCCESS! Connected to database")

            cursor = conn.cursor()

            # Tjek antal postnumre
            cursor.execute("SELECT COUNT(*) FROM postal_code")
            count = cursor.fetchone()[0]
            print(f"Found {count} postal codes in database")

            # Vis nogle eksempler
            cursor.execute("SELECT cPostalCode, cTownName FROM postal_code LIMIT 10")
            print("Sample postal codes:")
            for postal_code, town in cursor:
                print(f"   {postal_code} - {town}")

            cursor.close()
            conn.close()
            print("Database is ready for integration tests!")

    except Exception as e:
        print(f" ERROR: {e}")
        print("\n Check:")
        print("- Is database 'addresses' created?")
        print("- Is addresses.sql imported?")

if __name__ == "__main__":
    test_database()