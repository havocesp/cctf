# -*- coding: utf-8 -*-
"""
 CCTF
 - Author:      Daniel J. Umpierrez
 - Created:     07-10-2018
 - License:     UNLICENSE
"""
import abc
import typing as tp
from collections import UserDict

__all__ = ['Precision', 'Limit', 'BaseDict', 'Meta']


class Meta(abc.ABCMeta):
    @classmethod
    def __prepare__(mcs, name, bases, **kwargs):
        return dict(**kwargs)

    @classmethod
    def __instancecheck__(cls, other):
        return isinstance(other, (str, cls))

    def __new__(mcs, name, bases, attrs, **kwargs):
        return type(name, bases + (str,), attrs)

    def __call__(cls, *args, **kwargs):
        return cls.__new__(*args, **kwargs)


class BaseDict(UserDict):
    """Dict base class."""

    @property
    def fields(self):
        """Return fields names as List[AnyStr] type.

        >>> BaseDict(min=0.0, max=1.0).fields
        ['min', 'max']

        """
        return self.keys()

    @property
    def to_list(self):
        """Return List[float] type containing Limit values.

        >>> BaseDict(min=0.0, max=10.0).to_list
        [0.0, 10.0]

        :return: list type containing Limit values.
        """
        return self.values()

    @property
    def to_dict(self):
        """Return a Dict[AntStr, float] type containing Limit values.

        >>> BaseDict(min=0.0, max=10.0).to_dict
        {'min': 0.0, 'max': 10.0}

        :return : dict type containing Limit values.
        """
        return dict(self.data)

    def items(self):
        """Dict key-pair items as list of tuples.

        :return: dict items as list type.
        """
        return list(self.data.items())

    def keys(self):
        """Return stored dict keys as list.

        :return: all stored dict keys as list.
        """
        return list(self.data.keys())

    def values(self):
        """Return stored dict values as list.

        :return: all stored dict values as list.
        """
        return list(self.data.values())

    def __str__(self):
        """String conversion formatter.

        >>> str(BaseDict(min=10.0, max=1000.0))
        '(min: 10.0, max: 1000.0)'

        :return: string conversion formatter.
        """
        return f'({", ".join(f"{k}: {v}" for k, v in self.items())})'

    def __repr__(self):
        """Return Range instance name followed by it values as string (min and max values separated by ", ")

        >>> BaseDict(min=10.0, max=1000.0)
        BaseDict(min: 10.0, max: 1000.0)

        :return: Range instance name followed by it values as string (min and max values separated by ", ")
        """
        return f'{type(self).__name__}{self.__str__()}'

    def __getattr__(self, item):
        """Dict entries accessing as class attributes implementation.

        :param str item: attribute name.
        :return: self.data value for item key.
        :raise AttributeError:
        """
        temp_data = super().__dict__.get('data')
        if temp_data is None:
            raise AttributeError(f'{item} not in data.')
        elif item not in 'data' and item in temp_data:
            return temp_data[item]
        elif item in temp_data:
            return temp_data
        else:
            raise AttributeError(f'{item} is not a valid attribute.')

    # def __getitem__(self, item):
    #     if isinstance(item, int) and item in [0, 1]:
    #         return self.min if item == 0 else self.max
    #     elif str(item) in ['min', 'max']:
    #         return vars(self).get(item, 0.0)
    #     else:
    #         raise IndexError(f'{str(item)} not in index.')


class Limit:
    """Limits class with amount, price and cost attributes."""

    def __init__(self, amount=None, price=None, cost=None, market=None):
        """Initialize Limits class with amount, price and cost values.

        >>> amount = dict(min=0, max=100)
        >>> price = dict(min=10, max=1000)
        >>> cost = dict(min=0.0, max=10000)
        >>> market = dict(min=0.0, max=10000)
        >>> Limit(amount=amount, price=price, cost=cost, market=market)
        Limit(amount: {'min': 0, 'max': 100}, price: {'min': 10, 'max': 1000}, cost: {'min': 0.0, 'max': 10000})

        """
        if isinstance(amount or 1, tp.Mapping):
            self.amount = amount
        else:
            self.amount = dict(min=0, max=0)
        if isinstance(price or 1, tp.Mapping):
            self.price = price
        else:
            self.price = dict(min=0, max=0)
        if isinstance(cost or 1, tp.Mapping):
            self.cost = cost
        else:
            self.cost = dict(min=0, max=0)
        if isinstance(market or 1, tp.Mapping):
            self.market = market
        else:
            self.market = dict(max=0, min=0)

        self.cost = cost
        self.price = price
        self.amount = amount
        self.market = market

    def __repr__(self):
        """Precision object str representation handler.

        :return str:
        """
        return 'Limit(amount: {amount}, price: {price}, cost: {cost})'.format(**{k: v for k, v in vars(self).items()})


class Precision:
    """Market precision class.

    >>> Precision()
    Precision(amount: 8, price: 8, cost: 8, base: 8, quote: 8)
    >>> Precision(amount=5, price=5, base=5, quote=3)
    Precision(amount: 5, price: 5, cost: 8, base: 5, quote: 3)
    >>> Precision(**dict(amount=3, price=10))
    Precision(amount: 3, price: 10, cost: 8, base: 8, quote: 8)

    """

    def __init__(self, amount=8, price=8, cost=8, base=8, quote=8):
        """Precision constructor.

        :param int base:  base currency precision (default 8).
        :param int quote: quote currency precision (default 8).
        :param int amount: amount precision (default 8).
        :param int price: price precision (default 8).
        :param int cost:  cost precision (default 8).
        """
        self.amount = amount
        self.price = price
        self.cost = cost
        self.base = base
        self.quote = quote

    def __repr__(self):
        """Precision object str representation handler.

        >>> Precision(amount=5, price=5, base=5, quote=3)
        Precision(amount: 5, price: 5, cost: 8, base: 5, quote: 3)

        :return str: Precision object str representation handler
        """
        template = 'Precision(amount: {amount}, price: {price}, cost: {cost}, base: {base}, quote: {quote})'
        return template.format(**vars(self))
