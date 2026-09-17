import os
from dotenv import load_dotenv

load_dotenv()

# Database

DATABASE_URL = os.getenv("DATABASE_URL")
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

# Redis

REDIS_URL = os.getenv("REDIS_URL")
TEST_REDIS_URL = os.getenv("TEST_REDIS_URL")

# Rate limiting

MAX_REQUESTS: int = 10
WINDOW_SECONDS: int = 60
