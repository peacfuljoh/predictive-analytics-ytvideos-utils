
from src.ytpa_utils.misc_utils import (convert_num_str_to_int, apply_regex, remove_trailing_chars, just_dict_keys,
                                       print_df_full, convert_bytes_to_image, fetch_data_at_url)



NUM_STRS_IN = ['345', '2525200', '34,659', '483,203,991', '50K', '33.2K', '4.3M', '50M']
NUM_STRS_OUT = [345, 2525200, 34659, 483203991, 50000, 33200, 4300000, 50000000]


def test_convert_num_str_to_int():
    for a, b in zip(NUM_STRS_IN, NUM_STRS_OUT):
        res = convert_num_str_to_int(a)
        assert res == b

def test_apply_regex():
    substring_flag = '(.*?)'

    regex_exs_num = {
        '"defaultText":{"accessibility":{"accessibilityData":{"label":"(.*?) likes"}}': None,
        '"commentCount":{"simpleText":"(.*?)"},"contentRenderer"': None,
        'subscribers"}},"simpleText":"(.*?) subscribers"}': None,
    }
    regex_exs_txt_one = {
        '"teaserContent":{"simpleText":"(.*?)"},"trackingParams":"': ['abcde', 'xyz', 'a--4--@'],
        '"uploadDate":"(.*?)"': ['2023-05-06', '2022-11-12']}
    regex_exs_txt_mult = {
        '"videoDetails":{"videoId":(.*?),"author":"(.*?)",': [('abcde', 'vwxyz')]
    }

    for regex, val in regex_exs_num.items():
        for s_in, s_out in zip(NUM_STRS_IN, NUM_STRS_OUT):
            s_sub = regex.replace(substring_flag, s_in)
            s_full = '234234asfasdf' + s_sub + 'asdof8y3rbaosd87fh'
            assert apply_regex(s_full, regex, dtype='int') == s_out
    for regex, val in regex_exs_txt_one.items():
        for s in val:
            s_sub = regex.replace(substring_flag, s)
            s_full = '234234asfasdf' + s_sub + 'asdof8y3rbaosd87fh'
            assert apply_regex(s_full, regex) == s
    for regex, vals in regex_exs_txt_mult.items():
        for ss in vals:
            s_sub = regex.split('(.*?)')
            i_start = len(s_sub) - 1
            for i in range(len(ss)):
                s_sub.insert(i_start - i, ss[-1 - i])
            s_sub = ''.join(s_sub)
            s_full = '234234asfasdf' + s_sub + 'asdof8y3rbaosd87fh'
            assert apply_regex(s_full, regex)[0] == ss

def test_print_df_full():
    pass

def test_fetch_data_at_url():
    pass

def test_convert_bytes_to_image():
    pass

def test_remove_trailing_chars():
    trail_chars = ['\n', ' ']
    s = 'as7f asd07asd 0asd \n '
    assert remove_trailing_chars(s, trail_chars) == 'as7f asd07asd 0asd'

    trail_chars = ['\n', ' ', '.']
    s = 'asd7fa.s7s78sa ..\n '
    assert remove_trailing_chars(s, trail_chars) == 'asd7fa.s7s78sa'

def test_just_dict_keys():
    d = {'a': {'b': [1, 2, 3], 'c': [5, 4, 'a']}, 'd': [1, 2, 3], 'e': '2432'}
    exp = {'a': {'b': None, 'c': None}, 'd': None, 'e': None}
    assert just_dict_keys(d) == exp

