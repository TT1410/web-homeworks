from constants import ALL_AVAILABLE_CURRENCIES


def json_formatter(data: dict, currencies: list[str]) -> dict:
    """
    Формується потрібний json-формат курсу валют, при цьому ж відразу фільтром відкидаються непотрібні валюти
    та самі валюти сортуються у тому порядку,
    в якому вони стоять у дефолтному словнику доступних валют ALL_AVAILABLE_CURRENCIES
    """
    return {
        data['date']: dict(sorted({
            exrate['currency']: {
                'sale': exrate.get('saleRate', exrate['saleRateNB']),
                'purchase': exrate.get('purchaseRate', exrate['purchaseRateNB'])
            } for exrate in filter(lambda x: x['currency'] in currencies, data['exchangeRate'])}.items(),
                                  key=lambda x: list(ALL_AVAILABLE_CURRENCIES.keys()).index(x[0])))
    }