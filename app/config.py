import os

from dotenv import load_dotenv

load_dotenv('.env')

host = os.environ.get("DB_HOST")
database = os.environ.get("DB_NAME")
user = os.environ.get("DB_USER")
password = os.environ.get("DB_PASSWORD")
port = os.environ.get("DB_PORT")
db_url = os.environ.get("DB_URL")
