
from dotenv import load_dotenv
import os
from app.database import Database

load_dotenv()

host = os.environ.get("DB_HOST")
database = os.environ.get("DB_NAME")
user = os.environ.get("DB_USER")
password = os.environ.get("DB_PASSWORD")
print(host, database, user, password)

db = Database(host=host, database=database, user=user, password=password)
