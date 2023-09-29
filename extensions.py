import json
import requests
from config import headers, keys

# для получения курса валют используется сервис https://api.apilayer.com/fixer

class ConvertionExseption(Exception):
    pass

class СurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if quote == base:
            raise ConvertionExseption(f'Невозможно перевести одинаковые валюты {quote}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionExseption(f'Неудалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionExseption(f'Неудалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionExseption(f'Неудалось обработать колоичество {amount}')


        r = requests.get(f'https://api.apilayer.com/fixer/latest?symbols={quote_ticker}&base={base_ticker}', headers)

        temp = json.loads(r.content)["rates"]
        total_base = temp[f'{quote_ticker}']

        return total_base