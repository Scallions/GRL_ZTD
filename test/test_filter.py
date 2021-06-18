import pytest
import pandas as pd
import os

import tm.filter as filter

@pytest.fixture()
def tm_ts():
    print(os.getcwd())
    test_fp = "../radio/wyoming/04339/tm.txt"
    df = pd.read_csv(test_fp, header=None)
    df[0] = pd.to_datetime(df[0], format="%y%m%d/%H%M")
    df.index = df[0]
    df = df[[1, 2, 3, 4, 5]]
    return df


def test_filter(tm_ts):
    l1 = len(tm_ts)
    tm_ts_f = filter.Filter().filter(tm_ts)
    l2 = len(tm_ts_f)
    assert l1 > l2
