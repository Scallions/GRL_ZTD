"""
过滤粗差
"""

import abc

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import *
from sklearn.ensemble import IsolationForest
from tqdm import tqdm
import seaborn as sns

import tools


class IFilterMethod(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def filter(self):
        pass

    @abc.abstractmethod
    def filter_rate(self):
        pass


class KMeans(IFilterMethod):
    def __init__(self, ts):
        self.ts = ts

    def filter(self):
        pass

    def filter_rate(self):
        pass


class IQR(IFilterMethod):

    def filter(self):
        pass

    def filter_rate(self):
        pass


class ITrends(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def remove_trends(self):
        pass


class NoRemove(ITrends):
    def remove_trends(self):
        """
        不做任何移除
        Returns:

        """
        return self.ts


class RemoveYear(ITrends):
    def remove_trends(self):
        """
        移除周年项
        Returns:

        """
        pass


class Filter:
    def __init__(self, filter_method, trends):
        self.filter_method = filter_method
        self.trends = trends

    def filter(self, ts):
        trends, noise = self.trends.remove_trends(ts)
        noise_remove = self.filter.filter(noise)
        trends_remove = trends.iloc[noise_remove.index]
        return trends_remove + noise_remove
