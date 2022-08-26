import os
from dotenv import load_dotenv

load_dotenv()

TEST = os.getenv("DB_USERNAME")
print(TEST)
