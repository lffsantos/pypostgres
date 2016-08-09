#!/usr/bin/env python3
#
#   PyPostgres
#   Marcellus Amadeus
#

# stdlib
from collections import namedtuple


Result = namedtuple('Result', ['success', 'response'])
Error = namedtuple('Error', ['exception', 'name'])
