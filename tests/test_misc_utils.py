
from src.yt_utils.misc_utils import convert_num_str_to_int




def test_convert_num_str_to_int():
    in_ = ['345', '2525200', '34,659', '483,203,991', '50K', '33.2K', '4.3M', '50M']
    exp = [345, 2525200, 34659, 483203991, 50000, 33200, 4300000, 50000000]
    for a, b in zip(in_, exp):
        res = convert_num_str_to_int(a)
        assert res == b




if __name__ == '__main__':
    test_convert_num_str_to_int()

