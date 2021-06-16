import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import *
from sklearn.ensemble import IsolationForest
from tqdm import tqdm
import seaborn as sns


import tools

sns.set_style('darkgrid')

ITER = 1


def proc_df(tms):
    tms = tms[[1, 2, 3, 4, 5]].copy()
    a_len = 3
    d_len = 3
    # kernel = np.ones(a_len) / a_len
    dh1_kernel = np.hstack((-np.ones(d_len) / d_len, 1, np.zeros(d_len)))
    dh2_kernel = np.hstack((np.zeros(d_len), 1, -np.ones(d_len) / d_len))
    # average_h = np.convolve(kernel,df["alt"].to_numpy(),mode="same")
    tm = tms[5].to_numpy()
    ts = tms[4].to_numpy()
    dm1 = np.convolve(dh1_kernel, tm, mode="same")
    dm2 = np.convolve(dh2_kernel, tm, mode="same")
    ds1 = np.convolve(dh1_kernel, ts, mode="same")
    ds2 = np.convolve(dh2_kernel, ts, mode="same")
    # df["alt_"] = average_h
    tms["dm1"] = dm1
    tms["dm2"] = dm2
    tms["ds1"] = ds1
    tms["ds2"] = ds2
    return tms


def filter1(tms, key_ps = ["dm1", "dm2", "ds1", "ds2"]):
    for i in range(ITER):
        tms = proc_df(tms)
        try:
            res = KMeans(n_clusters=2).fit(tms[key_ps].abs())
        except TypeError:
            print(tms.shape)
        #     res = AgglomerativeClustering(n_clusters=2).fit(data[["dh1","dh2"]].abs())
        # yhat = IsolationForest(contamination=0.03).fit_predict(data[["dh1","dh2"]].abs())
        #     res = OPTICS().fit(data[["dh1","dh2"]].abs())
        #     data["label"] = res.labels_
        one_len = (res.labels_ == 1).sum()
        zero_len = (res.labels_ == 0).sum()
        if one_len > zero_len:
            tms = tms[res.labels_ == 1]
        else:
            tms = tms[res.labels_ == 0]
        # print(i, len(data))

    return tms


test_fp = "../radio/wyoming/04339/tm.txt"
df = pd.read_csv(test_fp, header=None)
df[0] = pd.to_datetime(df[0], format="%y%m%d/%H%M")
df.index = df[0]
df = df[[1, 2, 3, 4, 5]]
# df.reindex(df[0])
# df.rei
print(df.head())

trends, noise = tools.remove_trend(df)


kdata = filter1(df)

data = filter1(noise)
print(data.head())

plt.plot(df[5], label="Tm")
plt.plot(trends.loc[data.index, 5]+data[5], label="Filter")
plt.plot(trends[5], label="Trends")

# plt.plot(df[5], label="Tm")

def iqr(tms):
    tms = tms.copy()
    q1 = tms.quantile(0.25)
    q3 = tms.quantile(0.75)
    IQR = q3 - q1
    lr = q1 - 1.5 * IQR
    ur = q3 + 1.5 * IQR
    tms = tms[tms<ur]
    tms = tms[tms>lr]
    return tms


ff = iqr(noise[5])

# plt.plot(trends.loc[ff.index, 5]+ff, label="Filter")


# anomaly_detect_ts(df[5], direction="both", alpha=0.05, plot=True, longterm=True)

Tm = df.loc[ff.index, 5]
Ts = df.loc[ff.index, 4]

Tm_hat = Ts*0.72 + 70.2

ones = np.ones_like(np.expand_dims(Ts.to_numpy().transpose(),1))

A = np.hstack([np.expand_dims(Ts.to_numpy().transpose(),1), ones])
b = np.dot(np.dot(np.linalg.inv(np.dot(A.transpose(), A)), A.transpose()), Tm.to_numpy())

Tm_my = Ts * 0.75465213 + 59.8379946

print(b)
# plt.plot(Tm, label="Tm")
# plt.plot(Tm_hat, label="Bevis")
# plt.plot(Tm_my, label="single")
# plt.plot(Tm_hat-Tm, label="res_bevis")
# plt.plot(Tm_my-Tm, label="res_single")
plt.legend()
plt.show()
