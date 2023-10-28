
import datetime

import numpy as np
import pandas as pd

from src.ytpa_utils.val_utils import (is_dict_of_instances, is_list_of_formatted_strings,
                                      is_list_of_list_of_time_range_strings, is_list_of_floats,
                                      is_datetime_formatted_str, is_int_or_float, is_subset,
                                      is_list_of_sequences, is_list_of_strings, is_list_of_list_of_strings)
from src.ytpa_utils.constants import DT_FMT_DATE, DT_FMT_US



def test_is_dict_of_istances():
    d = dict(a='a', b='b', c='c')
    assert is_dict_of_instances(d, str)

    d = dict(a=5, b=4, c=2)
    assert is_dict_of_instances(d, int)

    d = dict(a=[1], b=[3], c=[5, 6])
    assert is_dict_of_instances(d, list)

def dt_fmt_func(dt, fmt):
    try:
        datetime.datetime.strptime(dt, fmt)
    except:
        return False
    return True

def test_is_list_of_formatted_strings():
    obj = ['2020-05-03', '2020-07-06', '2020-05-06']
    assert is_list_of_formatted_strings(obj, lambda x: dt_fmt_func(x, DT_FMT_DATE), list_len=3)

    obj = ['2020-05-03 05:40:30.332', '2020-07-06 06:05:03.234']
    assert is_list_of_formatted_strings(obj, lambda x: dt_fmt_func(x, DT_FMT_US))

    obj = ['2020-05-03 05:40:30.332', '2020-07-06 06:05:03']
    assert ~is_list_of_formatted_strings(obj, lambda x: dt_fmt_func(x, DT_FMT_US))

def test_is_list_of_list_of_time_range_strings():
    obj = [['2020-05-03', '2020-07-06'], ['2020-05-06', '2020-06-06']]
    assert is_list_of_list_of_time_range_strings(obj, lambda x: dt_fmt_func(x, DT_FMT_DATE))

    obj = [['2020-05-03', '2020-07-06'], ['2020-05-06', '2020-06-06', '2020-04-05']]
    assert ~is_list_of_list_of_time_range_strings(obj, lambda x: dt_fmt_func(x, DT_FMT_DATE))

    obj = [['2020-05-03 05:40:30.332', '2020-07-06 06:05:03.234'], '2020-05-03 05:40:30.332']
    assert ~is_list_of_list_of_time_range_strings(obj, lambda x: dt_fmt_func(x, DT_FMT_DATE))

def test_is_list_of_floats():
    obj = [1, 4, 2, 3]
    assert is_list_of_floats(obj)

    obj = [1.5, 4.3, 2, 3]
    assert is_list_of_floats(obj)

    obj = [1, 4, 2, 3, 'a']
    assert ~is_list_of_floats(obj)

    obj = [1, 4, 2, 3, [5]]
    assert ~is_list_of_floats(obj)

def test_is_datetime_formatted_str():
    s = '2020-05-03'
    assert is_datetime_formatted_str(s, DT_FMT_DATE)

    s = '2020-05-03 05:40:30.332'
    assert is_datetime_formatted_str(s, DT_FMT_US)

    s = '2020-05-03 05:40:30.332'
    assert ~is_datetime_formatted_str(s, DT_FMT_DATE)

def test_is_int_or_float():
    assert is_int_or_float(5)
    assert is_int_or_float(5.0)
    assert is_int_or_float(np.int64(5))
    assert is_int_or_float(np.float64(5))
    assert ~is_int_or_float('5')

def test_is_subset():
    d = dict(a=[1, 2], b=[3, 4], c=['asdfa', 'fdsfb'])
    df = pd.DataFrame(d)

    assert is_subset(['a', 'b'], d)
    assert is_subset(['a', 'c'], df.columns)
    assert is_subset(['b', 'a'], {'b', 'd', 3, 'a'})
    assert ~is_subset(['b', 'a'], {'d', 3, 'a'})

def test_is_list_of_sequences():
    assert is_list_of_sequences([(1, 2), (5, 6)], (tuple,))
    assert is_list_of_sequences([[1, 2], [5, 6]], (list,))
    assert is_list_of_sequences([[1, 2], (5, 6)], (list, tuple))
    assert ~is_list_of_sequences([[1, 2], 5, 6], (list, tuple))

def test_is_list_of_strings():
    assert is_list_of_strings(['a', 'b', 'd'])
    assert is_list_of_strings(['a', 'b', 'asdsdfs'])
    assert ~is_list_of_strings(['a', 3, 'asdsdfs'])

def test_is_list_of_list_of_strings():
    assert is_list_of_list_of_strings([['a', 'b']])
    assert is_list_of_list_of_strings([['a', 'b'], ['c']])
    assert ~is_list_of_list_of_strings([['a', 'b'], 'c'])

