#!/usr/bin/env python3
from collections import namedtuple
from psycopg2 import extras


def is_nested(values):
    '''Check whether given values contain nested elements.'''
    flat_types = (str, int, bool, float)
    return not all(any(isinstance(el, t) for t in flat_types) for el in values)


def get_cursor_factory(factory):
    if factory in ['NamedTuple', 'NamedTupleCursor', namedtuple, extras.NamedTupleCursor]:
        return extras.NamedTupleCursor
    elif factory in ['Dict', 'DictCursor', dict, extras.DictCursor]:
        return extras.DictCursor
    elif factory in ['RealDict', 'RealDictCursor', extras.RealDictCursor]:
        return extras.RealDictCursor
