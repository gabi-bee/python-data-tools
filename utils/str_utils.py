import re


def flag_leading_zeros(x: str):
    """return flag: 1 if leading 0s, 0 otherwise"""
    if re.match('^0[0-9]+', x):
        return 1
    else:
        return 0


def count_chars_after_point(x: str):
    """return count of characters after a '.' - can be used to get number of decimal places of number"""
    if '.' in x:
        return len(x.split('.')[1])
    else:
        return 0
