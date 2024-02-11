def flag_outlier(x: float, mean: float, std: float):
    """return flag 1 if x is an outlier (outside 3 std from mean)"""
    if x == mean:
        return 0
    elif x > mean:
        if x > mean + 3 * std:
            return 1
        else:
            return 0
    elif x < mean:
        if x < mean - 3 * std:
            return 1
        else:
            return 0
