from Utils import DataFrameHelper as dfh
from Utils import Log
import pandas as pd
import re
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


def plot_timeseries_by_column(dfs, idx_name, data_col, unit=None):
    """
    Sanity check dfs to be plotted for required columns. Format inputs nicely to pass
    to :func:`MatPlotLibHelper.plot_timeseries`
    :param dfs: list of dataframes
    :param idx_name: column name of index
    :param data_col: columns in the dfs that you want plotted
    :param unit: if index column is numeric, the time unit these values are in - ie ['D', 's', 'ms', 'us', 'ns']
    :return:
    """
    # convert single dataframe into list
    if type(dfs) is not list:
        dfs = [dfs]

    if type(data_col) is not list:
        data_col = [data_col]

    cols = [idx_name] + data_col
    if dfh.check_column_is_in_dataframes(dfs, cols) is False:
        return

    # now really plot
    tmp = [df[cols] for df in dfs]
    plot_timeseries(tmp, idx_name, unit)


def plot_timeseries(dfs, idx_name, unit=None):
    """
    Plot timeseries given curated dataframes
    :param dfs: list of dataframes - assumed to consist of idx column and all columns to plotted
    :param idx_name: column name of index, assumed to be some timestamp format. must exist in all dataframes
    :param unit: if index column is numeric, the time unit these values are in - ie ['D', 's', 'ms', 'us', 'ns']
    :return: nothing - just pretty plots
    """
    # convert single dataframe into list
    if type(dfs) is not list:
        dfs = [dfs]

    if dfh.check_column_is_in_dataframes(dfs, idx_name) is False:
        return

    # check if timestamps need formatting
    tmp = [df.copy() for df in dfs]

    # Infer Timestamp format
    sample = tmp[0].iloc[0][idx_name]
    if type(sample) == int and unit is not None and unit in ['D', 's', 'ms', 'us', 'ns']:
        # format timestamp in data
        for df in tmp:
            df[idx_name] = pd.to_datetime(df[idx_name], unit=unit)
        if unit in ['ms', 'us', 'ns']:
            fmt = '%Y/%m/%d %H:%M:%S.%f'
        elif unit == 's':
            fmt = '%Y/%m/%d %H:%M:%S'
        else:
            fmt = '%Y/%m/%d'
    elif type(sample) == str:
        # YYYY mm dd HH MM SS fff[ffffff]
        pattern_YYYYmmddHHMMSSfffffffff = '^([0-9]{4})[^0-9]{,1}([0-9]{2})[^0-9]{,1}([0-9]{2})[^0-9]{,1}([0-9]{2})[^0-9]{,1}([0-9]{2})[^0-9]{,1}([0-9]{2})[^0-9]{,1}([0-9]{3,})$'
        pattern_YYYYmmddHHMMSS = '^([0-9]{4})[^0-9]{,1}([0-9]{2})[^0-9]{,1}([0-9]{2})[^0-9]{,1}([0-9]{2})[^0-9]{,1}([0-9]{2})[^0-9]{,1}([0-9]{2})$'
        pattern_YYYYmmdd = '^([0-9]{4})[^0-9]{,1}([0-9]{2})[^0-9]{,1}([0-9]{2})$'

        result = re.match(pattern_YYYYmmddHHMMSSfffffffff, sample)
        if result is not None:
            fmt = '%Y/%m/%d %H:%M:%S.%f'
        else:
            result = re.match(pattern_YYYYmmddHHMMSS, sample)
            if result is not None:
                fmt = '%Y/%m/%d %H:%M:%S'
            else:
                result = re.match(pattern_YYYYmmdd, sample)
                if result is not None:
                    fmt = '%Y/%m/%d'
                else:
                    Log.err("Unknown format for index %s : [%s]" % (idx_name, sample))
        # format timestamp in data
        for df in tmp:
            df[idx_name] = pd.to_datetime(df[idx_name], format=fmt)
    else:
        Log.err("Unknown dtype for %s : [%s]" % (idx_name, tmp[0][idx_name].dtype))
        return

    # format timestamp in plot
    date_form = matplotlib.dates.DateFormatter(fmt)

    # i am going to ply everything you give me
    fig, ax = plt.subplots(figsize=(8.8, 8))
    cols = list(dfs[0].columns)
    cols.remove(idx_name)
    for df in tmp:
        for c in cols:
            # fill nans - fwd then back
            while df[c].hasnans:
                df[c].fillna(method='ffill', inplace=True)
                df[c].fillna(method='bfill', inplace=True)
            # plot
            ax.plot(df[idx_name], df[c])

    # set the date format
    ax.xaxis.set_major_formatter(date_form)
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right", fontsize=8)

    # make bottom axis thicker to accommodate timestamp length
    plt.subplots_adjust(bottom=0.15)

    plt.legend(loc='best')
    plt.show()


def main():
    df = dfh.get_test_dataframe()
    plot_timeseries_by_column(df, 'TimeStamp', ['ID', 'Value'])


if __name__ == '__main__':
    main()