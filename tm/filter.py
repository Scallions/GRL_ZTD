"""
过滤粗差
"""

import abc

import pandas as pd
import numpy as np
from sklearn.cluster import *
# from sklearn.ensemble import IsolationForest
from tqdm import tqdm

import tools


class IFilterMethod(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def filter(self, tms):
        pass

    @abc.abstractmethod
    def filter_rate(self):
        pass


class KMeans(IFilterMethod):
    def __init__(self, ts):
        self.ts = ts

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

    def filter(self, tms, key_ps=["dm1", "dm2", "ds1", "ds2"]):
        ITER = 2
        for i in range(ITER):
            tms = self.proc_df(tms)
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

    def filter_rate(self):
        pass


class IQR(IFilterMethod):

    def filter(self, tms):
        tms = tms.copy()
        tm = tms[5]
        q1 = tm.quantile(0.25)
        q3 = tm.quantile(0.75)
        IQR = q3 - q1
        lr = q1 - 1.5 * IQR
        ur = q3 + 1.5 * IQR
        tm = tm[tm < ur]
        tm = tm[tm > lr]
        return tms.loc[tm.index]

    def filter_rate(self):
        pass


class ITrends(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def remove_trends(self, mts):
        pass


class NoRemove(ITrends):
    def remove_trends(self, mts):
        """
        不做任何移除
        Returns:

        """
        return pd.DataFrame(data=np.zeros_like(mts.to_numpy()), index=mts.index, columns=[mts.name]), mts


class RemoveYear(ITrends):

    def remove_trends(self, mts):
        """从时间序列中提取周年项，和残差
        Args:
            mts ([type]): [description]
        Returns:
            [type]: [description]
        """

        def trend_of_ts(ts):
            length = len(ts)
            x = np.array(list(range(length))).reshape((length, 1))
            sinx = np.sin(x * np.pi * 2 / 365 / 2)
            cosx = np.cos(x * np.pi * 2 / 365 / 2)
            sin2x = np.sin(2 * x * np.pi * 2 / 365 / 2)
            cos2x = np.cos(2 * x * np.pi * 2 / 365 / 2)
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


class Filter:
    def __init__(self, filter_method=IQR(), trends=RemoveYear()):
        self.filter_method = filter_method
        self.trends = trends

    def filter(self, ts):
        trends, noise = self.trends.remove_trends(ts)
        noise_remove = self.filter_method.filter(noise)
        trends_remove = trends.loc[noise_remove.index]
        return trends_remove + noise_remove
