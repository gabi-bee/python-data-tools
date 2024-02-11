import re
from collections.abc import Callable

import numpy as np
import pandas as pd

from utils.df_utils import get_dtype_cols_dict, update_with_expected_cols

# columns expected in final results
expected_columns: dict[str, type] = {  # TODO update
    'dtype_py_inferred': object,
    'int_leading_zeros': int,
    'str_len_min': int,
    'str_len_max': int,
    'float_max_dps': int,
    'numeric_checksum': float,
    'numeric_max': int,
}


# main functions -------------------------------------------------------------------------------------------------------
def run_suite_of_df_col_checks(df_inferred: pd.DataFrame, df_str: pd.DataFrame, describe: bool = False) -> pd.DataFrame:
    """
    runs checks on df - return df of check results
    :param df_inferred: python inferred dtype df
    :param df_str: str forced dtype df
    :param describe: True if describe fn checks to be run
    :return: dataframe containing results from checks
    """
    global expected_columns
    results: list[pd.DataFrame | pd.Series] = []

    # define checks to run for each col dtype
    dtype_checks_dict: dict[str, list[Callable]] = {  # TODO update
        'object': [check_str_len_min_max_checksum],
        'int64': [check_int_leading_zeros],
        'float64': [],
    }

    # run checks on all cols
    all_col_checks_df_inferred: list[Callable] = [check_all_dtypes]
    if describe:
        all_col_checks_df_inferred.append(lambda x: [x.describe(include='all').transpose()])
        expected_columns = expected_columns | {'max': float, 'min': float}  # TODO update with missing
    results += run_checks_on_cols(df_inferred, *all_col_checks_df_inferred, all_columns=True)

    # TODO run checks on numeric cols

    # run checks for each dtype cols (python inferred)
    dtypes_dict: dict[str, list[str]] = get_dtype_cols_dict(df_inferred, expected_keys=list(dtype_checks_dict.keys()))
    for dtype, dtype_checks in dtype_checks_dict.items():
        results += run_checks_on_cols(df_str, *dtype_checks, columns=dtypes_dict[dtype])

    # TODO re-run checks for each dtype cols (logic inferred)
    # TODO run checks on final col

    # prepare results df
    df_results = pd.concat(results, axis=1)  # concatenate results into df
    df_results = update_with_expected_cols(df_results, list(expected_columns.keys()))

    return df_results


# helper functions -----------------------------------------------------------------------------------------------------
def run_checks_on_cols(df: pd.DataFrame, *checks: Callable[[pd.DataFrame], list[pd.Series | pd.DataFrame]],
                       columns: list[str] = None, all_columns: bool = False) -> list[pd.Series | pd.DataFrame]:
    """

    :param df:
    :param checks:
    :param columns:
    :param all_columns:
    :return:
    """
    results = []

    if columns:
        df_to_check = df[columns]
        if all_columns:
            print('warning: all_columns = True AND columns passed as args. checks will be run on just columns passed')
    elif all_columns:
        df_to_check = df
    else:
        df_to_check = None
        print("warning: neither all_columns nor columns specified - therefore, checks aren't being run")

    if columns or all_columns:
        results = [result for check in checks for result in check(df_to_check)]

    return results


# util functions -------------------------------------------------------------------------------------------------------
def match_leading_zeros(x: str):
    """return flag: 0 if no leading 0s, 1 if leading 0s, na if na"""
    if pd.isna(x):
        return np.nan
    elif re.match('^0[0-9]+', x):
        return 1
    else:
        return 0


def get_str_len(x: str):
    """get len of string x, return x if na"""
    if pd.isna(x):
        return np.nan
    else:
        return len(x)


# individual check functions -------------------------------------------------------------------------------------------
def check_all_dtypes(df_inferred: pd.DataFrame) -> list[pd.Series]:
    """get col dtypes (python inferred)"""
    dtypes = df_inferred.dtypes
    dtypes.name = 'dtype_py_inferred'
    return [dtypes]


def check_int_leading_zeros(df_str: pd.DataFrame) -> list[pd.Series]:
    """get col count of values with leading 0s"""
    int_leading_zeros = df_str.map(match_leading_zeros).sum()
    int_leading_zeros.name = 'int_leading_zeros'
    return [int_leading_zeros]


def check_str_len_min_max_checksum(df_str: pd.DataFrame) -> list[pd.Series]:
    """get col min string length, max string length and checksum of string lengths"""
    df_lens = df_str.map(get_str_len)

    str_len_min = df_lens.min()
    str_len_min.name = 'str_len_min'

    str_len_max = df_lens.max()
    str_len_max.name = 'str_len_max'

    str_len_checksum = df_lens.sum()
    str_len_checksum.name = 'str_len_checksum'

    return [str_len_min, str_len_max, str_len_checksum]


def check_float_max_dps(df_str: pd.DataFrame) -> list[pd.Series]:
    pass  # TODO


def check_numeric_checksum(df_inferred: pd.DataFrame) -> list[pd.Series]:
    pass  # TODO


def check_numeric_max(df_inferred: pd.DataFrame) -> list[pd.Series]:
    pass  # TODO
