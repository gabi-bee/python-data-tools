import numpy as np
import pandas as pd


def get_dtype_cols_dict(df: pd.DataFrame, expected_keys: list[str] = None) -> dict[str, list[str]]:
    """
    gets dictionary of dtype: cols
    :param df: dataframe
    :param expected_keys: list of expected keys in output - it will add these if not present in result
    :return: dictionary with
        key: str(dtype) of columns
        value: list of column names
    """
    dtypes: pd.Series = df.dtypes.map(lambda x: x.name)  # get inferred dtypes
    grouped = dtypes.groupby(dtypes).groups
    grouped = {str(key): value.tolist() for key, value in grouped.items()}

    if expected_keys:
        for key in expected_keys:
            if key not in grouped:
                grouped[key] = []

    return grouped


def reshape_with_expected_cols(df: pd.DataFrame, expected_cols: list[str] = None,
                               reshape: bool = True, drop_unexpected: bool = False) -> pd.DataFrame:
    """
    # TODO
    :param df:
    :param expected_cols:
    :param reshape:
    :param drop_unexpected:
    :return:
    """
    orig_cols = df.columns.tolist()

    # add missing cols
    for col in expected_cols:
        if col not in orig_cols:
            df[col] = np.nan
    new_cols = df.columns.tolist()

    # get unexpected cols
    unexpected_cols = [col for col in orig_cols if col not in expected_cols]
    if unexpected_cols:
        print(f'warning: unexpected cols present in df: {",".join(unexpected_cols)}')
        if drop_unexpected:
            print('warning: dropped unexpected cols')

    # reshape and drop as per params
    if reshape:
        if drop_unexpected:
            df_new = df[expected_cols]
        else:
            df_new = df[expected_cols + unexpected_cols]
    else:
        if drop_unexpected:
            df_new = df[[col for col in new_cols if col in expected_cols]]
        else:
            df_new = df

    return df_new
