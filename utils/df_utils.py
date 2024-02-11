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
    # create dict {dtype: cols} for cols in df
    dtypes: pd.Series = df.dtypes.map(lambda x: x.name)  # get inferred dtypes
    dtype_cols_dict = {str(key): value.tolist() for key, value in dtypes.groupby(dtypes).groups.items()}

    if expected_keys:
        # add expected keys to dict if not present
        dtype_cols_dict = dtype_cols_dict | {key: [] for key in expected_keys if key not in dtype_cols_dict}

    return dtype_cols_dict


def update_with_expected_cols(df: pd.DataFrame, expected_cols: list[str] = None,
                              reshape: bool = True, drop_unexpected: bool = False) -> pd.DataFrame:
    """
    update df:
        - add missing expected_columns
        - reorder columns if reshape = True
        - drop unexpected columns in drop_unexpected = True
    :param df: dataframe
    :param expected_cols: list of expected column names
    :param reshape: True if reordering cols as per expected_cols order
    :param drop_unexpected: True if dropping unexpected columns
    :return: reshaped dataframe
    """
    orig_cols = df.columns.tolist()

    # add missing cols
    for col in expected_cols:
        if col not in orig_cols:
            df[col] = np.nan
    updated_cols = df.columns.tolist()

    # get unexpected cols
    unexpected_cols = [col for col in orig_cols if col not in expected_cols]
    if unexpected_cols:
        print(f'warning: unexpected cols present in df: {",".join(unexpected_cols)}')
        if drop_unexpected:
            print('warning: dropped unexpected cols')

    # reshape and drop as per params
    if reshape:
        if drop_unexpected:
            df_updated = df[expected_cols]
        else:
            df_updated = df[expected_cols + unexpected_cols]  # unexpected_cols will be moved to end of df
    else:
        if drop_unexpected:
            df_updated = df[[col for col in updated_cols if col in expected_cols]]
        else:
            df_updated = df

    return df_updated
