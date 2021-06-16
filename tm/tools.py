import numpy as np


def read_sites():
    """read site meta data from csv file

    Returns:
        [site_metadata]: metadata of radio sites
    """
    sites = []
    with open("temp/wyoming_sites.csv", "r") as f:
        for line in f.readlines():
            data = line.split()
            sites.append(data)
    return sites

def tm_files():
    sites = read_sites()
    for site in sites:
        site_name = site[0]
        fp = f"./radio/wyoming/{site_name}/tm.txt"
        yield fp


def remove_trend(mts):
    """从时间序列中提取周年项，和残差
    Args:
        mts ([type]): [description]
    Returns:
        [type]: [description]
    """

    def trend_of_ts(ts):
        length = len(ts)
        x = np.array(list(range(length))).reshape((length, 1))
        sinx = np.sin(x*np.pi*2/365/2)
        cosx = np.cos(x*np.pi*2/365/2)
        sin2x = np.sin(2*x*np.pi*2/365/2)
        cos2x = np.cos(2*x*np.pi*2/365/2)
        ones = np.ones((length, 1))
        data = np.hstack((ones, x, sinx, cosx, sin2x, cos2x))
        # data = np.hstack((ones, x))
        b = np.dot(np.dot(np.linalg.inv(np.dot(data.transpose(), data)), data.transpose()), ts)
        ts_hat = np.dot(data, b)
        noise = ts - ts_hat
        trend = pd.DataFrame(data=ts_hat, index=mts.index, columns=[ts.name])
        noise = pd.DataFrame(data=noise, index=mts.index, columns=[ts.name])
        return trend, noise

    trends = None
    noise = None
    for ts in mts:
        trend, noise = trend_of_ts(mts[ts])
        if trends is None:
            trends = trend
            noises = noise
        else:
            trends = pd.concat([trends, trend], axis=1)
            noises = pd.concat([noises, noise], axis=1)

    return trends, noises