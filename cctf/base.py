# -*- coding: utf-8 -*-
"""
 CCTF
 - Author:      Daniel J. Umpierrez
 - Created:     07-10-2018
 - License:     UNLICENSE
"""
import abc
import random
import typing as tp
from collections import UserDict

__all__ = ['Range', 'Precision', 'Limit', 'BaseDict', 'Meta']


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
    def to_tuple(self):
        """Return Tuple[float] type containing min and max values.

        >>> BaseDict(min=0.0, max=10.0).to_tuple
        (0.0, 10.0)

        :return tp.Tuple[float]: Tuple[float] type containing Limit values.
        """
        return float(self.data['min']), float(self.data['max'])

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
        return '({})'.format(', '.join('{}: {}'.format(k, v) for k, v in self.items()))

    def __repr__(self):
        """Return Range instance name followed by it values as string (min and max values separated by ", ")

        >>> BaseDict(min=10.0, max=1000.0)
        BaseDict(min: 10.0, max: 1000.0)

        :return: Range instance name followed by it values as string (min and max values separated by ", ")
        """
        return '{}{}'.format(type(self).__name__, self.__str__())

    def __getattr__(self, item):
        """Dict entries accessing as class attributes implementation.

        :param str item: attribute name.
        :return: self.data value for item key.
        :raise Attrib?uteError:
        """

        if item not in 'data' and item in self.data:
            return self.data[item]
        elif item in vars(self):
            return vars(self).get(item, self.data)
        else:
            raise AttributeError('{} is not a valid attribute.'.format(item))


class Range(BaseDict):
    """Range class.

    >>> Range(min=100.0, max=1000.0).min
    100.0

    """
    MAX = 1000000000.0
    MIN = 0.0

    def __init__(self, **kwargs):
        """
        Init Range instance with min an max values.

        >>> rang = Range(min=10.0, max=100.0)
        >>> rang
        Range(min: 10.0, max: 100.0)
        >>> str(rang)
        '(min: 10.0, max: 100.0)'

        :param kwargs:  max - max keys used as range delimiter as str or float.
        """
        super().__init__(**{k: float(v) for k, v in kwargs.items()})
        if not len(self.data):
            self.data.update(**{'min': self.MIN, 'max': self.MAX})

    def __call__(self, other):
        """Check if other value is in range (equivalent to "other in self").

        >>> Range(min=0.0, max=10)(5.0)
        True
        >>> Range(min=0.0, max=10.0)(-1.0)
        False

        :param other:
        :type other: int or float
        :return:
        """
        return isinstance(other, (int, float)) and other > self.data['min'] and other < self.data['max']

    @property
    def random(self):
        """Return a random float inside range.

        >>> r = Range(min=0, max=10)
        >>> random_value = r.random
        >>> isinstance(random_value, float)
        True
        >>> random_value in r
        True

        :return float: a random float inside range.
        """
        return random.uniform(self.data['min'], self.data['max'])

    @property
    def split(self):
        """Returns "min" and "max" values as tuple.

        >>> Range(min=1, max=10).split
        (1.0, 10.0)

        :return tuple: "min" and "max" values as tuple
        """
        return self.data['min'], self.data['max']

    def __contains__(self, item):
        """Check if item "float" is inside "Range" instance "min" and "max" attributes values.

        >>> 10.0 in Range(min=0.0, max=100.0)
        True
        >>> '10.0' in Range(min=1.0, max=15.0)
        True
        >>> 10 in Range(min='1.0', max='15')
        True
        >>> '-15' in Range(min=-10, max=10)
        False

        :param item: any float type convertible type instance with value to be checked.
        :type item: tp.SupportsFloat or str
        :return bool: True if item is inside range values, otherwise False
        """
        try:
            item = float(item)
            return self.data['min'] <= item <= self.data['max']
        except (ValueError, AttributeError) as err:
            print(str(err))
        return False

    def __getitem__(self, item):
        if isinstance(item, int) and item in [0, 1]:
            return self.data.get('min', self.MIN) if item == 0 else self.data.get('max', self.MAX)
        elif str(item) in ['min', 'max']:
            return self.data.get(item, 0.0)
        else:
            raise IndexError('{} not in index.'.format(str(item)))


class Limit(BaseDict):
    """Limits class with amount, price and cost attributes."""

    def __init__(self, **kwargs):
        """Initialize Limits class with amount, price and cost values.

        >>> amount = dict(min=0, max=100)
        >>> price = dict(min=10, max=1000)
        >>> cost = dict(min=0.0, max=10000)
        >>> Limit(amount=amount, price=price, cost=cost)
        Limit(amount: (min: 0.0, max: 100.0), price: (min: 10.0, max: 1000.0), cost: (min: 0.0, max: 10000.0))

        """
        kwargs = {k: Range(**{x: float(y or 0) or 0.0 for x, y in v.items()}) for k, v in kwargs.items()}
        super().__init__(**kwargs)
        self.amount.min = Range(**self.data.get('amount', Range(min=Range.MIN, max=Range.MAX)))
        self.price.min = Range(**self.data.get('price'))
        self.cost.max = Range(**self.data.get('cost'))

    def __getitem__(self, item):
        """Return min or max value by position value as int or str reference.

        >>> limits = Limit(amount=dict(min=0, max=100), price=dict(min=10, max=100), cost=dict(min=0, max=10))
        >>> str(limits[0])
        '(min: 0.0, max: 100.0)'
        >>> repr(limits['price'])
        'Range(min: 10.0, max: 100.0)'
        >>> limits[10]
        Traceback (most recent call last):
         ...
        IndexError: 10 not in index.

        :param item:
        :return: min or max value desired value.
        :raise: IndexError
        """
        # self.amount, self.price, self.cost = Range(), Range(), Range()

        if isinstance(item, int) and item in [0, 2]:
            return self.to_list[item]
        elif str(item) in self.fields:
            return self.to_dict[item]
        else:
            raise IndexError('{} not in index.'.format(str(item)))


class Precision(BaseDict):
    """Market precision class.

    >>> Precision()
    Precision(amount: 8, price: 8, cost: 8, base: 8, quote: 8)
    >>> Precision(amount=5, price=5, base=5, quote=3)
    Precision(amount: 5, price: 5, cost: 8, base: 5, quote: 3)
    >>> Precision(**dict(amount=3, price=10))
    Precision(amount: 3, price: 10, cost: 8, base: 8, quote: 8)

    """

    def __init__(self, **kwargs):
        """Precision constructor.

        :param kwargs:
            - param int base:   base currency precision.
            - param int quote:  quote currency precision.
            - param int amount: amount precision.
            - param int price:  price precision.
            - param int cost:   cost precision.
        """
        fields = ['amount', 'price', 'cost', 'base', 'quote']
        initial_data = {field: 8 if field not in kwargs else kwargs[field] for field in fields}
        super().__init__(**initial_data)
