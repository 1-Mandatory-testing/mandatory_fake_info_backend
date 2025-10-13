from pydantic_settings import BaseSettings

class DatabaseSettings(BaseSettings):
    db_host: str = "localhost"
    db_database: str = "addresses"
    db_user: str = "root"
    db_password: str = ""

    class Config:
        env_file = ".env"

settings = DatabaseSettings()

DB_CONFIG = {
    'host': settings.db_host,
    'database': settings.db_database,
    'user': settings.db_user,
    'password': settings.db_password
}