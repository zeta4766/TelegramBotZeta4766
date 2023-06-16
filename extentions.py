import json
import requests
from config import dict_names
class Convert_exception(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        try:
            input_quote = dict_names[quote]
        except KeyError:
            raise Convert_exception(f'Не удалось обработать валюту {quote}')

        try:
            output_quote = dict_names[base]
        except KeyError:
            raise Convert_exception(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise Convert_exception(f'Не удалось обработать стоимость {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={input_quote}&tsyms={output_quote}')
        text = json.loads(r.content)[dict_names[base]]
        return round(text*amount, 2)