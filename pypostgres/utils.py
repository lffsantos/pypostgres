#!/usr/bin/env python3
from collections import namedtuple, Iterable
from psycopg2 import extras


def is_nested(values):
    '''Check if values is composed only by iterable elements.'''
    return (all(isinstance(item, list) or isinstance(item, tuple) for item in values)
            if isinstance(values, Iterable) else False)


def get_cursor_factory(factory):
    if factory is None:
        return
    elif factory.lower() in ('namedtuple',
                             'namedtuplecursor',
                             namedtuple,
                             extras.NamedTupleCursor):
        return extras.NamedTupleCursor
    elif factory.lower() in ('dict',
                             'dictcursor',
                             'realdict',
                             'realdictcursor',
                             dict,
                             extras.RealDictCursor):
        return extras.RealDictCursor
    return TypeError('Unknown factory: %s' % factory)
