# -*- coding: utf-8 -*-
"""
 CCTF
 - Author:      Daniel J. Umpierrez
 - Created:     08-10-20018
 - License:     MIT
"""
import collections as col
import typing as tp


def flt(value, p=None, as_str=False):
    """
    Float builtin wrapper for precision param initialization.

    :param bool as_str: return as string
    :param value:
    :type value: Number or str
    :param int p:
    :return:
    :rtype: str or Number
    """

    value_str = str(value or '0.0').strip()

    if '.' in value_str:
        template = '{{:.{:d}f}}'.format(p or infer_precision(value))
        value = template.format(float(value_str)).rstrip('.0')
        backup = str(value)
        try:
            value = value if as_str else float(value)
        except ValueError:
            value = backup
        return value
    elif value_str.lstrip('-+').rstrip('.').isnumeric():
        return int(value)
    else:
        return value


def infer_precision(number):
    """

    :param float number:
    :return int:
    """
    number = number or 0.0
    try:
        number = float(number)
    except ValueError:
        return number
    if number is not None and isinstance(number, float):
        if number < 0.000001:
            return 10
        elif number < 0.0001:
            return 8
        elif number < 0.01:
            return 5
        elif number < 1.0:
            return 3
        elif number < 100:
            return 2
        elif number < 1000:
            return 1
        else:
            return 0


def num2str(n, precision=8):
    """
    Numeric type infer and parser

    Accept any Iterable (dict, list, tuple, set, ...) or built-in data types int, float, str, ... and try  to
    convert it a number data type (int, float)
    :param n:
    :type n: Number or tp.Iterable
    :param int precision:
    :return tp.Iterable:
    """
    if n is not None:
        if isinstance(n, str):
            backup = type(n)(n)
            try:
                n = flt(n, precision, as_str=True)
            except ValueError:
                n = backup
        elif isinstance(n, str):
            n = flt(n, precision, as_str=True)
        elif isinstance(n, col.Mapping):
            n = {k: num2str(v, precision) if isinstance(v, col.Iterable) else v for k, v in dict(n).items()}
        elif isinstance(n, col.Iterable):
            n = [num2str(n, precision) if isinstance(n, col.Iterable) else n for n in list(n)]
    return n
