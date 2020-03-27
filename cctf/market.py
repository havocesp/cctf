# -*- coding: utf-8 -*-
"""
 CCTF
 - Author:      Daniel J. Umpierrez
 - Created:     08-10-2018
 - License:     UNLICENSE
"""
import sys
from typing import Text, Dict, Union as U, Any

from cctf.base import Precision, Limit, BaseDict
from cctf.symbol import Symbol, Currency

__all__ = ['Markets', 'Market', 'Ticker', 'Tickers']

_DEFAULT_RANGE = dict(min=0.0, max=sys.maxsize)
_DEFAULT_LIMITS = dict(
    amount=_DEFAULT_RANGE.copy(),
    price=_DEFAULT_RANGE.copy(),
    cost=_DEFAULT_RANGE.copy())
_DEFAULT_PRECISION = dict(amount=8, price=8, quote=8, base=8)


class Market(BaseDict):
    """Market model class.

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
    Precision(amount: 8, price: 5, cost: 8, base: 8, quote: 8)

    """

    def __init__(self, **kwargs):
        """Market constructor.

        >>> data = {'quote': 'BTC',
        ...         'base': 'CHAT',
        ...         'quoteId': 'BTC',
        ...         'baseId': 'CHAT',
        ...         'limits': {
        ...             'amount': {'min': 0.0, 'max': 10000000000.0},
        ...             'price': {'min': 0.0, 'max': 10000000000.0},
        ...             'cost': {'min': 0.0, 'max': 10000000000.0}
        ...         },
        ...         'precision': {
        ...             'amount': 8,
        ...             'price': 10,
        ...             'cost': 8
        ...         }
        ... }
        >>> Market(**data).base
        'CHAT'

        :param kwargs: param names are identical to Exchange class markets from ccxt lib.
        """
        super(Market, self).__init__(**kwargs)

        self._info = self.data.get('info', dict()) or dict()

        limit = dict(min=0.0, max=1000000.0)
        default_limits = dict(amount=limit.copy(), price=limit.copy(), cost=limit.copy())
        limits = {k: v for k, v in self.data.get('limits', default_limits).items() if v}

        default_precision = dict(amount=8, price=8, quote=8, base=8)
        default_precision.update(**{k: v for k, v in self.data.get('precision', default_precision).items() if v})

        self.taker = self.data.get('taker')
        self.maker = self.data.get('maker')
        self.percentage = self.data.get('percentage', False)
        self.tier_based = self.data.get('tierBased', False)
        self.precision = Precision(**default_precision)
        self.limits = Limit(**limits)
        self.base = Currency(self.data.get('base'))
        self.quote = Currency(self.data.get('quote'))
        self.symbol = Symbol(f'{self.base}/{self.quote}')
        self.baseId = self.data.get('baseId') or self.base
        self.quoteId = self.data.get('quoteId') or self.quote
        self.id = self.data.get('id', self.symbol)
        self.active = self.data.get('active', False)

    def as_dict(self) -> Dict:
        """Return data as dict.

        :return: field->value data as dict.
        """
        return {k: v for k, v in self.data.items() if v is not None}

    def __repr_(self):
        """Precision object str representation handler.

        >>> Precision(amount=5, price=5, base=5, quote=3)
        Precision(amount: 5, price: 5, cost: 8, base: 5, quote: 3)

        :return str: Precision object str representation handler
        """
        template = 'Precision(amount: {amount}, price: {price}, cost: {cost}, base: {base}, quote: {quote})'
        return template.format(**vars(self))


class Markets(Dict[U[Text, Symbol], Dict]):
    """Markets class.

    Initialization data example:

    {
    'id':     'btcusd',   // string literal for referencing within an exchange
    'symbol': 'BTC/USD',  // uppercase string literal of a pair of currencies
    'base':   'BTC',      // uppercase string, base currency, 3 or more letters
    'quote':  'USD',      // uppercase string, quote currency, 3 or more letters
    'active': true,       // boolean, market status
    'precision': {        // number of decimal digits "after the dot"
        'price': 8,       // integer, might be missing if not supplied by the exchange
        'amount': 8,      // integer, might be missing if not supplied by the exchange
        'cost': 8,        // integer, very few exchanges actually have it
    },
    'limits': {           // value limits when placing orders on this market
        'amount': {
            'min': 0.01,  // order amount should be > min
            'max': 1000,  // order amount should be < max
        },
        'price': { ... }, // same min/max limits for the price of the order
        'cost':  { ... }, // same limits for order cost = price * amount
    },
    'info':      { ... }, // the original unparsed market info from the exchange
}
    """

    def __init__(self, **kwargs):
        """Markets class constructor.

        >>> Markets()
        {}

        :param kwargs:
        """
        init_data = dict()
        for k, v in kwargs.items():
            v = {x: y for x, y in v.items() if y is not None}
            m = Market(**v)
            init_data.update({Symbol(k): Market(**m)})
        super().__init__(**init_data)


class Ticker(Dict[Text, Any]):
    """Represent ticker data for specific market."""

    def __init__(self, **kwargs):
        init_data = {k: v for k, v in kwargs.items() if v}
        super().__init__(**init_data)

        self.last = self.get('last', 0.0)
        self.ask = self.get('ask', 0.0)
        self.bid = self.get('bid', 0.0)
        self.low = self.get('low', 0.0)
        self.high = self.get('high', 0.0)
        self.symbol = self.get('symbol', 0.0)
        self.quoteVolume = self.get('quoteVolume', 0.0)
        self.baseVolume = self.get('baseVolume', 0.0)
        self.percentage = self.get('percentage', 0.0)
        self.id = self.get('percentage')
        self._info = self.get('info', dict())


class Tickers(Dict[U[Text, Symbol], Ticker]):
    """Tickers class."""

    def __init__(self, **kwargs):
        """Constructor."""
        super().__init__({Symbol(k): Ticker(**v) for k, v in kwargs.items()})


class ExchangeInfo:

    def __init__(self, **kwargs):
        """
        {
            'id':   'exchange'                  // lowercase string exchange id
            'name': 'Exchange'                  // human-readable string
            'countries': [ 'US', 'CN', 'EU' ],  // array of ISO country codes
            'urls': {
                'api': 'https://api.example.com/data',  // string or dictionary of base API URLs
                'www': 'https://www.example.com'        // string website URL
                'doc': 'https://docs.example.com/api',  // string URL or array of URLs
            },
            'version':         'v1',            // string ending with digits
            'api':             { ... },         // dictionary of api endpoints
            'has': {                            // exchange capabilities
                'CORS': false,
                'publicAPI': true,
                'privateAPI': true,
                'cancelOrder': true,
                'createDepositAddress': false,
                'createOrder': true,
                'deposit': false,
                'fetchBalance': true,
                'fetchClosedOrders': false,
                'fetchCurrencies': false,
                'fetchDepositAddress': false,
                'fetchMarkets': true,
                'fetchMyTrades': false,
                'fetchOHLCV': false,
                'fetchOpenOrders': false,
                'fetchOrder': false,
                'fetchOrderBook': true,
                'fetchOrders': false,
                'fetchTicker': true,
                'fetchTickers': false,
                'fetchBidsAsks': false,
                'fetchTrades': true,
                'withdraw': false,
            },
            'timeframes': {                     // empty if the exchange !has.fetchOHLCV
                '1m': '1minute',
                '1h': '1hour',
                '1d': '1day',
                '1M': '1month',
                '1y': '1year',
            },
            'timeout':          10000,          // number in milliseconds
            'rateLimit':        2000,           // number in milliseconds
            'userAgent':       'ccxt/1.1.1 ...' // string, HTTP User-Agent header
            'verbose':          false,          // boolean, output error details
            'markets':         { ... }          // dictionary of markets/pairs by symbol
            'symbols':         [ ... ]          // sorted list of string symbols (traded pairs)
            'currencies':      { ... }          // dictionary of currencies by currency code
            'markets_by_id':   { ... },         // dictionary of dictionaries (markets) by id
            'proxy': 'https://crossorigin.me/', // string URL
            'apiKey':   '92560ffae9b8a0421...', // string public apiKey (ASCII, hex, Base64, ...)
            'secret':   '9aHjPmW+EtRRKN/Oi...'  // string private secret key
            'password': '6kszf4aci8r',          // string password
            'uid':      '123456',               // string user id
        }
        """
        self.id: str = kwargs.get('id')
        self.name: str = kwargs.get('name')
        self.countries: list = kwargs.get('countries')
        self.version: list = kwargs.get('version')
        self._has: list = kwargs.get('has')
        self.timeframes: dict = kwargs.get('timeframes')
        self.rate_limit: bool = kwargs.get('rateLimit')
        self.user_agent: bool = kwargs.get('userAgent')
        self.verbose: bool = kwargs.get('verbose')
        self.apikey: bool = kwargs.get('apiKey')
        self.secret: bool = kwargs.get('rateLimit')
        self.password: bool = kwargs.get('password')
        self.uid = kwargs.get('uid')
        self.proxy = kwargs.get('proxy')
        self.url_api: str = self._urls.get('api')
        self.url_doc: str = self._urls.get('doc')
        self.url_main: str = self._urls.get('www')
        self.markets: dict = kwargs.get('markets', dict())
        self.markets_by_id: dict = kwargs.get('markets_by_id', {})
        self.currencies: dict = kwargs.get('currencies', {})
        self.symbols: dict = kwargs.get('symbols', {})
        self._api = kwargs.get('api')
        self._urls: dict = kwargs.get('urls', {})
