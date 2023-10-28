
import datetime

from src.constants import (TESTING, DT_STR_TEST_US, DT_STR_TEST_DATE, DT_STR_TEST_S, DT_STR_TEST_MS,
                           DT_STR_TEST_DATE_OFFSET, DT_STR_TEST_S_OFFSET, DT_STR_TEST_MS_OFFSET, DT_STR_TEST_US_OFFSET,
                           DT_FMT_DATE, DT_FMT_SEC, DT_FMT_MS, DT_FMT_US)
from src.ytpa_utils.time_utils import get_ts_now_formatted, get_ts_now_str, get_dt_now, TimeLock



def test_get_ts_now_formatted():
    # get_ts_now_formatted()
    TESTING[0] = True

    s_exp_all = [DT_STR_TEST_DATE_OFFSET, DT_STR_TEST_S_OFFSET, DT_STR_TEST_US_OFFSET, DT_STR_TEST_US_OFFSET]
    for fmt, s_exp in zip([DT_FMT_DATE, DT_FMT_SEC, DT_FMT_MS, DT_FMT_US], s_exp_all):
        assert s_exp == get_ts_now_formatted(fmt, offset=datetime.timedelta(days=1, hours=5))

def test_get_ts_now_str():
    TESTING[0] = True

    s_exp_all = [DT_STR_TEST_DATE, DT_STR_TEST_S, DT_STR_TEST_MS, DT_STR_TEST_US]
    for mode, s_exp in zip(['date', 's', 'ms', 'us'], s_exp_all):
        assert s_exp == get_ts_now_str(mode)

    s_exp_all = [DT_STR_TEST_DATE_OFFSET, DT_STR_TEST_S_OFFSET, DT_STR_TEST_MS_OFFSET, DT_STR_TEST_US_OFFSET]
    for mode, s_exp in zip(['date', 's', 'ms', 'us'], s_exp_all):
        assert s_exp == get_ts_now_str(mode, offset=datetime.timedelta(days=1, hours=5))

def test_get_dt_now():
    TESTING[0] = True

    dt = get_dt_now()
    assert datetime.datetime.strptime(DT_STR_TEST_US, DT_FMT_US) == dt

def test_TimeLock():
    pass
