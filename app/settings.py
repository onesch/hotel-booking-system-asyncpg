import os
from dotenv import load_dotenv

load_dotenv()

# Database

DATABASE_URL = os.getenv("DATABASE_URL")
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

# Redis
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

# Rate limiting
MAX_REQUESTS: int = 10
WINDOW_SECONDS: int = 60
