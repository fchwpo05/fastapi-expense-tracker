import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Expense Tracker API"

    def __init__(self):
        db_url = os.getenv("DATABASE_URL")
        if db_url is None:
            raise ValueError("DATABASE_URL is not set in .env!")
        self.DATABASE_URL: str = db_url

settings = Settings()