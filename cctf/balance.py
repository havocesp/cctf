# -*- coding: utf-8 -*-
"""CCTF

 - Author:      Daniel J. Umpierrez
 - Created:     08-10-2018
 - License:     UNLICENSE
"""
import collections as col
import typing as tp

from cctf.symbol import Currency, CURRENCIES
from cctf.utils import num2str


class Balance(col.UserDict):
    """Balance class."""

    def __init__(self, **kwargs):
        """Balance class constructor.

        >>> balance = Balance(currency='BTC', total=0.1034)
        >>> balance.currency
        'BTC'

        :param kwargs: init data
        """
        self._precision = 8

        if kwargs.get('currency') and kwargs.get('currency') in CURRENCIES.names:
            kwargs['currency'] = Currency(kwargs.get('currency'))  # type: Currency

        super().__init__(**kwargs)

        self.currency = self.data.get('currency', Currency(''))

    @property
    def dict(self):
        """Get balance data as dict type."""
        return {str(self.currency): dict(used=self.used, total=self.total, free=self.free)}

    @property
    def used(self):
        """Returns used balance (total - free)

        :return float: used balance
        """
        return self.data.get('used', 0.0)

    @used.setter
    def used(self, value):
        """Getter for "used" attribute.

        :param float value: value to be assigned
        """
        self.data.update(used=value or 0.0)

    @property
    def total(self):
        """Returns total balance (free + used)

        :return float: total balance
        """
        return self.data.get('total', 0.0)

    @total.setter
    def total(self, value):
        """
        Getter for "total" attribute.

        :param float value: value to be assigned
        """
        self.data.update(total=value or 0.0)

    @property
    def free(self):
        """Returns free balance (total - used)

        :return float: free balance
        """
        return self.data.get('free', 0.0)

    @free.setter
    def free(self, value):
        """Getter for "free" attribute.

        :param float value: value to be assigned
        """
        self.data.update(free=value or 0.0)

    def to(self, currency):
        """Get balance amount value by using "currencies" price ratio.

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
        if currency is not None and isinstance(currency or 0, str):
            currency = Currency(currency)
        else:
            raise ValueError('Value for "currency" should be str type.')
        response = self.currency.to(currency)
        return response

    @property
    def to_eur(self):
        """Converts balance currency amount to EUR.

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

    @property
    def to_usd(self):
        """Converts balance currency amount to USD.

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

    @property
    def to_btc(self):
        """Converts balance currency amount to BTC.

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

    def __float__(self):
        """Return total balance as float.

        >>> balance = Balance(total=100.0)
        >>> float(balance)
        100.0

        :return float: total balance value ("total" property).
        """
        return float(self.total)

    def __eq__(self, other):
        """Equal implementation to support Balance as "other".

        >>> eur = Balance(total=100.0, currency='EUR')
        >>> usd = Balance(total=100.0, currency='USD')
        >>> eur == Balance(total=100.0, currency='EUR')
        True
        >>> eur == 100.0
        True
        >>> eur == usd
        False
        >>> eur == Balance(total=99.99, currency='EUR')
        False

        :param other: the int, float or Balance to compare to.
        :type other: int or float or Balance
        :return bool: True if other is equal to self.total (and self.currency is the same as other if other is Balance)
        """
        if isinstance(other or '', Balance):
            return other.total == self.total and self.currency == other.currency
        elif isinstance(other, (float, int)):
            return self.total == float(other)
        else:
            return False

    def __round__(self, n=None):
        self._precision = n or 8
        self.total = round(self.total, n or 8)
        self.free = round(self.free, n or 8)
        self.used = round(self.used, n or 8)

    def __str__(self):
        return format(self.total, '.@f'.replace('@', str(self._precision)))

    def __repr__(self):
        return '({}: {})'.format(self.currency, num2str(self.total))


# noinspection PyUnusedClass
class Wallet(tp.Dict[str, Balance]):
    def __init__(self, *args, **kwargs):
        """Class constructor.

        :param args:
        :param kwargs:
        """
        if len(args) and all((isinstance(b, Balance) for b in args)):
            for b in args:
                kwargs.update(**b.dict)
            # kwargs.update({str(b.currency): b.dict for b in args})
        super().__init__(**{str(k): Balance(currency=k, **(dict(total=v) if isinstance(v, float) else v)) for k, v in
                            kwargs.items()})

    @property
    def currencies(self):
        return [c for c in sorted(self.keys())]

    def __contains__(self, item):
        return str(item) in self.keys()

    # def get_total(self, as_currency=None):
    #     """
    #     Returns wallet value estimation.
    #
    #     >>> btc_balance = Balance(currency='BTC', total=0.0114, used=0.0232)
    #     >>> bcn_balance = Balance(currency='BCN', total=10000)
    #     >>> wallet = Wallet(btc_balance, bcn_balance)
    #     >>> usd_total = wallet.get_total('USD')
    #     >>> isinstance(usd_total, Balance)
    #     True
    #
    #     # >>> isinstance(usd_total, float)
    #
    #     :param as_currency:
    #     :type as_currency: str or Currency
    #     :return:
    #     """
    #     if str(as_currency) in ['USD', 'EUR', 'GBP', 'YEN', *CURRENCIES.names]:
    #         prices = CryptoCmpy.get_price(fsyms=self.currencies, tsyms=as_currency)
    #         result = 0.0
    #         for fcoin, tcoin in prices.items():
    #             result += tcoin[str(as_currency)] * self.get(fcoin)['total']
    #         return Balance(currency=as_currency, total=result)
