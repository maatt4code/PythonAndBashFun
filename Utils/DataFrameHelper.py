import pandas as pd
from Utils import Log


def get_rows_by_numerid_index(df, id) -> pd.DataFrame:
    """
    Get rows from df using numeric indices (iloc)
    :param df: dataframe
    :param id: numeric row indices
    :return: rows with these numeric indices
    """
    assert df is not None and type(df) is pd.DataFrame
    assert type(id) is int
    if id >= len(df):
        raise TypeError("Id [%d] is too large or df" % id)
    return df.iloc[id]


def get_rows_by_key_index(df, id) -> pd.DataFrame:
    """
    Get row from df using (user-defined) index (column) (loc)
    :param df: dataframe
    :param id: user-defined indices from index column
    :return: rows with indices correspond to user-provided values
    """
    assert df is not None and type(df) is pd.DataFrame
    return df.loc[id]


def get_columns_by_names(df, cols) -> pd.DataFrame:
    """
    Get columns from df using column names ([ name ])
    :param df: dataframe
    :param id: column names
    :return: columns with these column names
    """
    assert df is not None and type(df) is pd.DataFrame
    return df[cols]


def filter_columns_by_null(df, col, include=False) -> pd.DataFrame:
    """
    filter dataframe by columns with null values
    :param df: dataframe
    :param col: columns to apply filter on
    :param include: whether to keep or throw away null entries
    :return: filtered dataframe
    """
    assert df is not None and type(df) is pd.DataFrame

    # dynamically select which function to call
    fn = ['notnull', 'isnull'][include]

    if type(col) is not list:
        col = [col]

    # init idx to all row
    idx = pd.Series([True] * len(df))
    for c in col:
        # intersect indices
        idx = idx & getattr(df[c], fn)()
    return df[idx]


def filter_columns_by_value(df, col, v_start, v_end, include=False) -> pd.DataFrame:
    """
    filter dataframe by columns using start and end values
    :param df: dataframe
    :param col: columns to apply filter on
    :param v_start: start values of these columns
    :param v_end: end values of these columns
    :param include: whether to keep or throw away entries satisfying filter
    :return: filtered dataframe
    """
    assert df is not None and type(df) is pd.DataFrame
    assert (type(col) is str and type(v_start) is not list and type(v_end) is not list)\
           or\
           (type(col) is list and len(v_start) == len(col) and len(v_end) == len(col))

    if type(col) is not list:
        col = [col]
        v_start = [v_start]
        v_end = [v_end]

    # init idx to all row
    idx = pd.Series([True] * len(df))
    for (c, s, e) in zip(col, v_start, v_end):
        if include:
            i_s = df[c] >= s
            i_e = df[c] <= e
            # intersect
            i = i_s & i_e
        else:
            i_s = df[c] < s
            i_e = df[c] > e
            # union
            i = i_s | i_e
        # intersect indices
        idx = idx & i
    return df[idx]


def check_column_is_in_dataframes(dfs, col_name) -> bool:
    """
    check whether all given columns are in all given dataframes
    :param dfs: dataframes
    :param col_name: column names to look for
    :return: True is all columns are found in all dataframes; false otherwise
    """
    if type(dfs) is not list:
        dfs = [dfs]

    if type(col_name) is not list:
        col_name = [col_name]

    # check col_name is a column
    for df in dfs:
        in_cols = set(col_name)
        df_cols = set(df.columns)
        # we only care all given column names are in DF ... ...
        diffs = in_cols - df_cols
        if diffs is not None and len(diffs) != 0:
            for c in diffs:
                Log.err("Col [%s] in List but not in DF" % c)
            return False
    return True


def check_indices_are_the_same(dfs, idx_name=None) -> bool:
    """
    check whether index column in all dataframes have the same values (ie same indices exist in all)
    :param dfs: dataframes
    :param idx_name: name of index column
    :return: True if same indices exist in all dataframes; false otherwise
    """
    # you only gave me 1 dataframe...
    if type(dfs) is not list:
        return True

    assert type(dfs[0]) is pd.DataFrame

    if idx_name is None:
        # check indices
        base = dfs[0].index
        for df in dfs:
            if not df.index.equals(base):
                return False
        return True
    else:
        # check idx_name is a column
        if check_column_is_in_dataframes(dfs, idx_name) is False:
            return False
        # check indices
        base = dfs[0][idx_name]
        for df in dfs:
            if not df[idx_name].equals(base):
                return False
        return True


def get_test_dataframe() -> pd.DataFrame:
    """
    get a test dataframe with timestamps, numbers, strings and nulls
    :return: test dataframe
    """
    # create dummy dataframe
    data = {
        'TimeStamp': ['2020/10/01 00:00:00.000', '2020/10/01 00:00:00.005', '2020/10/01 00:00:00.010', '2020/10/01 00:00:00.015', '2020/10/01 00:00:00.020', '2020/10/01 00:00:00.025', '2020/10/01 00:00:00.030', '2020/10/01 00:00:00.035', '2020/10/01 00:00:00.040', '2020/10/01 00:00:00.045', '2020/10/01 00:00:00.050', '2020/10/01 00:00:00.055', '2020/10/01 00:00:00.060', '2020/10/01 00:00:00.065', '2020/10/01 00:00:00.070', '2020/10/01 00:00:00.075', '2020/10/01 00:00:00.080', '2020/10/01 00:00:00.085', '2020/10/01 00:00:00.090', '2020/10/01 00:00:00.095', '2020/10/01 00:00:00.100', '2020/10/01 00:00:00.105', '2020/10/01 00:00:00.110', '2020/10/01 00:00:00.115', '2020/10/01 00:00:00.120', '2020/10/01 00:00:00.125', '2020/10/01 00:00:00.130', '2020/10/01 00:00:00.135', '2020/10/01 00:00:00.140', '2020/10/01 00:00:02.145'],
        'ID': [None, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 125, 130, 135, 140, 145, 150],
        'Value': [128, 695, 490, 283, None, 11, 404, 28, 842, 373, 758, None, 107, 98, 475, None, 822, 919, 628, 103, 230, None, 431, 689, 362, 971, 258, 962, None, 613],
        'Msg': ['h', 'P', 'M', 'n', 'W', ']', 'd', 'K', 'Z', 'Y', 'Z', 'b', 'A', 'G', 'd', '\\', 'I', 'P', 'd', 'j', 'A', 'H', ']', 'v', 'L', '_', 'E', 'B', 'X', '[']
    }

    # turn it into dataframe
    df = pd.DataFrame(data=data)
    return df


def main():
    df = get_test_dataframe()
    Log.info(df)

    #
    Log.info("get_rows_by_key_index : %s" % get_rows_by_key_index(df, 5));
    Log.info("get_columns_by_names : %s" % get_columns_by_names(df, 'ID'));
    Log.info("get_columns_by_names : %s" % get_columns_by_names(df, ['ID', 'Value']));
    Log.info("filter_columns_by_null : %s" % filter_columns_by_null(df, 'ID'));
    Log.info("filter_columns_by_null : %s" % filter_columns_by_null(df, ['ID', 'Value']));
    Log.info("filter_columns_by_null : %s" % filter_columns_by_null(df, 'Value', include=True));
    Log.info("filter_columns_by_value : %s" % filter_columns_by_value(df, 'Value', 100, 300, include=True));
    Log.info("filter_columns_by_value : %s" % filter_columns_by_value(df, ['ID', 'Value'], [50, 100], [100, 500], include=True));
    Log.info("filter_columns_by_value : %s" % filter_columns_by_value(df, ['ID', 'Value'], [50, 100], [100, 500], include=False));

    df2 = df.copy()
    df2.rename(columns={'TimeStamp': 'Timestamp'})
    Log.info("check_indices_are_the_same : %s" % check_indices_are_the_same([df, df2]));
    Log.info("check_indices_are_the_same : %s" % check_indices_are_the_same([df, df2], 'TimeStamp'));

    df = df.set_index('TimeStamp')
    Log.info(get_rows_by_key_index(df, '2020/10/01 00:00:00.040'))


if __name__ == '__main__':
    main()