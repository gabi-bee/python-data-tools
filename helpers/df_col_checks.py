from collections.abc import Callable

import numpy as np
import pandas as pd

from utils.df_utils import get_dtype_cols_dict, update_with_expected_cols
from utils.float_utils import flag_outlier
from utils.str_utils import flag_leading_zeros, count_chars_after_point

# columns expected in final results
expected_columns: dict[str, type] = {  # TODO update
    'dtype_py_inferred': object,
    'int_leading_zeros': int,
    'str_len_min': int,
    'str_len_max': int,
    'float_max_dps': int,
    'num_checksum': float,
    'num_max': float,
    'num_min': float,
    'num_mean': float,
    'num_std': float,
    'num_count_outliers': int,
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

    # run checks on all cols
    all_col_checks_df_inferred: list[Callable] = [check_all_dtypes]
    if describe:
        all_col_checks_df_inferred.append(lambda x: [x.describe(include='all').transpose()])
        expected_columns = expected_columns | {'max': float, 'min': float}  # TODO update with missing
    results += run_checks_on_cols(df_inferred, *all_col_checks_df_inferred, all_columns=True)

    # define checks to run for each col dtype
    dtype_checks_dict: dict[str, list[Callable]] = {  # TODO update
        'object': [check_str_len_min_max_checksum],
        'int64': [check_int_leading_zeros],
        'float64': [check_float_max_dps],
    }

    # get dict of dtypes and associated columns
    dtypes_dict: dict[str, list[str]] = get_dtype_cols_dict(df_inferred, expected_keys=list(dtype_checks_dict.keys()))

    # run checks on numeric cols
    numeric_col_checks: list[Callable] = [  # TODO update
        check_num_checksum,
        check_num_max,
        check_num_min,
        check_num_mean
    ]
    numeric_cols = dtypes_dict['int64'] + dtypes_dict['float64']
    results += run_checks_on_cols(df_inferred, *numeric_col_checks, columns=numeric_cols)

    # run checks for each dtype cols (python inferred)
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
    # TODO update Docstring and add test
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


def gen_map_handle_missing_vals(df: pd.DataFrame | pd.Series,
                                map_fn: Callable, **map_fn_kwargs) -> pd.DataFrame | pd.Series:
    """apply mapping function and handle null values"""
    map_result = df.map(lambda x: map_fn(x, **map_fn_kwargs) if not pd.isna(x) else np.nan)
    return map_result


def gen_aggregate_map(map_result: pd.DataFrame | pd.Series, agg_fn: str, name: str) -> pd.Series:
    result = None

    if agg_fn == 'sum':
        result = map_result.sum()
    elif agg_fn == 'max':
        result = map_result.max()
    elif agg_fn == 'min':
        result = map_result.min()
    elif agg_fn == 'mean':
        result = map_result.mean()
    elif agg_fn == 'std':
        result = map_result.std()
    else:
        # TODO throw error
        pass

    if type(result) == pd.Series:
        result.name = name
    return result


def check_generic(df: pd.DataFrame | pd.Series, name: str,
                  map_fn: Callable, agg_fn: str, **map_fn_kwargs) -> list[pd.Series]:
    """get check results"""
    map_result = gen_map_handle_missing_vals(df, map_fn, **map_fn_kwargs)
    agg_result = gen_aggregate_map(map_result, agg_fn, name)
    return [agg_result]


# individual check functions -------------------------------------------------------------------------------------------
def check_all_dtypes(df_inferred: pd.DataFrame) -> list[pd.Series]:
    """get col dtypes (python inferred)"""
    dtypes = df_inferred.dtypes.map(lambda x: x.name)
    dtypes.name = 'dtype_py_inferred'
    return [dtypes]


def check_int_leading_zeros(df_str: pd.DataFrame) -> list[pd.Series]:
    """get col count of values with leading 0s"""
    return check_generic(df_str, 'int_leading_zeros', flag_leading_zeros, agg_fn='sum')


def check_str_len_min_max_checksum(df_str: pd.DataFrame) -> list[pd.Series]:
    """get col min string length, max string length and checksum of string lengths"""
    df_lens = gen_map_handle_missing_vals(df_str, len)
    str_len_min = gen_aggregate_map(df_lens, 'min', 'str_len_min')
    str_len_max = gen_aggregate_map(df_lens, 'max', 'str_len_max')
    str_len_checksum = gen_aggregate_map(df_lens, 'sum', 'str_len_checksum')

    return [str_len_min, str_len_max, str_len_checksum]


def check_float_max_dps(df_str: pd.DataFrame) -> list[pd.Series]:
    """get col max decimal places"""
    return check_generic(df_str, 'float_max_dps', count_chars_after_point, agg_fn='max')


def check_num_checksum(df_inferred: pd.DataFrame) -> list[pd.Series]:
    """get col sum"""
    return check_generic(df_inferred, 'num_checksum', lambda x: x, agg_fn='sum')


def check_num_max(df_inferred: pd.DataFrame) -> list[pd.Series]:
    """get col max"""
    return check_generic(df_inferred, 'num_max', lambda x: x, agg_fn='max')


def check_num_min(df_inferred: pd.DataFrame) -> list[pd.Series]:
    """get col min"""
    return check_generic(df_inferred, 'num_min', lambda x: x, agg_fn='min')


def check_num_mean(df_inferred: pd.DataFrame) -> list[pd.Series]:
    """get col mean"""
    return check_generic(df_inferred, 'num_mean', lambda x: x, agg_fn='mean')


def check_num_std(df_inferred: pd.DataFrame) -> list[pd.Series]:
    """get col standard deviation"""
    return check_generic(df_inferred, 'num_std', lambda x: x, agg_fn='std')


def check_num_count_outliers(df_inferred: pd.DataFrame) -> list[pd.Series]:
    """get col outlier count"""
    [num_mean] = check_num_mean(df_inferred)
    [num_std] = check_num_std(df_inferred)

    results = {}
    for col in df_inferred.columns:
        mean = num_mean.loc[col]
        std = num_std.loc[col]
        [col_result] = check_generic(df_inferred[col], 'num_count_outliers', flag_outlier, agg_fn='sum', mean=mean,
                                     std=std)
        results[col] = col_result
    num_count_outliers = pd.Series(data=results)
    num_count_outliers.name = 'num_count_outliers'
    return [num_count_outliers]
