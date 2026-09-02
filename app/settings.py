import os
from dotenv import load_dotenv

load_dotenv()

# Database

DATABASE_URL = os.getenv("DATABASE_URL")
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
