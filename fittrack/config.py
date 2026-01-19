import configparser
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_INI_PATH = BASE_DIR / "db.ini"
DB_INI_EXAMPLE_PATH = BASE_DIR / "db.ini.example"

config_parser = configparser.ConfigParser()

# Read db.ini if exists, otherwise read example (for defaults only)
if DB_INI_PATH.exists():
    config_parser.read(DB_INI_PATH)
elif DB_INI_EXAMPLE_PATH.exists():
    config_parser.read(DB_INI_EXAMPLE_PATH)

def get_value(section: str, key: str, default=None):
    """
    Safely get configuration value from:
    1) Environment variables
    2) db.ini / db.ini.example
    3) Default value
    """
    return (
        os.getenv(key.upper())
        or (
            config_parser.get(section, key)
            if config_parser.has_section(section)
            and config_parser.has_option(section, key)
            else default
        )
    )

class Config:
    DB_HOST = get_value("mysql", "host", "localhost")
    DB_PORT = get_value("mysql", "port", "3306")
    DB_USER = get_value("mysql", "user", "root")
    DB_PASSWORD = get_value("mysql", "password", "")
    DB_NAME = get_value("mysql", "database", "fittrack_db")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
