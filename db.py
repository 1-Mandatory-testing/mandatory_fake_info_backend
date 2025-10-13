import mysql.connector
from mysql.connector import Error
from typing import Dict, Optional
from config import DB_CONFIG
import random

class DB:
    _town_count: Optional[int] = None
    
    def __init__(self):
        self.connection = None
        self._connect()
        if DB._town_count is None:
            self._set_town_count()
    
    def _connect(self):
        """Open connection to MySQL database"""
        try:
            self.connection = mysql.connector.connect(
                host=DB_CONFIG['host'],
                database=DB_CONFIG['database'],
                user=DB_CONFIG['user'],
                password=DB_CONFIG['password'],
                charset='utf8mb4',
                collation='utf8mb4_general_ci'
            )
        except Error as e:
            raise Exception(f"Database connection unsuccessful: {e}")
    
    def _set_town_count(self):
        """Get total number of towns (cached as class variable)"""
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) AS total FROM postal_code")
        result = cursor.fetchone()
        DB._town_count = result['total']
        cursor.close()
    
    def get_random_town(self) -> Dict[str, str]:
        """Get random postal code and town name"""
        random_offset = random.randint(0, DB._town_count - 1)
        
        cursor = self.connection.cursor(dictionary=True)
        query = f"""
            SELECT cPostalCode AS postal_code, cTownName AS town_name
            FROM postal_code
            LIMIT {random_offset}, 1
        """
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        
        return result
    
    def __del__(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()