import sys
from typing import Optional

from constants import (
    ALL_AVAILABLE_CURRENCIES,
    DEFAULT_CURRENCIES,
)


def get_days() -> Optional[int]:
    try:
        days = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    except ValueError:
        print("You will be shown the exchange rate for the current day\n")
        return

    if days < 0:
        print("You will be shown the exchange rate for the current day\n")
        return

    if days > 10:
        print("The period for which you can receive exchange rates cannot exceed 10 days!\n"
              "The default exchange rates will only be displayed for the last 10 days.\n")
        return 10

    print(f"You will be shown the exchange rate for the last {days} days\n")
    return days


def get_currencies() -> list[str]:
    additional_currencies = ''

    for key, value in ALL_AVAILABLE_CURRENCIES.items():
        if key not in DEFAULT_CURRENCIES.keys():
            additional_currencies += f"\t{key}: {value}\n"

    default_currencies = " and ".join([f'{key} ({val})' for key, val in DEFAULT_CURRENCIES.items()])

    currencies = input("Enter the currencies from the list whose exchange rate you want to receive.\n"
                       f"{additional_currencies}"
                       f"(only {default_currencies} by default): ").upper().split(' ')

    currencies.extend(["USD", "EUR"])

    return currencies
