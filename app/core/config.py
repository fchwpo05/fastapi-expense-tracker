import os
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env

class Settings:
    PROJECT_NAME: str = "Expense Tracker API"
    
    DATABASE_URL: str
    SECRET_KEY: str

    def __init__(self):
        # Load DATABASE_URL
        db_url = os.getenv("DATABASE_URL")
        if db_url is None:
            raise ValueError("DATABASE_URL is not set in .env!")
        self.DATABASE_URL = db_url

        # Load SECRET_KEY
        secret = os.getenv("SECRET_KEY")
        if secret is None:
            raise ValueError("SECRET_KEY is not set in .env!")
        self.SECRET_KEY = secret

# We are creating a single instance to import across the project
settings = Settings()