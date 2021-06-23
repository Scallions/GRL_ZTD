# 预处理Wyoming数据 输出每次观测的，经纬度，椭球高，地表温度
import os
import numpy as np
import pandas as pd
import re

from tools import *
import multiprocessing
from io import StringIO

from loguru import logger

def text2ob(obt):
    lines = obt.split("\n")
    date = lines[0]
    data = lines[2:3] + lines[5:]
    with StringIO("\n".join(data)) as f:
        df = pd.read_csv(f, sep=r"\s+")

    # 对缺失值进行处理 TODO(处理缺失值)
    df = df.fillna(df.interpolate(method='linear'))
    df = df.dropna()

    ob = {'date': date, 'temp': df['TEMP'], 'rh': df['RELH'], 'pres': df['PRES'], 'gph': df['HGHT']}
    return ob


def split_obts(obts):
    spliter = re.compile(r"\d{6}/\d{4}")
    dates = spliter.findall(obts)
    obts = spliter.split(obts)[1:]
    return (dates[i]+obts[i] for i in range(len(dates)))

def read_obs(site):
    site_name = site[0]
    start = int(site[-2])
    end = int(site[-1])
    obs = []
    for year in range(2015, 2021):
        for mon in range(1, 13):
            for day in range(1, 32):
                filepath = f"./radio/wyoming/{site_name}/{year}/{mon}-{day}.txt"
                if os.path.exists(filepath):
                    with open(filepath) as f:
                        obts = f.read()
                    for obt in split_obts(obts):
                        ob = text2ob(obt)
                        obs.append(ob)
    return obs


def calc_ob(ob, lon, lat):
    temp = ob['temp'].to_numpy()
    rh = ob['rh'].to_numpy()
    pres = ob['pres'].to_numpy()
    gph = ob['gph'].to_numpy()
    date = ob['date']
    kt = temp + 273.15

    # compute var pres
    e_sat = 0.6112 * np.exp((17.2694 * temp) / (temp + 273.15 - 35.86))
    e_sat = e_sat * 10
    vap_pres = rh * e_sat / 100

    Tm_a = 0
    Tm_b = 0
    for x in range(0, len(pres) - 1):
        Tm_a = Tm_a + (gph[x + 1] - gph[x]) * vap_pres[x] / kt[x]
        Tm_b = Tm_b + (gph[x + 1] - gph[x]) * vap_pres[x] / (kt[x]) ** 2
    Tm = Tm_a / Tm_b
    return f"{date}, {lon:.4f}, {lat:.4f}, {gph[0]}, {kt[0]:.4f}, {Tm:.4f}\n"


def out_file(site):
    site_name = site[0]
    filepath = f"./radio/wyoming/{site_name}/tm.txt"
    return filepath


def calc_tm(site):
    """
    计算站点的tm时间序列，输出观测时间点的参数
    Args:
        site: 站点信息

    """
    logger.info(f"start calc tm of site: {site[0]}")
    lon = float(site[2])
    lat = float(site[1])
    obs = read_obs(site)
    res = ""
    for ob in obs:
        res += calc_ob(ob, lon, lat)

    out_fp = out_file(site)
    if len(res) < 10:
        return
    logger.info(f"out data site: {site[0]}, file: {out_fp}")
    with open(out_fp, "w") as f:
        f.write(res)


def main():
    sites = read_sites()
    pool = multiprocessing.Pool()

    for site in sites:
        pool.apply_async(func=calc_tm, args=(site,))

    pool.close()
    pool.join()

def test():
    for obt in split_obts(test_ob):
        ob = text2ob(obt)
        print(calc_ob(ob,58, -32))

if __name__ == '__main__':
    main()