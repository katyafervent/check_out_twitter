import time
from http import HTTPStatus

import requests
from loguru import logger
from requests.exceptions import RequestException

from constants import HEADERS, RETRY_PERIOD, USER_ID, USERS_ENDPOINT
from exceptions import HTTPException, TwitterAPIRequestError
from utils import get_pretty_json_string


def get_tweets():
    try:
        response = requests.get(
            f"{USERS_ENDPOINT}/{USER_ID}/tweets", headers=HEADERS
        )
    except Exception as error:
        raise HTTPException from error
    print(get_pretty_json_string(response.json()))


def get_info_about_user(user_id):
    if not user_id:
        user_id = USER_ID
    try:
        response = requests.get(f"{USERS_ENDPOINT}/{user_id}", headers=HEADERS)
    except Exception as error:

        raise HTTPException from error

    print(get_pretty_json_string(response.json()))


def check_response(response: dict) -> list:
    """Validates response content.
    Raises:

        TypeError: on wrong response type
        KeyError: on wrong response value

    Returns:

        checking status
    Args:
        response (dict): response from twitter V2
    Returns:
        list: List of tweets
    """
    if not isinstance(response, dict):
        raise TypeError("Невалидный тип ответа от twitter API.")

    if "data" not in response:
        if response["meta"]["result_count"] != 0:
            raise KeyError(
                "Невалидный формат ответа от API "
                "Отсутствуют необходимый ключ 'data'"
            )
        logger.debug("Новых твитов нет")
        return []

    if not isinstance(response["data"], list):
        raise TypeError(
            "Невалидный тип ответа от twitter API "
            "Ключ data должен быть списком.",
        )
    return response["data"]


def get_new_tweets(since_id):
    try:
        response = requests.get(
            f"{USERS_ENDPOINT}/{USER_ID}/tweets",
            headers=HEADERS,
            params={"since_id": since_id},
        )
    except RequestException as error:
        raise TwitterAPIRequestError(
            "Неоднозначное исключение во время обработки запроса "
        ) from error
    if response.status_code != HTTPStatus.OK:
        code, text = response.status_code, response.text
        details = f"Код ответа: {code}, сообщение об ошибке: {text}"

        if response.status_code == HTTPStatus.UNAUTHORIZED:
            raise HTTPException(
                f"Ошибка авторизации к twitter API. {details}",
            )
        if response.status_code == HTTPStatus.BAD_REQUEST:
            raise HTTPException(
                f"Ошибка запроса к twitter API. {details}",
            )
        raise HTTPException(f"Некорректный ответ от twitter. {details}")
    return response.json()


def print_tweet_text(tweet):
    print('\n\n')
    print('================================')
    print(tweet["text"])
    print('================================')
    print('\n\n')


if __name__ == "__main__":
    logger.add("file_1.log", rotation="1 kb")
    since_id = 1

    while True:
        try:
            response = get_new_tweets(since_id=since_id)
            tweets = check_response(response)
            if tweets:
                new_tweet = tweets[0]
                since_id = new_tweet['id']

                print_tweet_text(new_tweet)
                logger.info(f"Новый твит {new_tweet['id']} успешно напечатан")

        except Exception as error:
            logger.exception(
                f"Произошла ошибка во время работы программы: {error}"
            )

        finally:
            time.sleep(RETRY_PERIOD)
