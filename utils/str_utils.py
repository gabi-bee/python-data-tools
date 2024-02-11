import re


def flag_leading_zeros(x: str):
    """return flag: 1 if leading 0s, 0 otherwise"""
    if re.match('^0[0-9]+', x):
        return 1
    else:
        return 0
