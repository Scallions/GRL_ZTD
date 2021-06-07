import asyncio
import requests_async as requests
import os
import re

"""
需要提取信息
- 观测时间
- pw 
"""


def load_grl_sites():
    """Find sites in Greenland

    Returns:
        [site_info]: list of sites info
    """
    sites_file = "radio/wyoming/radiosonde-station-list.txt"
    # 后5个数字是测站代码
    sites_list = []
    with open(sites_file,'r') as f:
        for line in f.readlines():
            site_num = line[6:11]
            lon = float(line[22:30])
            lat = float(line[12:20])
            start = line[72:76]
            end = line[77:81]
            if 55 < lat < 85 and -75 < lon < -10:
                print(f"{site_num}: {lat:.2f}, {lon:.2f}")
                sites_list.append(f"{site_num} {lat} {lon} {start} {end}")
    print(len(sites_list))
    with open("temp/wyoming_sites.csv","w") as f:
        for site in sites_list:
            f.write(site+"\n")

def read_sites():
    """read site meta data from csv file

    Returns:
        [site_metadata]: metadata of radio sites
    """
    sites = []
    with open("temp/wyoming_sites.csv", "r") as f:
        for line in f.readlines():
            data = line.split()
            sites.append([data[0],data[-2], data[-1]])
    return sites



async def download_file(url, site, year, month, day):
    print("start download ", url)
    path = f"./radio/wyoming/{site}/{year}"
    file = f"./radio/wyoming/{site}/{year}/{month}-{day}.txt"
    if not os.path.exists(path):
        os.makedirs(path)
    if os.path.exists(file) and os.path.getsize(file) > 5000:
        print("end download file exist", url)
        return 
    i = 0
    rep = None
    while True:
        i+=1
        if i > 10 :
            print("url maybe not correct:",url)
            break
        try:
            rep = await requests.get(url)
            if rep.status_code == 200:
                break 
            elif rep.status_code == 400:
                print("url not found ", url)
                break 
            else:
                await asyncio.sleep(5)
            if i > 20 :
                print("url maybe not correct:",url)
                break
        except:
            await asyncio.sleep(5)
            continue
    if rep is None:
        print("NO data", url)
        return
    with open(file, "wb") as code:
        # 提取数据
        datas = extra_datas(rep.content)
        code.write(datas.encode())
    if(os.path.getsize(file) < 1000):
        os.remove(file)
    print("end download ", url)

def extra_datas(rep):
    data_re = re.compile(r"<PRE>(.*?)</PRE>", re.DOTALL)
    date_re = re.compile(r"Observation time: (\d+/\d+)")
    res = data_re.findall(rep.decode())
    datas = ""
    for i in range(len(res)//2):
        datas += date_re.findall(res[2*i+1])[0]
        datas += res[2*i]
    return datas

async def get_data_in(site,year,month,day):
    base_url = f'http://weather.uwyo.edu/cgi-bin/sounding?region=np&TYPE=TEXT%3ALIST&YEAR={year}&MONTH={month:02d}&FROM={day:02d}00&TO={day:02d}23&STNM={site}'
    await download_file(base_url, site, year, month, day)

async def get_year_data(site, year):
    for mon in range(1,13):
        tasks = []
        s1 = asyncio.Semaphore(2)
        async with s1:
            for day in range(1,32):
                tasks.append(asyncio.create_task(get_data_in(site,year, mon, day)))
            await asyncio.gather(*tasks)

async def get_site_data(site):
    start = int(site[-2])
    end = int(site[-1])
    tasks = []
    s1 = asyncio.Semaphore(2)
    async with s1:
        # for year in range(start,end+1):
        for year in range(2015, 2021):
            tasks.append(asyncio.create_task(get_year_data(site[0],year)))
        await asyncio.gather(*tasks)

async def main():
    sites = read_sites()
    tasks = []
    s1 = asyncio.Semaphore(2)
    async with s1:
        for site in sites:
            tasks.append(asyncio.create_task(get_site_data(site)))
        await asyncio.gather(*tasks) 

if __name__ == "__main__":
    # load_grl_sites()
    # with open("temp/sites.csv","w") as f:
        # for site in a:
            # f.write(site+"\n")
    asyncio.run(main())