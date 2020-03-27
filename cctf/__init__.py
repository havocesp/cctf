# -*- coding: utf-8 -*-
"""CCTF

Crypto-Currencies Trading Framework.
"""
import sys

from cctf.balance import Balance, Wallet
from cctf.base import Limit, Meta
from cctf.market import Markets, Market, Tickers, Ticker
from cctf.orders import Side, Order, OHLC, TradeFields
from cctf.symbol import Symbol, Symbols, Currency, Currencies, CURRENCIES

# from ccxt import binance

sys.setrecursionlimit(250)

__project__ = 'CCTF'
__package__ = 'cctf'
__description__ = __doc__
__author__ = 'Daniel J. Umpierrez'
__version__ = '0.1.2'
__license__ = 'UNLICENSE'
__site__ = 'https://github.com/havocesp/{}'.format(__package__)
__email__ = 'umpierrez@pm.me'

__all__ = ['__description__', '__author__', '__license__', '__version__', '__project__', '__site__', '__email__',
           'Limit', 'Symbol', 'Symbols', 'Currency', 'Currencies', 'CURRENCIES', 'Markets',
           'Market', 'Tickers', 'Ticker', 'Balance', 'Wallet', 'Side', 'Order', 'Meta', 'OHLC', 'TradeFields']

#
# def main(base_market=None, min_timeframe_volume=0.001, min_ticker_volume=0.0, timeframe=None):
#     base_market = base_market or 'BTC'
#
#     api = binance(dict(timeout=15000, enableRateLimit=True))
#
#     markets = api.load_markets()
#
#     symbols = [s for s in markets if s.endswith(base_market)]
#
#     tickers = api.fetch_tickers(symbols)
#
#     if min_ticker_volume > 0.0:
#         tickers = {k: v for k, v in tickers.items(
#         ) if v['quoteVolume'] > min_ticker_volume and k.split('/')[0] not in ('PAX', 'USDC', 'TUSD')}
#
#     prev_result = list()
#     clear(), pos(1, 1)
#
#     while True:
#
#         counter = 0
#         result = list()
#         for k, v in tickers.items():
#             pos(1, 1), clearLine()
#             counter += 1
#             print(f' - ({counter}/{len(tickers)}) Loading data for {k} symbol ...')
#             ohlc = api.fetch_ohlcv(k, timeframe=timeframe or '1m', limit=5)
#             time.sleep(uniform(.1, .2))
#             date, open, high, low, close, volume = ohlc[-1]
#             quote_volume = volume * close
#             if quote_volume > min_timeframe_volume:
#                 result.append([[quote_volume, 0.0], k])
#
#         result = sorted(result, key=lambda s: s[0][0], reverse=True)
#
#         if len(prev_result) == 0:
#             prev_result = result
#         else:
#             temp = result.copy()
#
#             prev_symbols = [s[1] for s in prev_result]
#
#             for i, r in enumerate(result.copy()):
#                 volume, symbol = r
#                 if symbol in prev_symbols:
#                     prev_volume = prev_result[prev_symbols.index(r[1])][0]
#                 else:
#                     prev_volume = volume
#                 result[i][0] = [volume[0], volume[0] - prev_volume[0]]
#
#             prev_result = temp
#         clear(), pos(2, 1)
#
#         for row in result:
#             vol, symbol = row
#             vol, diff = vol
#             base, quote = symbol.split('/')
#             if 'USD' in quote:
#                 volume = f'{vol:,.0f}'
#                 diff = f'({diff:+,.0f})'
#             else:
#                 volume = f'{vol:.8f}'
#                 diff = f'({diff:+.8f})'
#             print(f' * {symbol:<10} -> {volume:>12} {diff:>12}')
#
#         time.sleep(5)
#
#
# if __name__ == '__main__':
#     sys.argv.extend(['-b', 'USDT', '-T', '5m', '-t', '6000000', '-m', '50000'])
#
#     parser = argparse.ArgumentParser()
#     parser.add_argument('-b', '--base-market', default='BTC')
#     parser.add_argument('-T', '--timeframe', default='1m')
#     parser.add_argument('-m', '--min-timeframe-volume', type=float, default=0.01)
#     parser.add_argument('-t', '--min-ticker-volume', type=float, default=1.0)
#
#     args = parser.parse_args(sys.argv[1:])
#
#     main(**vars(args))
