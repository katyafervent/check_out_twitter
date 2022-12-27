import os

from dotenv import load_dotenv

load_dotenv()


CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")
USER_ID = os.getenv("USER_ID")

ENDPOINT = "https://api.twitter.com/2"
USERS_ENDPOINT = f"{ENDPOINT}/users"
# HEADERS = {"Authorization": "Bearer "}
HEADERS = {"Authorization": f"Bearer {BEARER_TOKEN}"}

RETRY_PERIOD = 15
