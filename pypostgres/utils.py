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
    '''Check whether given values contain nested elements.'''
    flat_types = (str, int, bool, float)
    return not all(any(isinstance(el, t) for t in flat_types) for el in values)
