from dotenv import load_dotenv
import os

load_dotenv()

def get_env_variable(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"{name} is not set")
    return value

DATABASE_URL = get_env_variable("DATABASE_URL")