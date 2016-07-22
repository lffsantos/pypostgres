#!/usr/bin/env python3
#
#   PyPostgres
#   Marcellus Amadeus
#

# stdlib
from collections import namedtuple


Result = namedtuple('Result', ['success', 'response'])
Error = namedtuple('Error', ['exception', 'name'])


def is_nested(values):
    '''Check whether given values have lists of lists (or tuples of tuples)'''
    return all([(isinstance(el, list) or isinstance(el, tuple)) for el in values])
