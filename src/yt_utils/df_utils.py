

from typing import List, Optional
import pandas as pd
import numpy as np

from src.yt_utils.val_utils import is_subset



""" Array, DataFrame, and SQL ops """
def df_generator_wrapper(func):
    """
    Wrapper for handling StopIteration and other generator exceptions when yielding a DataFrame.
    Use this to decorate functions that return a DataFrame.
    """
    def wrap(*args, **kwargs):
        while 1:
            try:
                yield func(*args, **kwargs)
            except StopIteration:
                yield pd.DataFrame()
    return wrap

def join_on_dfs(df0: pd.DataFrame,
                df1: pd.DataFrame,
                index_keys: List[str],
                df0_keys_select: Optional[List[str]] = None,
                df1_keys_select: Optional[List[str]] = None) \
        -> pd.DataFrame:
    """
    Combine info from two DataFrames analogously to the SQL op:
        SELECT df0.col00, df0.col01, df1.col10 FROM df0 JOIN ON df0.index_key0 = df1.index_key0

    The index keys in df0 are treated like foreign keys into df1.
    """
    # TODO: handle case where index keys in df0 don't exist in df1
    # perform select on df0
    if df0_keys_select is not None:
        df0_select = df0[df0_keys_select]
    else:
        df0_select = df0

    # turn index keys in df1 into multi-index
    df1_mindex = df1.set_index(index_keys, drop=True)

    # get index keys for all rows of df0
    ids_ = df0[index_keys].to_numpy().tolist()
    if len(index_keys) == 1:
        ids_ = [id_[0] for id_ in ids_]
    else:
        ids_ = [tuple(id_) for id_ in ids_]

    # perform select on df1
    assert is_subset(ids_, df1_mindex.index) # all ID keys in df0 must exist in df1's multi-index for the JOIN
    if df1_keys_select is not None:
        df1_select = df1_mindex.loc[ids_, df1_keys_select]
    else:
        df1_select = df1_mindex.loc[ids_]
    df1_select = df1_select.set_index(df0.index)

    # concatenate
    df = pd.concat((df0_select, df1_select), axis=1)

    return df

def convert_mixed_df_to_array(df: pd.DataFrame,
                              cols: Optional[List[str]] = None) \
        -> np.ndarray:
    """
    Convert DataFrame with mixed-type columns into a numpy array.
    Only converts numerical columns. Emits warning for non-numerical/list-type columns.
    """
    if cols is None:
        cols = df.columns

    data: List[np.ndarray] = []
    for col in cols:
        data_ = df[col]
        samp0 = data_.iloc[0]
        if isinstance(samp0, (int, float, np.int64, np.float64)):
            data.append(data_.to_numpy()[:, np.newaxis])
        elif isinstance(samp0, list):
            data.append(np.array(list(data_)))
        else:
            print(f'convert_mixed_df_to_array() -> Skipping column {col} with invalid raw_data type {type(samp0)}.')

    return np.hstack(data)

def get_duplicate_idxs(df: pd.DataFrame,
                       colname: str) \
        -> pd.DataFrame:
    """
    Get duplicate indices for entries in a specified column of a DataFrame.

    Steps:
        - adds col with index values
        - group rows by specified column
        - aggregate rows into groups, add two cols with duplicate first appearance + row indices where duplicates appear
        - convert to DataFrame with index (first index) and one column (duplicate indices)
    """
    idxs = (df[[colname]].reset_index()
            .groupby([colname])['index']
            .agg(['first', tuple])
            .set_index('first')['tuple'])
    return idxs

def df_dt_codec(df: pd.DataFrame,
                opts: dict,
                mode: str):
    """
    In-place conversion of specified columns (keys of opts) between strings and datetimes with specified format
    (vals in opts).

    encode: from timestamps or datetimes to strings
    decode: from strings to datetime of specified formats
    """
    assert mode in ['encode', 'decode']
    for key, dt_fmt in opts.items():
        if mode == 'encode':
            df[key] = df[key].astype(str)
        else:
            raise NotImplementedError