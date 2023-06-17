from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

config = {
    "SQLALCHEMY_DATABASE_URI": os.getenv("DB_URI"),
}
