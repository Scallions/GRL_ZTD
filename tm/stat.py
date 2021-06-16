"""
Some code for statistics analysis
"""


def r_index(ts1, ts2):
    return ts1.corr(ts2)


