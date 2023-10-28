
import pandas as pd
import numpy as np
import datetime

from src.constants import DT_FMT_DATE, DT_FMT_US
from src.ytpa_utils.df_utils import get_duplicate_idxs, join_on_dfs, convert_mixed_df_to_array, df_dt_codec




def test_join_on_dfs():
    # single index
    df0 = pd.DataFrame(
        dict(
            id0=['id_0', 'id_1', 'id_0', 'id_0', 'id_1'],
            val0=[1, 2, 3, 4, 5],
            val1=[6, 7, 8, 9, 10],
            str0=['a', 'b', 'c', 'd', 'e']
        )
    )

    df1 = pd.DataFrame(
        dict(
            id0=['id_0', 'id_1'],
            arr0=[[7, 8, 7], [112, 332, 231]]
        )
    )

    df_join = join_on_dfs(
        df0,
        df1,
        index_keys=['id0'],
        df0_keys_select=['id0', 'val0', 'str0'],
        df1_keys_select=['arr0']
    )

    df_join_expected = pd.DataFrame(
        dict(
            id0=['id_0', 'id_1', 'id_0', 'id_0', 'id_1'],
            val0=[1, 2, 3, 4, 5],
            str0=['a', 'b', 'c', 'd', 'e'],
            arr0=[[7, 8, 7], [112, 332, 231], [7, 8, 7], [7, 8, 7], [112, 332, 231]]
        )
    )

    assert len(df_join) == len(df_join_expected)
    assert all(df_join.columns == df_join_expected.columns)
    for i in df_join.index:
        for key in df_join.columns:
            assert df_join.loc[i, key] == df_join_expected.loc[i, key]

    # multi-index
    df0 = pd.DataFrame(
        dict(
            id0=['id_0', 'id_1', 'id_0', 'id_0', 'id_1'],
            id1=['id_5', 'id_5', 'id_6', 'id_5', 'id_5'],
            val0=[1, 2, 3, 4, 5],
            val1=[6, 7, 8, 9, 10],
            str0=['a', 'b', 'c', 'd', 'e']
        )
    )

    df1 = pd.DataFrame(
        dict(
            id0=['id_0', 'id_0', 'id_1'],
            id1=['id_5', 'id_6', 'id_5'],
            arr0=[[7, 8, 7], [5, 4, 3], [112, 332, 231]]
        )
    )

    df_join = join_on_dfs(
        df0,
        df1,
        index_keys=['id0', 'id1'],
        df0_keys_select=['id0', 'id1', 'val0', 'str0'],
        df1_keys_select=['arr0']
    )

    df_join_expected = pd.DataFrame(
        dict(
            id0=['id_0', 'id_1', 'id_0', 'id_0', 'id_1'],
            id1=['id_5', 'id_5', 'id_6', 'id_5', 'id_5'],
            val0=[1, 2, 3, 4, 5],
            str0=['a', 'b', 'c', 'd', 'e'],
            arr0=[[7, 8, 7], [112, 332, 231], [5, 4, 3], [7, 8, 7], [112, 332, 231]]
        )
    )

    assert len(df_join) == len(df_join_expected)
    assert all(df_join.columns == df_join_expected.columns)
    for i in df_join.index:
        for key in df_join.columns:
            assert df_join.loc[i, key] == df_join_expected.loc[i, key]


def test_convert_mixed_df_to_array():
    d = dict(
        a=[1, 2, 3],
        b=[5, 6, 7],
        c=[[7, 6, 5], [4, 5, 3], [3, 2, 2]]
    )
    df = pd.DataFrame(d)

    arr = convert_mixed_df_to_array(df, ['a', 'b', 'c'])
    arr_exp = np.array([[1, 5, 7, 6, 5], [2, 6, 4, 5, 3], [3, 7, 3, 2, 2]])
    assert np.allclose(arr, arr_exp)

    arr = convert_mixed_df_to_array(df, ['a', 'b'])
    arr_exp = np.array([[1, 5], [2, 6], [3, 7]])
    assert np.allclose(arr, arr_exp)

    arr = convert_mixed_df_to_array(df, ['c', 'a'])
    arr_exp = np.array([[7, 6, 5, 1], [4, 5, 3, 2], [3, 2, 2, 3]])
    assert np.allclose(arr, arr_exp)


def test_get_duplicate_idxs():
    df = pd.DataFrame(dict(
        a=[4, 5, 4, 3, 2, 3],
        b=['a', 'a', 'e', 'e', 'a', 'e']
    ))

    idxs = get_duplicate_idxs(df, 'a')
    idxs_exp = pd.Series([(4,), (3, 5), (0, 2), (1,)], index=[4, 3, 0, 1])
    assert idxs.equals(idxs_exp)

    idxs = get_duplicate_idxs(df, 'b')
    idxs_exp = pd.Series([(0, 1, 4), (2, 3, 5)], index=[0, 2])
    assert idxs.equals(idxs_exp)


def test_df_dt_codec():
    day = datetime.datetime.strptime('2020-05-05', DT_FMT_DATE)
    days = [day + datetime.timedelta(days=i) for i in range(2)]

    datetime_ = datetime.datetime.strptime('2020-05-05 14:43:11.342435', DT_FMT_US)
    datetimes = [datetime_ + datetime.timedelta(hours=5 * i) for i in range(2)]

    df = pd.DataFrame(dict(
        day=days,
        datetime=datetimes
    ))

    opts = dict(day=DT_FMT_DATE, datetime=DT_FMT_US)
    df2 = df.copy()
    df_dt_codec(df2, opts, 'encode')

    df_exp = pd.DataFrame(dict(
        day=['2020-05-05', '2020-05-06'],
        datetime=['2020-05-05 14:43:11.342435', '2020-05-05 19:43:11.342435']
    ))

    assert df2.equals(df_exp)
