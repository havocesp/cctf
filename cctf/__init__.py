# -*- coding: utf-8 -*-
"""
 CCTF: Crypto-Currencies Trading Framework.
"""

__project__ = 'CCTF'
__package__ = 'cctf'
__description__ = __doc__
__author__ = 'Daniel J. Umpierrez'
__version__ = '0.1.0'
__license__ = 'MIT'
__site__ = 'https://github.com/havocesp/{}'.format(__package__)
__email__ = 'umpierrez@pm.me'
__keywords__ = ['altcoins', 'altcoin', 'exchange', 'bitcoin', 'trading']

import cctf.core
import cctf.symbol
from cctf.balance import Balance, Wallet
from cctf.core import Range, Precision, Limits
from cctf.market import Markets, Market, Tickers, Ticker
from cctf.symbol import Symbol, Symbols, Currency, Currencies, CURRENCIES

__all__ = ['__description__', '__author__', '__license__', '__version__', '__package__', '__project__', '__site__',
           '__email__', '__keywords__', 'core', 'symbol', 'Range', 'Precision', 'Limits', 'Symbol', 'Symbols',
           'Currency', 'Currencies', 'CURRENCIES', 'Markets', 'Market', 'Tickers', 'Ticker', 'Balance', 'Wallet']
