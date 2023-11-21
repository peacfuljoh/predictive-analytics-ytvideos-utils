
import pandas as pd
import datetime

from src.ytpa_utils.constants import DT_FMT_DATE, DT_FMT_US
from src.ytpa_utils.df_utils import df_dt_codec


def try_df_dt_codec():
    day = datetime.datetime.strptime('2020-05-05', DT_FMT_DATE)
    days = [day + datetime.timedelta(days=i) for i in range(2)]

    datetime_ = datetime.datetime.strptime('2020-05-05 14:43:11.342435', DT_FMT_US)
    datetimes = [datetime_ + datetime.timedelta(hours=5 * i) for i in range(2)]

    df = pd.DataFrame(dict(
        day=days,
        datetime=datetimes
    ))

    func_encode_str = lambda df_col: df_col.astype(str)
    opts = dict(day={'func': func_encode_str},
                datetime={'func': func_encode_str})
    df2 = df.copy()
    df_dt_codec(df2, opts)

    df_exp = pd.DataFrame(dict(
        day=['2020-05-05', '2020-05-06'],
        datetime=['2020-05-05 14:43:11.342435', '2020-05-05 19:43:11.342435']
    ))

    print(df)

    print(df_exp)

    print(df2)

    assert df2.equals(df_exp)


if __name__ == '__main__':
    try_df_dt_codec()






