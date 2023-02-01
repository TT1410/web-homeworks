import json
import platform
import asyncio

from src import (
    get_exchange_rates,
    get_currencies,
    get_days,
)


async def main() -> None:
    result = await get_exchange_rates(
        currencies=get_currencies(),
        days=get_days(),
    )

    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
