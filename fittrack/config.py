import configparser
import os
from pathlib import Path

# db.ini is located inside the same folder as this file (fittrack/)
BASE_DIR = Path(__file__).resolve().parent
DB_INI_PATH = BASE_DIR / "db.ini"

config_parser = configparser.ConfigParser()
config_parser.read(DB_INI_PATH)

class Config:
    DB_HOST = os.getenv("DB_HOST", config_parser.get("mysql", "host"))
    DB_PORT = os.getenv("DB_PORT", config_parser.get("mysql", "port"))
    DB_USER = os.getenv("DB_USER", config_parser.get("mysql", "user"))
    DB_PASSWORD = os.getenv("DB_PASSWORD", config_parser.get("mysql", "password"))
    DB_NAME = os.getenv("DB_NAME", config_parser.get("mysql", "database"))

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
