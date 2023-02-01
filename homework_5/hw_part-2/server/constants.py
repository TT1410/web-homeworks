from aiopath import AsyncPath


BASE_URL_PB_EXCHANGE = "https://api.privatbank.ua/p24api/exchange_rates"

DEFAULT_CURRENCIES = {
    "USD": "U.S. dollar",
    "EUR": "euro",
}

ALL_AVAILABLE_CURRENCIES = {
    "USD": "U.S. dollar",
    "EUR": "euro",
    "CHF": "swiss franc",
    "GBP": "british pound",
    "PLZ": "polish zloty",
    "SEK": "swedish krona",
    "XAU": "gold",
    "CAD": "canadian dollar",
}

LOGFILE_TXT = AsyncPath('.', 'logs.txt')
