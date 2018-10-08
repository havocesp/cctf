# -*- coding: utf-8 -*-
"""
 CCTF
 - Author:      Daniel J. Umpierrez
 - Created:     07-10-2018
 - License:     MIT
"""
import collections as col
import random
import typing as tp

__all__ = ['Range', 'Precision', 'Limits']


class Range(col.UserDict):
    """
    Range class.
    """
    MAX = 10000000.0
    MIN = 0.0

    def __init__(self, **kwargs):
        """
        Init Range instance with min an max values.

        >>> Range(min=10, max=100)
        Range: 10.0, 100.0

        :param min: min range value.
        :type min:  tp.SupportsFloat or str
        :param tp.SupportsFloat or str max: max range value.
        :type max:  tp.SupportsFloat or str
        """
        self.min = Range.MIN
        self.max = Range.MAX

        if len(kwargs) == 1 and isinstance(list(kwargs.values())[0], col.Mapping):
            kwargs = dict(list(kwargs.values())[0])

        kwargs = dict(kwargs or dict(min=self.min, max=self.max))

        if 'min' not in kwargs:
            kwargs.update({'min': Range.MIN})

        if 'max' not in kwargs:
            kwargs.update({'max': Range.MAX})

        super().__init__(**kwargs)
        try:

            if isinstance(self.data, col.Mapping):
                self.min = float(self.data.get('min') or Range.MIN)
                self.max = float(self.data.get('max') or Range.MAX)

        except (ValueError, TypeError, AttributeError):
            self.min = Range.MIN
            self.max = Range.MAX

    def __call__(self, other):
        """
        Check if other value is in range (equivalent to "other in self").

        >>> Range(0, 10)(5)
        True
        >>> Range(0.0, 10.0)(-1.0)
        False

        :param other:
        :type other: str or tp.SupportsFloat or Range
        :return:
        """
        return other in self

    @property
    def random(self):
        """
        Return a random float inside range.

        >>> r = Range(0, 10)
        >>> random_value = r.random
        >>> isinstance(random_value, float)
        True
        >>> random_value in r
        True

        :return float: a random float inside range.
        """
        return random.uniform(self.min, self.max)

    @property
    def split(self):
        """
        Returns "min" and "max" values as tuple.

        >>> Range(1, 10).split
        (1.0, 10.0)

        :return tuple: "min" and "max" values as tuple
        """
        return self.min, self.max

    def __str__(self):
        """
        Return range values as string (min and max values separated by ", ")

        >>> str(Range(10.0, 1000.0))
        '10.0, 1000.0'

        :return str: min and max values separated by "-"
        """
        return '{}, {}'.format(self.min, self.max)

    def __repr__(self):
        """
        Return Range instance name followed by it values as string (min and max values separated by ", ")

        >>> Range(10.0, 1000.0)
        Range: 10.0, 1000.0

        :return:
        """
        return 'Range: {}'.format(self.__str__())

    def __contains__(self, item):
        """
        Check if item "float" is inside "Range" instance "min" and "max" attributes values.

        >>> 10.0 in Range(0.0, 100.0)
        True
        >>> '10.0' in Range(1.0, 15.0)
        True
        >>> 10 in Range('1.0', '15')
        True
        >>> '-15' in Range(-10, 10)
        False

        :param item: any float type convertible type instance with value to be checked.
        :type item: tp.SupportsFloat or str
        :return bool: True if item is inside range values, otherwise False
        """
        try:
            item = float(item)
            return self.min <= item <= self.max
        except (ValueError, AttributeError) as err:
            print(str(err))
            return False

    def __getitem__(self, item):
        """
        Return min or max value by position value as int or str reference.

        >>> Range(0, 100)[0]
        0.0
        >>> Range('0', '100')['max']
        100.0
        >>> Range(0, 100)[10]
        Traceback (most recent call last):
         ...
        IndexError: 10 not in index.

        :param item:
        :type item: int or str
        :return: min or max value desired value.
        :raise: IndexError
        """
        if isinstance(item, int) and item in [0, 1]:
            return self.min if item == 0 else self.max
        elif str(item) in ['min', 'max']:
            return getattr(self, item)
        else:
            raise IndexError('{} not in index.'.format(str(item)))

    def __reversed__(self):
        """
        Return a reverse instance of Range with max as min and vice versa.

        >>> reversed(Range(min=10, max=0))
        Range: 0.0, 10.0

        :return Range: a reverse instance of Range with max as min and vice versa.
        """
        return Range(max=self.max, min=self.min)

    @property
    def fields(self):
        """
        Return fields names as List[AnyStr] type.

        >>> Range().fields
        ['min', 'max']

        :return tp.List[tp.AnyStr]: fields names as List[AnyStr] type.:
        """
        return [k for k in self.__dict__.keys() if k[0] != '_']

    @property
    def to_list(self):
        """
        Return List[float] type containing Limits values.

        >>> Range(0, 10).to_list
        [0.0, 10.0]

        :return tp.List[float]: List[float] type containing Limits values.
        """
        return list(self.to_tuple)

    @property
    def to_tuple(self):
        """
        Return Tuple[float] type containing min and max values.

        >>> Range(0, 10).to_tuple
        (0.0, 10.0)

        :return tp.Tuple[float]: Tuple[float] type containing Limits values.
        """
        return self.min, self.max

    @property
    def to_dict(self):
        """
        Return a Dict[AntStr, float] type containing Limits values.

        >>> Range(0, 10).to_dict
        {'min': 0.0, 'max': 10.0}

        :return tp.Dict[tp.AnyStr, float]: Dict[AntStr, float] type containing Limits values.
        """
        return dict(zip(self.fields, self.to_list))


class Limits(col.UserDict):

    def __init__(self, **kwargs):
        """
        Initialize Limits class with amount, price and cost values.

        >>> amount = dict(min=0, max=100)
        >>> price = Range(10, 1000)
        >>> cost = dict(min=0.0, max=10000)
        >>> Limits(amount, price=price, cost=cost)
        [Limits](amount: 0.0, 100.0 - price: 10.0, 1000.0 - cost: 0.0, 10000.0)

        :param amount:
        :type amount: tp.Dict or Range
        :param price:
        :type price: tp.Dict or Range
        :param cost:
        :type cost: tp.Dict or Range
        """
        super().__init__(**kwargs)
        self.amount = Range(**self.data) if isinstance(self.data, col.Mapping) else Range()
        self.price = Range(**self.data) if isinstance(self.data, col.Mapping) else Range()
        self.cost = Range(**self.data) if isinstance(self.data, col.Mapping) else Range()

    @property
    def fields(self):
        """
        Return fields names as List[AnyStr] type.

        >>> Limits().fields
        ['amount', 'price', 'cost']

        :return tp.List[tp.AnyStr]: fields names as List[AnyStr] type.:
        """
        return [k for k in self.__dict__.keys() if k[0] != '_']

    @property
    def to_list(self):
        """
        Return List[Range] type containing Limits values.

        >>> Limits().to_list
        [Range: 0.0, 10000000.0, Range: 0.0, 10000000.0, Range: 0.0, 10000000.0]

        :return tp.List[Range]: List[Range] type containing Limits values.
        """
        return list(self.to_tuple)

    @property
    def to_tuple(self):
        """
        Return Tuple[Range] type containing Limits values.

        >>> Limits().to_tuple
        (Range: 0.0, 10000000.0, Range: 0.0, 10000000.0, Range: 0.0, 10000000.0)

        :return tp.Tuple[Range]: Tuple[Range] type containing Limits values.
        """
        return self.amount, self.price, self.cost

    @property
    def to_dict(self):
        """
        Return a Dict[AntStr, Range] type containing Limits values.

        >>> Limits().to_dict
        {'amount': Range: 0.0, 10000000.0, 'price': Range: 0.0, 10000000.0, 'cost': Range: 0.0, 10000000.0}

        :return tp.Dict[tp.AnyStr, Range]: Dict[AntStr, Range] type containing Limits values.
        """
        return dict(zip(self.fields, self.to_list))

    def __getitem__(self, item):
        """
        Return min or max value by position value as int or str reference.

        >>> limits = Limits(amount=Range(0, 100), price=Range(10, 100), cost=Range(0, 10))
        >>> limits[0]
        Range: 0.0, 100.0
        >>> limits['price']
        Range: 10.0, 100.0
        >>> limits[10]
        Traceback (most recent call last):
         ...
        IndexError: 10 not in index.

        :param item:
        :type item: int or str
        :return: min or max value desired value.
        :raise: IndexError
        """
        # self.amount, self.price, self.cost = Range(), Range(), Range()

        if isinstance(item, int) and item in [0, 2]:
            return self.to_list[item]
        elif str(item) in self.fields:
            return self.to_dict[str(item)]
        else:
            raise IndexError('{} not in index.'.format(str(item)))

    def __str__(self):
        """
        Return range values as string (min and max values separated by ", ")

        >>> str(Limits(amount=Range(0, 100), price=Range(10, 100), cost=Range(0, 10)))
        'amount: 0.0, 100.0 - price: 10.0, 100.0 - cost: 0.0, 10.0'

        :return str: min and max values separated by "-"
        """
        return 'amount: {} - price: {} - cost: {}'.format(str(self.amount), str(self.price), str(self.cost))

    def __repr__(self):
        """
        Return Range instance name followed by it values as string (min and max values separated by ", ")

        >>> Limits(amount=Range(0, 100), price=Range(10, 100), cost=Range(0, 10))
        [Limits](amount: 0.0, 100.0 - price: 10.0, 100.0 - cost: 0.0, 10.0)

        :return:
        """
        return '[Limits]({})'.format(self.__str__())


class Precision(col.UserDict):
    """
    Market precision class.

    >>> Precision()
    Precision(base=8, quote=8, amount=8, price=8)
    >>> Precision(amount=5, price=5, base=5, quote=3)
    Precision(base=5, quote=3, amount=5, price=5)
    >>> Precision(**dict(amount=8, price=10))
    Precision(base=8, quote=8, amount=8, price=10)

    """

    def __init__(self, **kwargs):
        """
        Precision constructor.

        :param int base: base currency precision.
        :param int quote: quote currency precision.
        :param int amount: amount precision.
        :param int price: price precision.
        :param int cost: cost precision.
        """
        super().__init__(**kwargs)
        self.base = self.data.get('base', 8)
        self.quote = self.data.get('quote', 8)
        self.amount = self.data.get('amount', 8)
        self.price = self.data.get('price', 8)

    # def __str__(self):
    #     template = 'Precision(base={base:d}, quote={quote:d}, amount={amount:d}, price={price:d})'
    #     return template.format(**self.__dict__)
    #
    # def __repr__(self):
    #     return self.__str__()
