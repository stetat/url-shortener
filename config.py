import string
from dotenv import load_dotenv
from os import getenv

load_dotenv()

ALPHABET = string.digits + string.ascii_letters
SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
BASE_URL = "https://127.0.0.1:8080/"
