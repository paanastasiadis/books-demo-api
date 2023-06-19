"""
Configuration module for loading environment variables and setting up the application.

- config: A dictionary containing configuration options, including the SQLAlchemy database URI.
"""

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

config = {
    "SQLALCHEMY_DATABASE_URI": os.getenv("DB_URI"),
}
