# -*- coding: utf-8 -*-
"""CCTF

 - Author:      Daniel J. Umpierrez
 - Created:     08-10-2018
 - License:     UNLICENSE
"""
import json
import pathlib as path
import time
from typing import Iterable as Iter, Mapping as Map, List, Text, Union as U

from cctf.base import Meta, BaseDict
from cctf.utils import get_url, get_price

_DEBUG = False
_DATA_DIR = path.Path.home().joinpath('.local', 'cctf')
_DATA_DIR.mkdir(exist_ok=True, parents=True)
_CACHE_DIR = _DATA_DIR.joinpath('cache')
_CACHE_DIR.mkdir(exist_ok=True, parents=True)
_COIN_LIST_URL = 'https://min-api.cryptocompare.com/data/all/coinlist'

__all__ = ['Symbol', 'Symbols', 'Currency', 'Currencies', 'CURRENCIES']


class Currencies(BaseDict):
    """Currencies class model.

    Loads all currencies metadata (from cached file or from server).

    >>> currencies = Currencies()
    >>> 'BTC' in currencies.names
    True

    """

    def __init__(self):
        d = self._load()
        super(Currencies, self).__init__(**d)

    def __get__(self, item):
        if item in self.data.keys():
            return Currency(self.data[item])
        else:
            return self.__dict__[item]

    @property
    def names(self):
        """Currencies names as list.

        :return tp.List[tp.AnyStr]: currencies names as List[AnyStr]
        """
        return sorted(set(list(self.data) + ['EUR', 'USD']))

    def _get_metadata(self):
        """Get currencies metadata from cryptocompare site.

        >>> data = Currencies()._get_metadata()
        >>> len(data) > 0
        True
        >>> 'BTC' in data
        True

        :return dict:
        """
        data = dict()

        response = get_url(_COIN_LIST_URL)

        if isinstance(response or [], dict) and len(response):
            try:
                if response['Response'] == 'Success':
                    data = response['Data']
                    cache_file = _CACHE_DIR.joinpath('currencies.json')
                    cache_file.touch(exist_ok=True)
                    with open(str(cache_file), 'wt') as fp:
                        json.dump(data, fp, indent=2)
            except ValueError as err:
                if _DEBUG:
                    print(str(err))
        return data

    def _load(self, force_reload=False):
        """Currencies data loader and cache data handler.

        :return dict: currencies data as dict.
        """
        # path to cache file
        cache_file = _CACHE_DIR.joinpath('currencies.json')
        cache_file.touch(exist_ok=True)

        # check if cache file is older than 24 hours
        ctime = cache_file.stat().st_ctime
        if not force_reload and int(time.time()) - ctime < 3600 * 24:
            # load from cache
            if _DEBUG:
                print(' - Using cache file: {}'.format(str(cache_file)))
            try:
                data = json.loads(cache_file.read_text())
            except json.JSONDecodeError:
                data = self._get_metadata() or dict()
                if data is not None and len(data):
                    with open(str(cache_file), 'wt') as fp:
                        json.dump(data, fp, indent=2)

        else:
            # overwrite cache file with new content
            if _DEBUG:
                print(' - Updating cache file ...')
            data = self._get_metadata() or dict()
            if data is not None and len(data):
                with open(str(cache_file), 'wt') as fp:
                    json.dump(data, fp, indent=2)

        return data


CURRENCIES = globals().get('CURRENCIES', Currencies())


class Currency(metaclass=Meta):
    """Currency class."""

    def __new__(cls, s):
        return str.__new__(cls, str(s).upper())

    def __add__(self, other):
        """Create a Symbol by combining the self currency as base and the other as quote.

        >>> Currency('BTC') + 'USD'
        (Symbol:BTC/USD)

        :param other: the other currency used for symbol creation.
        :type other: str or Currency
        :return Symbol: a Symbol instance formed from self and other currencies as quote and base respectively.
        """
        other = str(other).upper()
        if other in CURRENCIES.names:
            symbol_str = '{}/{}'.format(self, other)
            return Symbol(symbol_str)

    def to(self, to_currency):
        """Convert currency to other currencies contained in "to_currencies"

        >>> btc = Currency('BTC')
        >>> conversion = btc.to('USD')
        >>> isinstance(conversion, float) and conversion > 0.0
        True

        :param to_currency: currencies to convert to.
        :return float: current price in "to_currency" currency.
        """
        result = get_price(str(self), to_currency)
        return result

    def __contains__(self, item):
        """This is an "in" operator behaviour implementation.

        >>> 'BTC' in Currency('BTC')
        True
        >>> 'BTC' in Currency('ETH')
        False

        :return str: str type representation.
        """
        return str(item) == str(self)


class Symbol(metaclass=Meta):
    """Symbol class."""

    def __new__(cls, symbol=None, base=None, quote=None):
        assert (symbol and '/' in symbol) or len(
            [e for e in (symbol, base, quote)]) > 1, 'No symbol name or base currency was supplied.'
        symbol = str(symbol or '')
        if '/' in symbol:
            symbol = symbol.upper()
        elif symbol and base and quote is None:
            symbol = f'{symbol}{quote}'
        elif base and quote and symbol is None:
            symbol = f'{base}{quote}'
        else:
            err_msg = f'- Symbol {symbol or "Empty"} is not valid (no "/" separator found (example: BTC/ETH).'
            raise ValueError(err_msg)

        if len(base or str()) and len(quote or str()):
            symbol = f'{str(base).upper()}/{str(quote).upper()}'
        elif len(base or str()):
            symbol = f'{str(base).upper()}/BTC'

        return str.__new__(cls, symbol)

    @property
    def parts(self):
        """If symbol is initialized, return base, quote Currency instances as tuple.

        >>> Symbol('BTC/ETH').parts
        ['BTC', 'ETH']

        :return tp.Tuple[Currency]: base, quote Currency instances as tuple.
        """
        if '/' in super().__str__():
            obj_str = super().__str__()
            elements = map(Currency, obj_str.split('/'))
            return list(elements)

    @property
    def base(self):
        """Base currency as "Currency" instance.

        >>> Symbol('BTC/USD').base
        'BTC'

        """
        return Currency(str(self).split('/')[0])

    @property
    def quote(self):
        """Quote currency as "Currency" instance.

        >>> Symbol('BTC/USD').quote
        'USD'

        """
        raw = str(self).split('/')
        if len(raw) > 1:
            return Currency(raw[1])

    @property
    def price(self):
        """Returns current price symbol.

        >>> price = Symbol('BTC/USD').price
        >>> isinstance(price, float) and price > 0.0
        True

        :return float: current price symbol.
        """
        return self.base.to(self.quote)

    def as_dict(self):
        """Return class attributes as dict (useful to be use with "print" function)

        >>> Symbol('BTC/USD').as_dict()
        {'base': 'BTC', 'quote': 'USD'}

        :return dict: class attributes as dict
        """
        return {'base': self.base, 'quote': self.quote}

    def __getattr__(self, item):
        """If item match with either quote or base currency of the Symbol class instance a Currency instance will be
        return, otherwise, AttributeError will be raised.

        >>> Symbol('BTC/USD').BTC
        'BTC'

        :param item:
        :return Currency:
        :raise: AttributeError
        """
        if any(item == c for c in map(str, super().__str__().split('/'))):
            return self.base if item == self.parts[0] else self.quote
        else:
            raise AttributeError('Invalid {} attribute.'.format(str(item)))

    def __getitem__(self, item):
        """Gets symbol currency by position or by currency name.

        >>> btc_usd = Symbol('BTC/USD')
        >>> btc_usd[0]
        'BTC'
        >>> btc_usd['USD']
        'USD'
        >>> btc_usd[Currency('USD')]
        'USD'

        :param item:
        :return: Currency instance if item is either base or quote currencies of this Symbol instance.
        """
        if isinstance(item, int) and item in [0, 1]:
            if item == 0:
                return self.base
            elif item == 1:
                return self.quote
            else:
                raise IndexError(
                    'Index should be: 0->BaseCurrency, 1->QuoteCurrency')
        elif item in self:
            return self.base if item == self.parts[0] else self.quote
        raise TypeError()

    def __contains__(self, item):
        """This is an "in" operator behaviour implementation.

        >>> 'BTC' in Symbol('BTC/ETH')
        True
        >>> Currency('ETH') in Symbol('BTC/ETH')
        True
        >>> 'BTC/ETH' in Symbol('BTC/ETH')
        True
        >>> 'ETH/BTC' in Symbol('BTC/ETH')
        False
        >>> 'ET' in Symbol('BTC/ETH')
        False

        :return str: True if item currency or symbol is contained / equal to Symbol
        """
        if isinstance(item, Currency) or '/' not in str(item):
            currencies = super().__str__().split('/')
            return any(str(item) == c for c in map(str, currencies))
        elif isinstance(item, Symbol) or '/' in str(item):
            return str(item) == str(self)
        elif str(item) == '/':
            return True
        else:
            currencies = super().__str__().split('/')
            return any(str(item) == c for c in map(str, currencies))

    def __setattr__(self, key, value):
        if key in '_str' or hasattr(value or '', '__call__'):
            self.__dict__.update({key: value})
        else:
            raise AttributeError(
                'Only a callable type could be assigned to this class as attribute.')

    def price2precision(self):
        raise NotImplementedError()

    def amount2precision(self):
        raise NotImplementedError()

    def cost2precision(self):
        raise NotImplementedError()

    def __repr__(self):
        """Symbol representation as str.

        >>> Symbol('BTC/USD')
        (Symbol:BTC/USD)

        :return: Symbol str representation for class instances.
        :rtype:
        """
        return f'(Symbol:{self})'

    def __str__(self):
        """Symbol representation as str.

        >>> Symbol('BTC', 'USD')
        (Symbol:USD/BTC)

        :return: Symbol str representation for class instances.
        :rtype:
        """
        return super().__str__()


class Symbols(List[U[Symbol, Text]]):
    """Symbols list like access class."""

    def __init__(self, *symbols):
        """Constructor."""
        symbols = list(symbols)
        if len(symbols) == 1:
            if isinstance(symbols[0], Text):
                symbols = [symbols[0]]
            elif isinstance(symbols[0], Map):
                symbols = list(dict(**symbols[0]).keys())
            elif isinstance(symbols[0], Iter):
                symbols = list(symbols[0])
        super().__init__(self._str2symbol(*symbols))

    def __add__(self, other):
        if isinstance(other, str) and '/' in other:
            self.append(Symbol(other))
        else:
            raise ValueError(f'Invalid symbol {str(other)}.')

    def _str2symbol(self, *symbols) -> List[Symbol]:
        result = [Symbol(s) for s in map(str, symbols) if '/' in s]
        return result

    def extend(self, other: Iter[U[Symbol, Text]]):
        super().extend(map(Symbol, other))


# class Currencies(List[U[Currency, Text]]):
#     """Currencies list like access class."""
#
#     def __init__(self, *currencies):
#         """Constructor."""
#         if len(currencies) == 1:
#             if isinstance(currencies[0], Text):
#                 currencies = [currencies[0]]
#             elif isinstance(currencies[0], Map):
#                 currencies = list(dict(**currencies[0]).keys())
#             elif isinstance(currencies[0], Iter):
#                 currencies = list(currencies[0])
#         super().__init__(self._str2currency(*currencies))
#
#     def __add__(self, other):
#         if isinstance(other, str) and len(other):
#             self.append(Currency(other.upper()))
#         else:
#             raise ValueError(f'Invalid currency {str(other)}.')
#
#     def extend(self, other: Iter[U[Currency, Text]]):
#         super().extend(map(Currency, other))
#
#     def _str2currency(self, *currencies):
#         return [Currency(c) for c in map(str, currencies) if len(c.strip())]


if __name__ == '__main__':
    print(len(Currencies().names))
    # symbol = 'MATIC/USDT'
    # symbols = Symbols(symbol, Symbol('LINK/USDT'))
    # symbols.extend(['BTT/USDT', 'CELR/USDT'])
    #
    # for s in symbols:
    #     print(s)
    # btc = Currency('BTC')
    # usdt = Currency('USDT')
    # s = Symbol('BTC', quote='USDT')
    # print(btc)
    # print(usdt)
    # print(btc + usdt)
    # print(s)
