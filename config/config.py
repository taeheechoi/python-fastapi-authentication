from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from functools import lru_cache

load_dotenv('.env')

class Settings(BaseSettings):
    app_name: str = 'my API'
    NUTRITIONIX_API_ID: str
    NUTRITIONIX_API_KEY: str
    NUTRITIONIX_URL: str
    EXPECTED_CALORIES_PER_DAY: str
    JWT_SECRET:str
    JWT_ALGORITHM:str
    PORT: str
    

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()