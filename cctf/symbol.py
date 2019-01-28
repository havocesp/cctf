# -*- coding: utf-8 -*-
"""CCTF

 - Author:      Daniel J. Umpierrez
 - Created:     08-10-2018
 - License:     UNLICENSE
"""
import json
import pathlib as path
import time
from collections import UserDict

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

        # data = pd.read_json(_COIN_LIST_URL, )
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

    @property
    def names(self):
        """Currencies names as list.

        :return tp.List[tp.AnyStr]: currencies names as List[AnyStr]
        """
        return sorted(self.data.keys()) + ['EUR', 'USD']


CURRENCIES = globals().get('CURRENCIES', Currencies())


class Currency(metaclass=Meta):
    """Currency class."""

    def __new__(cls, s):
        return str.__new__(cls, str(s).upper())

    def __add__(self, other):
        """Create a Symbol by combining the self currency as base and the other as quote.

        >>> Currency('BTC') + 'USD'
        {Symbol} BTC/USD

        :param other: the other currency used for symbol creation.
        :type other: str or Currency
        :return Symbol: a Symbol instance formed from self and other currencies as quote and base respectively.
        """
        other = str(other).upper()
        if other in CURRENCIES.names:
            return Symbol('{}/{}'.format(super().__str__(), other))

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
        """If symbol is initialized, return base, quote Currency instances as tuple.

        >>> Symbol('BTC', 'ETH').parts
        ('BTC', 'ETH')

        :return tp.Tuple[Currency]: base, quote Currency instances as tuple.
        """
        if '/' in super().__str__():
            elements = super().__str__().split('/')
            return Currency(elements[0]), Currency(elements[1])

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
        return Currency(str(self).split('/')[1])

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
                raise IndexError('Index should be: 0->BaseCurrency, 1->QuoteCurrency')
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
            raise AttributeError('Only a callable type could be assigned to this class as attribute.')

    def price2precision(self):
        raise NotImplementedError()

    def amount2precision(self):
        raise NotImplementedError()

    def cost2precision(self):
        raise NotImplementedError()

    def __str__(self):
        """Symbol objects representation as str.

        :return: Symbol str representation for class instances.
        :rtype:
        """
        return super().__str__()

    def __repr__(self):
        """Symbol representation as str.

        :return: Symbol str representation for class instances.
        :rtype:
        """
        return '{Symbol} ' + super(Symbol, self).__str__()


class Symbols(UserDict):
    """Symbols dict like access class."""

    def __init__(self, **data):
        """Constructor."""
        super().__init__(**data)


if __name__ == '__main__':
    s = Symbol('BTC', 'USDT')
    print(s.price)
