# -*- coding: utf-8 -*-
"""
 CCTF
 - Author:      Daniel J. Umpierrez
 - Created:     08-10-2018
 - License:     MIT
"""
import collections as col
import typing as tp

from cryptocmp import CryptoCmp

from cctf.symbol import Currency, CURRENCIES
from cctf.utils import num2str


class Balance(col.UserDict):
    """
    Balance class.
    """

    def __init__(self, **kwargs):
        """
        Balance class constructor.

        >>> balance = Balance(currency='BTC', total=0.1034)
        >>> balance.currency
        'BTC'

        :param kwargs: init data
        """

        if kwargs.get('currency') and kwargs.get('currency') in CURRENCIES.names:
            kwargs['currency'] = Currency(kwargs.get('currency'))  # type: Currency

        super().__init__(**kwargs)

        self.__dict__.update(**kwargs)

        self.total = self.__dict__.get('total', 0.0)
        if isinstance(self.total, dict):
            self.used = self.total.get('used', 0.0)
            self.total = self.total.get('total', 0.0)
        else:
            self.used = 0.0

        self.currency = self.__dict__.get('currency', Currency(''))

    @property
    def dict(self):
        return {str(self.currency): dict(used=self.used, total=self.total, free=self.free)}

    # noinspection PyUnusedFunction
    @property
    def free(self):
        """
        Returns free balance (total - used)

        :return float: free balance
        """
        return self.total - self.used

    def to(self, *currencies, timestamp=None):
        """
        Get balance amount value by using "currencies" price ratio.

        If timestamp is set price will be the historical at timestamp timeline point.

        >>> balance = Balance(currency='BTC', total=0.01711)
        >>> balance
        (BTC: 0.01711)
        >>> balance.total
        0.01711
        >>> balance.currency
        'BTC'
        >>> as_eur = balance.to_eur
        >>> isinstance(as_eur, float)
        True

        # >>> conversion = etc_balance.to('EUR')
        # >>> isinstance(conversion, float)
        True

        :param currencies: currencies used for conversion.
        :param int timestamp: number of seconds since 1970 (unix epoch)
        :return: price as float if one currency is supplied for conversion, otherwise a dict type will be returned.
        :rtype: float or dict
        """
        currencies = [Currency(c) for c in currencies]

        if timestamp:
            response = self.currency.to(ts=timestamp, *currencies)
        else:
            response = self.currency.to(*currencies)

        if 'Error' in response:
            print(' - [ERROR] {}'.format(response.get('Message')))
        else:

            if len(currencies) > 1:
                result = dict()
                for c in currencies:
                    ratio = response[self.currency].get(str(c), 0.0)
                    value = float(ratio * self.total)
                    result.update({c: dict(ratio=ratio, value=value)})
                return result if len(result) > 0 else result.get(currencies[0])
            else:
                return response.get(currencies[0])

    # noinspection PyUnusedFunction
    @property
    def to_eur(self):
        """
        Converts balance currency amount to EUR.
        >>> balance = Balance(currency='BTC', total=0.01711)
        >>> result = balance.to_eur
        >>> isinstance(result, float)
        True

        :return float: conversion result as float
        """
        if self.currency != 'EUR':
            return self.currency.to('EUR') * self.total
        else:
            return self.total

    # noinspection PyUnusedFunction
    @property
    def to_usd(self):
        """
        Converts balance currency amount to USD.

        >>> balance = Balance(currency='BTC', total=0.01711)
        >>> result = balance.to_usd
        >>> isinstance(result, float)
        True

        :return float: conversion result as float
        """
        if self.currency != 'USD':
            return self.currency.to('USD') * self.total
        else:
            return self.total

    # noinspection PyUnusedFunction
    @property
    def to_btc(self):
        """
        Converts balance currency amount to BTC.

        >>> balance = Balance(currency='XRP', total=160.1711)
        >>> result = balance.to_btc
        >>> isinstance(result, float)
        True

        :return float: conversion result as float
        """
        if self.currency != 'BTC':
            return self.currency.to('BTC') * self.total
        else:
            return self.total

    def __str__(self):
        return '({}: {})'.format(self.currency, num2str(self.total))

    def __repr__(self):
        return self.__str__()


# noinspection PyUnusedClass
class Wallet(tp.Dict[str, Balance]):
    def __init__(self, *args, **kwargs):
        """

        :param kwargs:
        """
        if len(args) and all((isinstance(b, Balance) for b in args)):
            for b in args:
                kwargs.update(**b.dict)
            # kwargs.update({str(b.currency): b.dict for b in args})
        super().__init__(**{str(k): Balance(currency=k, **v) for k, v in kwargs.items()})

    # noinspection PyUnusedFunction
    @property
    def currencies(self):
        return [c for c in sorted(self.keys())]

    # noinspection PyUnusedFunction,PySameParameterValue
    def get_total(self, as_currency=None):
        """
        Returns sum of wallet balances in a specific currency.
        >>> btc_balance = Balance(currency='BTC', total=0.0114, used=0.0232)
        >>> bcn_balance = Balance(currency='BCN', total=10000)
        >>> wallet = Wallet(btc_balance, bcn_balance)
        >>> usd_total = wallet.get_total('USD')
        >>> isinstance(usd_total, Balance)
        True


        # >>> isinstance(usd_total, float)


        :param as_currency:
        :type as_currency: str or Currency
        :return:
        """
        if str(as_currency) in ['USD', 'EUR', 'GBP', 'YEN', *CURRENCIES.names]:
            prices = CryptoCmp.get_price(fsyms=self.currencies, tsyms=as_currency)
            result = 0.0
            for fcoin, tcoin in prices.items():
                result += tcoin[str(as_currency)] * self.get(fcoin)['total']
            return Balance(currency=as_currency, total=result)

    def __contains__(self, item):
        return str(item) in self.keys()
