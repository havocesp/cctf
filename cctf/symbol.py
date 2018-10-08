# -*- coding: utf-8 -*-
"""
 CCTF
 - Author:      Daniel J. Umpierrez
 - Created:     08-10-2018
 - License:     MIT
"""
import json
import pathlib as path
import time
from collections import UserDict
from logging import getLogger, INFO

import cryptocmp as ccmp

log = getLogger('{}: {}'.format(__package__, __file__.split('/')[-1].split('.')[0]))
log.setLevel(INFO)

CURRENCIES = dict()

__all__ = ['Symbol', 'Symbols', 'Currency', 'Currencies', 'CURRENCIES']


class Currency(str):
    """
    Currency class.
    """

    def __new__(cls, s):

        return str.__new__(cls, str(s).upper())

    def __add__(self, other):
        """
        Create a Symbol by combining the self currency as base and the other as quote.

        >>> Currency('BTC') + 'USD'
        'BTC/USD'

        :param other: the other currency used for symbol creation.
        :type other: str or Currency
        :return Symbol: a Symbol instance formed from self and other currencies as quote and base respectively.
        """
        other = str(other).upper()
        if other != self:
            return Symbol('{}/{}'.format(self, other))

    def to(self, *to_currencies, **kwargs):
        # noinspection PyUnresolvedReferences
        """
        Convert currency to other currencies contained in "to_currencies"

        >>> btc = Currency('BTC')
        >>> conversion = btc.to('USD')
        >>> isinstance(conversion, float) and conversion > 0.0
        True
        >>> conversion = btc.to('USD', 'EUR', 'ETH')
        >>> isinstance(conversion, dict) and all((isinstance(v, float) and v > 0.0 for v in conversion.values()))
        True

        :param to_currencies: currencies to convert to.
        :return:
        :rtype: float or dict
        """
        if to_currencies is None or not len(to_currencies):
            to_currencies = ['BTC' if self != 'BTC' else 'ETH']
        elif isinstance(to_currencies, str):
            to_currencies = [to_currencies]

        to_currencies = [str(c).upper() for c in to_currencies]
        timestamp = kwargs.get('timestamp')

        if timestamp and isinstance(timestamp, int):
            result = ccmp.CryptoCmp.get_historical_price(ts=timestamp, fsym=str(self), *to_currencies)
        else:
            result = ccmp.CryptoCmp.get_price(str(self), *to_currencies)

        return result.get(to_currencies[0], 0.0) if len(result) == 1 else result

    def __str__(self):
        """
        To str type converter.

        >>> str(Currency('BTC'))
        'BTC'

        :return str: str type with currency name
        """
        return super().__str__()

    def __repr__(self):
        """
        Class str type representation.

        >>> Currency('BTC')
        'BTC'

        :return str: str type representation.
        """
        return super().__repr__()

    def __contains__(self, item):
        """
        This is an "in" operator behaviour implementation.

        >>> 'BTC' in Currency('BTC')
        True
        >>> 'BTC' in Currency('ETH')
        False

        :return str: str type representation.
        """
        return item == self


class Symbol(str):
    """
    Symbol class.
    """

    def __new__(cls, *args, **kwargs):
        symbol = str()
        if '/' in str(args):
            symbol = str(args[0])
        elif len(args) >= 2:
            symbol = '{}/{}'.format(*args[:2])
        elif '/' in str(kwargs.get('symbol')):
            symbol = kwargs.get('symbol')
        elif kwargs.get('base') and kwargs.get('quote'):
            symbol = '{base}/{quote}'.format(**kwargs)
        elif kwargs.get('base') and kwargs.get('base') != 'BTC':
            symbol = '{base}/BTC'.format(**kwargs)

        return str.__new__(cls, str(symbol).upper())

    @property
    def parts(self):
        """
        If symbol is initialized, return base, quote Currency instances as tuple.

        >>> Symbol('BTC', 'ETH').parts
        ('BTC', 'ETH')

        :return tp.Tuple[Currency]: base, quote Currency instances as tuple.
        """
        if '/' in super().__str__():
            elements = self.split('/')
            return Currency(elements[0]), Currency(elements[1])

    @property
    def base(self):
        """
        Base currency as "Currency" instance.

        >>> Symbol('BTC/USD').base
        'BTC'

        """
        return self.parts[0]

    @property
    def quote(self):
        """
        Quote currency as "Currency" instance.

        >>> Symbol('BTC/USD').quote
        'USD'

        """
        return self.parts[1]

    @property
    def price(self):
        """
        Returns current price symbol.

        >>> price = Symbol('BTC/USD').price
        >>> isinstance(price, float) and price > 0.0
        True

        :return float: current price symbol.
        """
        return self.base.to(self.quote)

    def __getattr__(self, item):
        """
        If item match with either quote or base currency of the Symbol class instance a Currency instance will be
        return, otherwise, AttributeError will be raised.

        >>> Symbol('BTC/USD').BTC
        'BTC'

        :param item:
        :return Currency:
        :raise: AttributeError
        """
        if item in self.parts:
            return self.base if item == self.parts[0] else self.quote
        else:
            raise AttributeError('Invalid {} attribute.'.format(str(item)))

    def __getitem__(self, item):
        """
        Gets symbol currency by position or by currency name.

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
                raise IndexError('Index should be: 0->BaseCurrency, 1->QuoteCurrency')
        elif item in self.parts:
            return self.base if item == self.parts[0] else self.quote
        raise TypeError()

    def __reversed__(self):
        """
        Return an inverted Symbol instance.

        >>> reversed(Symbol('BTC/USD'))
        'USD/BTC'

        :return: reversed version of a Symbol currencies.
        """

        return self.quote + self.base

    def __str__(self):
        """
        Class str type representation.

        >>> str(Symbol('BTC/USDT'))
        'BTC/USDT'

        :return str: str type representation.
        """
        return super().__str__()

    def __repr__(self):
        """
        Class str type representation.

        >>> str(Currency('BTC/USDT'))
        'BTC/USDT'

        :return str: str type representation.
        """
        return super().__repr__()

    def __contains__(self, item):
        """
        This is an "in" operator behaviour implementation.

        >>> 'BTC' in Symbol('BTC/ETH')
        True
        >>> 'ETH' in Symbol('BTC/ETH')
        True
        >>> 'BTC/ETH' in Symbol('BTC/ETH')
        True
        >>> 'ETH/BTC' in Symbol('BTC/ETH')
        False
        >>> 'ET' in Symbol('BTC/ETH')
        False

        :return str: True if item currency or symbol is contained / equal to Symbol
        """
        return item in self.parts or item == str(self)


class Currencies(UserDict):
    """
    Currencies container.

    Loads all currencies metadata (from cached file or from server).

    >>> currencies = Currencies()
    >>> 'BTC' in currencies.names
    True

    """

    def __init__(self):
        self._data = self._load()

        super().__init__(**self._data)
        self.__dict__.update(**self._data)

    def __getattr__(self, item):
        if item in self:
            return Currency(self[self.index(item)])

    @staticmethod
    def _load():
        """
        Currencies data loader and cache data handler.

        :return dict: currencies data as dict.
        """
        # path to data dir
        data_dir = path.Path.cwd().joinpath('data')
        # create data dir (if not exists)
        data_dir.mkdir(parents=True, exist_ok=True)
        # path to cache file
        currencies_cache_file = data_dir.joinpath('currencies.json')
        # check if cache file exists
        if currencies_cache_file.is_file():
            # check if cache file is older than 24 hours
            ctime = currencies_cache_file.stat().st_ctime
            if int(time.time()) - ctime < 3600 * 24:
                # load from cache
                log.debug('Using cache file: {}'.format(str(currencies_cache_file)))
                data = json.loads(currencies_cache_file.read_text())
            else:
                # overwrite cache file with new content
                log.debug('Cache file is too old, updating ...')
                data = ccmp.CryptoCmp.get_coin_list() or dict()
                with open(str(currencies_cache_file), 'wt') as fp:
                    json.dump(data, fp)
        else:
            # generate a new cache file
            log.debug('No cache file was found, creating a new one at: {}'.format(str(currencies_cache_file)))
            data = ccmp.CryptoCmp.get_coin_list() or dict()
            with open(str(currencies_cache_file), 'wt') as fp:
                json.dump(data, fp)
        return data

    @property
    def names(self):
        """
        Currencies names as list.

        :return tp.List[tp.AnyStr]: currencies names as List[AnyStr]
        """
        return list(sorted(self.keys()))


# noinspection PyUnusedClass
class Symbols(UserDict):
    pass
    # def __init__(self, **kwargs):
    #     self._data = ccmp.CryptoCmp
    #     super().__init__(**kwargs)


# noinspection PyRedeclaration
CURRENCIES = Currencies()
