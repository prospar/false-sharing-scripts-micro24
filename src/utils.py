"""
Helper module with useful utility functions.
"""

import os
import sys
from enum import Enum

import numpy as np
import pandas as pd
import scipy.stats


def get_max_val(dict1: dict, dict2: dict) -> dict:
    """
    Return a dictionary that includes the maximum value for every key from two input dictionaries.
    """
    assert len(dict1) == len(dict2)
    max_val: dict = {key: max(value, dict2[key]) for key, value in dict1.items()}
    return max_val


def is_dict_in_list(my_list: list, my_dict: dict) -> bool:
    """
    Return True if the input list 'my_list' contains a dictionary element 'my_dict'.
    """
    return my_dict in my_list


# https://stackoverflow.com/questions/9427163/remove-duplicate-dict-in-list-in-python
def remove_duplicate_dicts_from_list(my_list: list) -> list:
    """
    Remove duplicate dictionaries from a list of dictionaries.
    """
    return [dict(t) for t in {tuple(d.items()) for d in my_list}]


# https://stackoverflow.com/questions/19755376/getting-the-difference-delta-between-two-lists-of-dictionaries
def get_diff_two_list_of_dicts(input_list1: list, input_list2: list) -> list:
    """
    Compute the difference of two lists of dictionaries and return the difference as a list.
    """
    import itertools
    diff: list = list(itertools.filterfalse(lambda x: x in input_list1, input_list2)) + list(
        itertools.filterfalse(lambda x: x in input_list2, input_list1))
    return diff


# https://stackoverflow.com/questions/2130016/splitting-a-list-into-n-parts-of-approximately-equal-length
def split_list_into_n_approx_equal_parts(a: list, n: int):
    """
    Split the list into n approximately equal parts. Return a list of lists.
    """
    k, m = divmod(len(a), n)
    return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))


def str_to_float(_inp: str) -> float:
    """Return float equivalent of the string, return zero if empty string.
    """
    _inp = _inp.strip()
    return float(_inp) if _inp else 0


def str_to_int(_inp: str) -> int:
    """Return integer equivalent of the string, return zero if empty string.
    """
    _inp = _inp.strip()
    return int(_inp) if _inp else 0


def str_to_bool(_inp: str) -> bool:
    """
    Return boolean equivalent of the string, return False if empty string.
    """
    _inp = _inp.strip()
    return _inp.lower() == "y" or _inp.lower() == "yes"


def raise_error(*args, stack=False):
    """Raise errors and exit.

    stack is a 'keyword-only' argument, meaning that it can only be used as a keyword rather than a
    positional argument.
    """
    if stack:
        import traceback
        traceback.print_stack()
    stmt = "[error] "
    for s in args:
        stmt += s + " "
    sys.exit(stmt)


def check_and_create_dir(outputDir: str) -> bool:
    """
    Create directory only if outputDir is not present.
    """
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)
        return True
    return False


# https://stackoverflow.com/questions/598398/searching-a-list-of-objects-in-python
def contains(list_, filter_):
    """
    Search a list of objects for any match based on the filter, even a match with one element will
    do.  Invoke with 'contains(myList, lambda x: x.n == 3)', will return True if any element has
    attribute n==3.
    """
    for x in list_:
        if filter_(x):
            return True
    return False


# https://stackoverflow.com/questions/3697432/how-to-find-list-intersection
def check_list_intersection(inp_list1: list, inp_list2: list) -> list:
    """Does not care about the order and duplicates."""
    return list(set(inp_list1) & set(inp_list2))


def dump_concatenated_csv_files(inp_path1: str,
                                inp_path2: str,
                                output_path: str,
                                DELETE_FILES=False):
    """
    Concatenate the two CSVs represented by the input absolute paths, and dump the output to a CSV
    file.
    """
    df1 = pd.DataFrame()
    if os.path.exists(inp_path1):
        df1 = pd.DataFrame(pd.read_csv(inp_path1))
    else:
        raise_error(f"Input file {inp_path1} does not exist!")

    df2 = pd.DataFrame()
    if os.path.exists(inp_path2):
        df2 = pd.DataFrame(pd.read_csv(inp_path2))
    else:
        raise_error(f"Input file {inp_path2} does not exist!")

    com_df = pd.DataFrame()

    # Files can be empty
    if not df1.empty and not df2.empty:
        com_df = pd.concat([df1, df2])
        assert com_df.shape[0] == df1.shape[0] + df2.shape[0]
    elif not df1.empty and df2.empty:
        com_df = df1
    elif df1.empty and not df2.empty:
        com_df = df2

    if not com_df.empty:
        com_df.reset_index(inplace=True, drop=True)
        com_df.index = np.arange(1, len(com_df) + 1)
        com_df.to_csv(output_path)
    else:
        print("Input files are empty!")

    if DELETE_FILES:
        for path_ in [inp_path1, inp_path2]:
            if os.path.exists(path_):
                os.remove(path_)


def get_diff_dataframe_rows_based_on_column(df1, df2, colname: str):
    """
    Print rows that are different between the two dataframes according to the values in column
    'colname'. The two dataframes should have the same number of rows.

    Keyword arguments:
    df1 -- [description]
    df2 -- [description]
    colname -- [description]
    """
    df1['diff'] = np.where((df1[colname] == df2[colname]), True, False)
    print(df1.loc[df1["diff"] is not True])


def get_rows_from_superset_dataframe(df1, df2, colname: str):
    """
    Get rows of df1 which are not in df2 based on column 'colname'. The data should match for
    rows that are present in both. That is, df1 is a superset of df2.

    Keyword arguments:
    df1 -- [description]
    df2 -- [description]
    """

    # Perform a left-join, eliminating duplicates in df2 so that each row of df1 joins with exactly
    # one row of df2.
    # The number of columns can be increased by specifying a list
    df_all = df1.merge(df2.drop_duplicates(), on=[colname], how='left', indicator=True)
    print(df_all["_merge"] == "left_only")


def join_two_dataframes_based_on_cols(df1, df2, colname: str):
    """[summary]"""
    merge_df = pd.merge(df1, df2, how="inner", on=[colname])
    print(merge_df)


# https://stackoverflow.com/questions/2474015/getting-the-index-of-the-returned-max-or-min-item-using-max-min-on-a-list
def get_max_and_index(data: list) -> list:
    val = max(data)
    idx = max(range(len(data)), key=data.__getitem__)
    return [val, idx]


def get_min_and_index(data: list) -> list:
    val = min(data)
    idx = min(range(len(data)), key=data.__getitem__)
    return [val, idx]


def limit_to_dicts_with_key(resultsSet: list, key: str) -> list:
    """Limit the incoming results set (which is a list of dictionaries) to a sublist of
      dictionaries that have the key.
      """
    tmp = []
    for dic in resultsSet:
        if key in dic:
            tmp.append(dic)
    return tmp


def limit_to_dicts_with_dict(resultsSet: list, di_limit: dict) -> list:
    """Limit incoming list of dictionaries rs to only those entries that contain the given
     dictionary di_limit.
     """
    li_tmp = []
    for d in resultsSet:
        if all(item in d.items() for item in di_limit.items()):
            li_tmp.append(d.copy())
    return li_tmp


def union_all_keys(rs: list) -> list:
    """Take the union of keys across all dicts in rs."""
    return list(set().union(*(d.keys() for d in rs)))


class MergeType(Enum):
    MERGE_MAX = 1
    MERGE_MIN = 2
    MERGE_AVG = 3
    MERGE_MED = 4
    MERGE_GEOMEAN = 5
    MERGE_CI = 6

    @staticmethod
    def _mergeAverage(rs: list, key: str) -> dict:
        """Merge the result set which is a list of dicts, and return the average."""
        fl_sum = 0.0
        tmp = {}
        try:
            if rs:
                for d in rs:
                    if d.get(key) is not None:
                        fl_sum += d.get(key)
                tmp[key] = fl_sum / len(rs)
            else:
                tmp[key] = 0
        except (ZeroDivisionError, TypeError) as e:
            print(f"Data set: \n{rs}\n"
                  f"Key: {key}")
            raise_error(repr(e) + ", Key:" + key, stack=True)
        return tmp

    @staticmethod
    def _mergeMedian(rs: list, key: str) -> dict:
        """Merge the result set which is a list of dicts, and return the median."""
        lst = []
        for d in rs:
            lst.append(d.get(key))
        tmp = {}
        tmp[key] = np.median(np.array(lst))
        return tmp

    # LATER: One option is to ignore zero values and then compute geomean for the rest.
    @staticmethod
    def _mergeGeoMean(rs: list, key: str) -> dict:
        """Merge the result set which is a list of dicts, and return the geomean."""
        b_zeroFound = False
        lst = []
        for d in rs:
            if d.get(key) == 0.0:
                b_zeroFound = True
                break
            lst.append(d.get(key))
        tmp = {key: 0.0}
        if not b_zeroFound:
            tmp[key] = scipy.stats.gmean(np.array(lst))
        return tmp

    @staticmethod
    def _mergeMin(rs: list, key: str) -> dict:
        """Merge the result set which is a list of dicts, and return the min."""
        lst = []
        for d in rs:
            lst.append(d.get(key))
        tmp = {}
        tmp[key] = min(lst)
        return tmp

    @staticmethod
    def _mergeMax(rs: list, key: str) -> dict:
        """Merge the result set which is a list of dicts, and return the max."""
        lst = []
        for d in rs:
            lst.append(d.get(key))
        tmp = {}
        tmp[key] = max(lst)
        return tmp

    @staticmethod
    def _mergeCI(rs: list, key: str) -> dict:
        """Calculate confidence intervals"""
        # https://stackoverflow.com/questions/15033511/compute-a-confidence-interval-from-sample-data
        ci_data = []
        fl_sum = 0.0
        avg = 0.0
        try:
            if rs:
                for d in rs:
                    fl_sum += d.get(key)
                    ci_data.append(d.get(key))
            else:
                ci_data = [0]
            avg = fl_sum / len(rs)
        except (ZeroDivisionError, TypeError) as e:
            raise_error(repr(e) + ", Key:" + key, stack=True)
        ci_data = scipy.stats.t.interval(0.95,
                                         len(ci_data),
                                         loc=np.mean(ci_data),
                                         scale=scipy.stats.sem(ci_data))[0]
        return {key: (avg - ci_data)}


def merge(rs: list, key: str, mergeType=MergeType.MERGE_AVG) -> dict:
    """Calculate confidence intervals"""
    """Merge the result set which is a list of dicts, and return the max."""

    if mergeType == MergeType.MERGE_AVG:
        return MergeType._mergeAverage(rs, key)
    if mergeType == MergeType.MERGE_MED:
        return MergeType._mergeMedian(rs, key)
    if mergeType == MergeType.MERGE_GEOMEAN:
        return MergeType._mergeGeoMean(rs, key)
    if mergeType == MergeType.MERGE_MIN:
        return MergeType._mergeMin(rs, key)
    if mergeType == MergeType.MERGE_MAX:
        return MergeType._mergeMax(rs, key)
    if mergeType == MergeType.MERGE_CI:
        return MergeType._mergeCI(rs, key)
    raise ValueError
