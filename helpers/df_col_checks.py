import re
from collections.abc import Callable

import numpy as np
import pandas as pd

from utils.df_utils import get_dtype_cols_dict, reshape_with_expected_cols

# columns expected in final results
expected_columns: dict[str, type] = {  # TODO update
    'dtype_py_inferred': object,
    'int_leading_zeros': int,
    'str_len_min': int,
    'str_len_max': int,
    'str_len_checksum': int,
}


# main functions -------------------------------------------------------------------------------------------------------
def run_suite_of_df_col_checks(df_inferred: pd.DataFrame, df_str: pd.DataFrame) -> pd.DataFrame:
    """
    runs checks on
    :param df_inferred: python inferred dtype df
    :param df_str: str forced dtype df
    :return: dataframe containing results from checks
    """
    results: list[pd.DataFrame | pd.Series] = []

    # define checks to run for each col dtype
    dtype_checks_dict: dict[str, list[Callable]] = {  # TODO update
        'object': [check_str_len_min_max_checksum],
        'int64': [check_int_leading_zeros],
        'float64': [],
    }

    # run checks on all cols
    all_col_checks_df_inferred: list[Callable] = [check_all_dtypes, lambda x: [x.describe(include='all').transpose()]]
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
    df_results = reshape_with_expected_cols(df_results, list(expected_columns.keys()))

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
        for check in checks:
            check_result = check(df_to_check)  # run check(s)
            results += check_result

    return results


# util functions -------------------------------------------------------------------------------------------------------
def match_leading_zeros(x: str):
    if pd.isna(x):
        return np.nan
    elif re.match('^0[0-9]+', x):
        return 1
    else:
        return 0


def get_str_len(x: str):
    if pd.isna(x):
        return np.nan
    else:
        return len(x)


# individual check functions -------------------------------------------------------------------------------------------
def check_all_dtypes(df_inferred: pd.DataFrame) -> list[pd.Series]:
    dtypes = df_inferred.dtypes
    dtypes.name = 'dtype_py_inferred'
    return [dtypes]


def check_int_leading_zeros(df_str: pd.DataFrame) -> list[pd.Series]:
    int_leading_zeros = df_str.map(match_leading_zeros).sum()
    int_leading_zeros.name = 'int_leading_zeros'
    return [int_leading_zeros]


def check_str_len_min_max_checksum(df_str: pd.DataFrame) -> list[pd.Series]:
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
