# -*- coding: utf-8 -*-
"""pandaxt
  orders module.
 
  - Author:     
  - License:    
  - Created:    13-11-2018
  - Modified:   13-11-2018
"""
from collections import UserDict


# noinspection PyUnusedFunction,PyUnusedFunction,PyUnusedFunction,PyUnusedFunction
class Order(UserDict):
    """ Order model class to serve as order data container.

    >>> Order(price=0.0543).price
    0.0543

    """
    PRICE = 'price'
    AMOUNT = 'amount'
    BUY = 'buy'
    SELL = 'sell'
    LIMIT = 'limit'
    MARKET = 'market'
    STATUS = 'status'
    CANCEL = 'cancel'

    # noinspection PyUnusedFunction
    class Status:
        NEW = 'new'
        CLOSED = 'closed'
        PENDING = 'pending'
        CANCELED = 'cancel'

        @classmethod
        def fields(cls):
            return [cls.NEW, cls.CLOSED, cls.PENDING, cls.CANCELED]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.price = kwargs.get(self.PRICE)
        # self.amount = kwargs.get(self.STATUS)
        # self.buy = kwargs.get(self.BUY)
        # self.sell = kwargs.get(self.SELL)
        # self.limit = kwargs.get(self.LIMIT)
        # self.market = kwargs.get(self.MARKET)
        # self.status = kwargs.get(self.STATUS)
        # self.cancel = kwargs.get(self.CANCEL)

    def __getattr__(self, item):
        return self.data.get(item) if item not in 'data' else self.data

    @classmethod
    def is_new(cls):
        return cls.status == cls.NEW

    @classmethod
    def is_completed(cls):
        return cls.STATUS == cls.CLOSED

    @classmethod
    def is_active(cls):
        return cls.STATUS == cls.PENDING

    @classmethod
    def is_removed(cls):
        return cls.STATUS == cls.CANCELED


# noinspection PyUnusedFunction,PyUnusedFunction,PyUnusedFunction
class Side:
    BUY = 'buy'
    SELL = 'sell'

    def is_buy(self):
        return self == Side.BUY

    def is_sell(self):
        return self == Side.SELL

    def reverse(self):
        if self == Side.BUY:
            return Side.SELL
        return Side.BUY


class TradeFields:
    AMOUNT = 'amount'
    COST = 'cost'
    DATETIME = 'datetime'
    FEE = 'fee'
    PRICE = 'price'
    SIDE = 'side'
    SYMBOL = 'symbol'
    TIMESTAMP = 'timestamp'


class OHLC:
    DATE = 'date'
    OPEN = 'open'
    HIGH = 'high'
    LOW = 'low'
    CLOSE = 'close'
    VOLUME = 'volume'
    QVOLUME = 'quotevolume'
