import numpy as np


def fix_int64(data):
    return (data if not isinstance(data, np.int64) else int(data))


def untuple(list_of_tuples, index=0):
    result = []
    for t in list_of_tuples:
        result.append(t[index])
    return result