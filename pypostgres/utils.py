#!/usr/bin/env python3
#
#   PyPostgres
#   Marcellus Amadeus
#

# stdlib
from collections import namedtuple

# third-party
import numpy as np


Result = namedtuple('Result', ['success', 'response'])
Error = namedtuple('Error', ['exception', 'name'])


def fix_int64(value):
    '''Replace numpy.int64 value for Python default int.'''
    return value if not isinstance(value, np.int64) else int(value)


def is_nested(values):
    '''Check whether given values have lists of lists (or tuples of tuples)'''
    return all([(isinstance(el, list) or isinstance(el, tuple)) for el in values])
