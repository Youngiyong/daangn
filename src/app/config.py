import os
from dotenv import load_dotenv

load_dotenv(verbose=True)


class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    API_V1_STR: str = os.getenv("API_V1_STR")
    PROJECT_NAME: str = os.getenv("PROJECT_NAME")
    PROJECT_VERSION: str = os.getenv("PROJECT_VERSION")


settings = Settings()