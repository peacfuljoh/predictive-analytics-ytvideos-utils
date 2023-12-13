
import pandas as pd
import numpy as np
import datetime
from pandas import Timestamp

from src.ytpa_utils.constants import DT_FMT_DATE, DT_FMT_US
from src.ytpa_utils.df_utils import (get_duplicate_idxs, join_on_dfs, convert_mixed_df_to_array, df_dt_codec,
                                     resample_one_df_in_time)




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
        datetime=datetimes,
        filler=[0, 1]
    ))

    func_encode_str = lambda df_col: df_col.astype(str)
    opts = dict(day={'func': func_encode_str},
                datetime={'func': func_encode_str},
                other={'func': None})
    df2 = df.copy()
    df_dt_codec(df2, opts)

    df_exp = pd.DataFrame(dict(
        day=['2020-05-05', '2020-05-06'],
        datetime=['2020-05-05 14:43:11.342435', '2020-05-05 19:43:11.342435'],
        filler=[0, 1]
    ))

    assert df2.equals(df_exp)

def test_resample_one_df_in_time():
    num_samps = 10

    day = datetime.datetime.strptime('2020-05-05', DT_FMT_DATE)
    dts = [day + datetime.timedelta(seconds=5 * i) for i in range(num_samps)]

    df = pd.DataFrame(dict(
        ts=dts,
        id=['a'] * num_samps,
        val=list(np.arange(num_samps))
    ))

    period = 3
    df_out = resample_one_df_in_time(df, period, ['id'], ['val'], 'ts')

    # print(df_out.to_dict())

    df_expected = pd.DataFrame.from_dict(
        {'val': {0: 0.0, 1: 0.6000000000000002, 2: 1.2000000000000002, 3: 1.8000000000000003, 4: 2.400000000000001,
                 5: 3.0, 6: 3.600000000000001, 7: 4.199999999999999, 8: 4.8, 9: 5.400000000000001, 10: 6.0,
                 11: 6.6000000000000005, 12: 7.200000000000003, 13: 7.8000000000000025, 14: 8.400000000000002},
         'ts': {0: Timestamp('2020-05-05 00:00:00'), 1: Timestamp('2020-05-05 00:00:03'),
                2: Timestamp('2020-05-05 00:00:06'), 3: Timestamp('2020-05-05 00:00:09'),
                4: Timestamp('2020-05-05 00:00:12'), 5: Timestamp('2020-05-05 00:00:15'),
                6: Timestamp('2020-05-05 00:00:18'), 7: Timestamp('2020-05-05 00:00:21'),
                8: Timestamp('2020-05-05 00:00:24'), 9: Timestamp('2020-05-05 00:00:27'),
                10: Timestamp('2020-05-05 00:00:30'), 11: Timestamp('2020-05-05 00:00:33'),
                12: Timestamp('2020-05-05 00:00:36'), 13: Timestamp('2020-05-05 00:00:39'),
                14: Timestamp('2020-05-05 00:00:42')},
         'id': {0: 'a', 1: 'a', 2: 'a', 3: 'a', 4: 'a', 5: 'a', 6: 'a', 7: 'a', 8: 'a', 9: 'a', 10: 'a', 11: 'a',
                12: 'a', 13: 'a', 14: 'a'}}
    )

    try:
        assert df_out.equals(df_expected)
    except Exception as e:
        print(df_out)
        print(df_expected)
        raise e





if __name__ == '__main__':
    test_resample_one_df_in_time()

