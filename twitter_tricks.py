import os

import requests
import tweepy
from loguru import logger
from requests.exceptions import RequestException

from constants import BEARER_TOKEN, HEADERS, USER_ID, USERS_ENDPOINT
from exceptions import HTTPException
from utils import get_pretty_json_string

# client = tweepy.Client(
#     consumer_key=CONSUMER_KEY,
#     consumer_secret=CONSUMER_SECRET,
#     bearer_token=BEARER_TOKEN,
# )


# response = client.get_recent_tweets_count(
#     query='from:saratov -is:retweet lang:ru', start_time='2022-12-22T00:00:00Z'
# )
# print(response.data)
# #  "GET", f"/2/users/me"
def do_something():
    pass


def get_tweets():
    try:
        response = requests.get(f"{USERS_ENDPOINT}/{USER_ID}/tweets", headers=HEADERS)
    except Exception as error:
        raise HTTPException from error
    print(get_pretty_json_string(response.json()))


def get_info_about_me():
    try:
        response = requests.get(f"{USERS_ENDPOINT}/{USER_ID}", headers=HEADERS)
    except Exception as error:
        raise HTTPException from error

    print(get_pretty_json_string(response.json()))


def check_response(response: dict) -> bool:
    """Validates response content.
    Raises:

        TypeError: on wrong response type
        KeyError: on wrong response value

    Returns:

        checking status
    Args:
        response (dict): response from twitter V2
    Returns:
        bool: checked done correctly
    """
    if not isinstance(response, dict):
        raise TypeError("Невалидный тип ответа от twitter API.")

    if "data" not in response:
        raise KeyError(
            "Невалидный формат ответа от API Практикум.Домашка. "
            f"Отсутствуют обязательные ключи: {', '.join(missing_keys)}",
        )

    if not isinstance(response.get("homeworks"), list):

        raise TypeError(
            "Невалидный тип ответа от API Практикум.Домашка. "
            "Ключ homeworks должен быть списком.",
        )


def get_new_tweet(since_id):

    try:
        response = requests.get(
            f"{USERS_ENDPOINT}/{USER_ID}/tweets",
            headers=HEADERS,
            params={"since_id": since_id},
        )
    except RequestException as error:
        raise HTTPException("Некорректный ответ от twitter") from error
    return response.json()


if __name__ == "__main__":
    logger.add("file_1.log", rotation="1 kb")
    # while True:
    new_tweet = get_new_tweet(since_id=639381407056461800)
    check_response(new_tweet)
    if new_tweet:
        print(new_tweet["data"][0]["text"])
    # get_tweets()
