import numpy as np


def fix_int64(data):
    return (data if not isinstance(data, np.int64) else int(data))


def untuple(list_of_tuples, index=0):
    for t in list_of_tuples:
        yield t[index]