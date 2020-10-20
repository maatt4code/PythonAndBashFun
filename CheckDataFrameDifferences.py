import os
import pandas as pd
from Utils import DataFrameHelper as DFH
from Utils import Log


def print_list_diffs(l1, l2):
    s1 = set(l1)
    s2 = set(l2)
    diff = s1 - s2
    if len(diff) != 0:
        print("Cols in 1 but not in 2 : %s" % diff)
    diff = s2 - s1
    if len(diff) != 0:
        print("Cols in 2 but not in 1 : %s" % diff)


def check_all_dfs_have_same_columns(dfs) -> bool:
    if type(dfs) is not list:
        return True
    cols = dfs[0].columns
    return DFH.check_column_is_in_dataframes(dfs, list(cols))


def check_values(dfs, threshold) -> bool:
    # column names and indices are assumed to be the same
    assert len(dfs) == 2

    cols = dfs[0].columns
    for c in cols:
        # if the column in the 2 dataframes do not equal
        if not dfs[0][c].equals(dfs[1][c]):
            # get indices of diff elements (True is different)
            # this returns T/F vs numeric indices {0, ..., n-1}
            diff = dfs[0][c] != dfs[1][c]

            # get rows that have different values for this column
            df1 = dfs[0][diff][c]
            df2 = dfs[1][diff][c]

            # check how different the values are
            for i in df1.index:
                elems = [df1.loc[i], df2.loc[i]]
                try:
                    # get values by index
                    vals = [float(e) for e in elems]
                    if abs(vals[0] - vals[1]) < threshold:
                        Log.warn("abs(%f - %f) = %f < %f" % (vals[0], vals[1], abs(vals[0] - vals[1]), threshold))
                        pass
                    else:
                        Log.err("abs(%f - %f) = %f >= %f" % (vals[0], vals[1], abs(vals[0] - vals[1]), threshold))
                except:
                    Log.err("%s != %s" % (elems[0], elems[1]))
            return False
    return True


def test_case():
    idx_name = 'TimeStamp'
    dir = os.path.join('Data')
    files = ['Dummy_1.csv', 'Dummy_2.csv']
    dfs = [pd.read_csv(os.path.join(dir, f)) for f in files]
    rets = [check_all_dfs_have_same_columns(dfs), DFH.check_indices_are_the_same(dfs, idx_name)]
    Log.info("check_column_names : %s" % rets[0])
    Log.info("check_indices : %s" % rets[1])
    if rets == [True] * len(rets):
        Log.info("check_values : %s" % check_values(dfs, 2))


def main():
    test_case()


if __name__ == "__main__":
    main()
