import numpy as np


def fix_int64(data):
    return (data if not isinstance(data, np.int64) else int(data))