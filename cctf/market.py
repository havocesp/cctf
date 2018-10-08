# -*- coding: utf-8 -*-
"""
 CCTF
 - Author:      Daniel J. Umpierrez
 - Created:     08-10-2018
 - License:     MIT
"""
import collections

from cctf.core import Precision, Limits
from cctf.symbol import Symbol, Currency

__all__ = ['Markets', 'Market', 'Ticker', 'Tickers']


class Market(collections.UserDict):
    """
    Market class.

    >>> limit = dict(min=10, max=1000)
    >>> precision = dict(amount=8, price=5, quote=None)
    >>> limits = dict(amount=limit, price=limit, cost=limit)
    >>> data = {
    ... 'fee_loaded': True,
    ... 'percentage': True,
    ... 'tierBased': False,
    ... 'taker': None,
    ... 'maker': None,
    ... 'precision': precision,
    ... 'limits': limits,
    ... 'id': '100',
    ... 'symbol': 'BTC/USDT',
    ... 'base': 'BTC',
    ... 'quote': 'USDT',
    ... 'baseId': '1001',
    ... 'quoteId': '100',
    ... 'active': True
    ... }
    >>> market = Market(**data)
    >>> market.fee_loaded
    True
    >>> market.precision
    Precision(base=8, quote=8, amount=8, price=5)

    """

    def __init__(self, **kwargs):
        """
        Market constructor.
        """
        super().__init__(**kwargs)

        self._info = self.data.get('info', dict()) or dict()

        limit = dict(min=0.0, max=1000000.0)
        default_limits = dict(amount=limit.copy(), price=limit.copy(), cost=limit.copy())
        limits = {k: v for k, v in self.data.get('limits', default_limits).items() if v}
        default_precision = dict(amount=8, price=8, quote=8, base=8)
        default_precision.update(**{k: v for k, v in self.data.get('precision', default_precision).items() if v})

        self.precision = Precision(**default_precision)
        self.limits = Limits(**limits)
        self.symbol = Symbol(self.data.get('symbol', ''))
        self.base = Currency(self.data.get('base', ''))
        self.quote = Currency(self.data.get('quote', ''))
        self.baseId, self.quoteId = self.data.get('baseId') or self.base, self.data.get('quoteId') or self.quote
        self.fee_loaded = self.data.get('fee_loaded', False)
        self.percentage = self.data.get('percentage', False)
        self.tierBased = self.data.get('tierBased', False)
        self.taker = self.data.get('taker', 0.0)
        self.maker = self.data.get('maker', 0.0)
        self.id = self.data.get('id', self.symbol)
        self.active = self.data.get('active', False)


class Markets(collections.UserDict):
    """
    Markets class.
    """

    def __init__(self, **kwargs):
        """
        Markets class constructor.

        >>> Markets()

        :param kwargs:
        """
        data = dict()
        for k, v in kwargs.items():
            v = {x: y for x, y in v.items() if y is not None}

            m = Market(**v)

            data.update({k: m})
        # data = {k: Market(**{x: y for x,y in  v.items() if y}) for k, v in kwargs.items()}

        super().__init__(**data)


class Ticker(collections.UserDict):
    """
    Represent ticker data for specific market.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__dict__.update(**kwargs)
        self.last = self.data.get('last', 0.0)
        self.ask = self.data.get('ask', 0.0)
        self.bid = self.data.get('bid', 0.0)
        self.low = self.data.get('low', 0.0)
        self.high = self.data.get('high', 0.0)
        self.quoteVolume = self.data.get('quoteVolume', 0.0)
        self.baseVolume = self.data.get('baseVolume', 0.0)
        self.percentage = self.data.get('percentage', 0.0)
        self.id = self.data.get('percentage', '')
        self._info = self.data.get('info', dict())
    #
    # def __getattr__(self, item):
    #     if item in self.keys():
    #         return self.get(item)
    #     else:
    #         raise AttributeError()
    #
    # def __setattr__(self, key, value):
    #     if key in self.keys():
    #         self.update({key: value})
    #     else:
    #         raise AttributeError()


class Tickers(collections.UserDict):

    def __init__(self, **kwargs):
        data = dict.fromkeys(list(kwargs.keys()))

        for k, v in kwargs.items():
            data[k] = Ticker(**v)

        super().__init__(**data)

    # def __getattr__(self, item):
    #     if item in self.keys():
    #         return self.get(item)
    #     else:
    #         raise AttributeError()
    #
    # def __setattr__(self, key, value):
    #     if key in self.keys():
    #         self.update({key: value})
    #     else:
    #         raise AttributeError()
