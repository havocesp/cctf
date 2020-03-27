import abc
from collections import UserDict
from decimal import Decimal
from typing import (List, Tuple, Any, Dict, NoReturn, ItemsView, KeysView,
                    ValuesView, Text, Type, TypeVar)

K = KeysView
V = ValuesView
KV = ItemsView
Int = int
Float = float

Num = TypeVar['Num', Int, Float, Decimal]
Bool = Type[bool]
NumExt = TypeVar('NumExt', Num, Text)


class Meta(abc.ABCMeta): ...


class BaseDict(UserDict):

    @property
    def fields(self) -> List:
        ...

    def values(self) -> List:
        ...

    def keys(self) -> List: ...

    @property
    def to_list(self) -> List:
        ...

    @property
    def to_tuple(self) -> Tuple:
        ...

    @property
    def to_dict(self) -> Dict: ...

    def __repr__(self) -> Text:
        ...

    def __str__(self) -> Text:
        ...

    def __getattr__(self, item: Text) -> Text:
        ...


class Range(BaseDict):
    MIN: Float
    MAX: Float

    def __init__(self, **kwargs: Int) -> NoReturn:
        super().__init__(**kwargs)
        ...

    def __call__(self, other) -> Bool:
        ...

    def random(self) -> Float:
        ...

    @property
    def split(self) -> Tuple:
        ...

    def __contains__(self, item: Any) -> Bool: ...

    def __getitem__(self, item: NumExt) -> Any: ...


class Limit(BaseDict):
    def __init__(self, **kwargs: Dict) -> NoReturn:
        super().__init__(**kwargs)
        ...

    def __getitem__(self, item) -> Float: ...


class Precision(BaseDict):
    def __init__(self, **kwargs: Int) -> NoReturn:
        super().__init__(**kwargs)
        ...

    def __getattr__(self, item: Text) -> Int: ...
