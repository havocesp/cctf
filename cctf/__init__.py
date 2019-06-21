# -*- coding: utf-8 -*-
"""CCTF
Crypto-Currencies Trading Framework.
"""
from cctf.balance import Balance, Wallet
from cctf.base import Range, Precision, Limit, Meta
from cctf.market import Markets, Market, Tickers, Ticker
from cctf.orders import Side, Order, OHLC, TradeFields
from cctf.symbol import Symbol, Symbols, Currency, Currencies, CURRENCIES

__project__ = 'CCTF'
__package__ = 'cctf'
__description__ = __doc__
__author__ = 'Daniel J. Umpierrez'
__version__ = '0.1.2'
__license__ = 'LGPL-3.0'
__site__ = 'https://github.com/havocesp/{}'.format(__package__)
__email__ = 'umpierrez@pm.me'

__all__ = ['__description__', '__author__', '__license__', '__version__', '__project__', '__site__', '__email__',
           'Range', 'Precision', 'Limit', 'Symbol', 'Symbols', 'Currency', 'Currencies', 'CURRENCIES', 'Markets',
           'Market', 'Tickers', 'Ticker', 'Balance', 'Wallet', 'Side', 'Order', 'Meta', 'OHLC', 'TradeFields']
