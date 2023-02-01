import json
from http import HTTPStatus
from typing import Optional
from datetime import date, timedelta

import aiohttp

from constants import BASE_URL_PB_EXCHANGE
from .exceptions import NetworkError
from .response_formatter import json_formatter


def check_result(content_type: str, status_code: int, body: str):
    if content_type != 'application/json':
        raise NetworkError(f"Invalid response with content type {content_type}: \"{body}\"")

    try:
        result_json = json.loads(body)
    except ValueError:
        result_json = {}

    if status_code == HTTPStatus.OK:
        return result_json

    raise NetworkError(f"Status code error: {status_code}", result_json)


async def get_exchange_rates(currencies: list[str],
                             days: Optional[int] = None,
                             url: str = BASE_URL_PB_EXCHANGE) -> list[dict]:
    date_ = date.today() - timedelta(days=days - 1 if days else 0)

    exchange_rates: list[dict] = []

    async with aiohttp.ClientSession() as session:
        while date.today() >= date_:
            params = {"date": date_.strftime("%d.%m.%Y")}

            try:
                async with session.get(url, params=params) as response:
                    result_json = check_result(response.content_type,
                                               response.status,
                                               await response.text())

                    exchange_rates.append(json_formatter(result_json, currencies))
            except aiohttp.ClientError as e:
                print(f"aiohttp client throws an error: {e}\n")
            except NetworkError as e:
                text = {
                    date_.strftime("%d.%m.%Y"): {
                        "error message": e.message,
                        "body_json": e.body_json
                    }
                }
                print(json.dumps(text, indent=2), '\n')

            date_ += timedelta(days=1)

    return exchange_rates
