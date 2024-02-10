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
