"""Generate urls to download ztd product in greenland
"""
# import pandas as pd 
import asyncio
import requests_async as requests
import re
from bs4 import BeautifulSoup
import os

async def get_ztd_list(url,site):
    urls = []
    print("start get ", url)
    i = 0
    while True:
        i+=1
        if i > 10 :
            print("url maybe not correct:",url)
            break
        try:
            rep = await requests.get(url)
            if rep.status_code == 200:
                break 
            elif rep.status_code == 404:
                print("url not found ", url)
                break
            else:
                await asyncio.sleep(1)
        except:
            await asyncio.sleep(1)
            continue
    # matchs = re.findall(f"{site}\.\d4\.trop\.zip", rep.text)
    # print(rep.text)
    soup = BeautifulSoup(rep.text, 'html.parser')
    for file in soup.find_all(text=re.compile("zip")):
        urls.append(url+"/" + file)
    print("end get ", url)
    return urls

async def download_file(url):
    print("start download ", url)
    file = url.split("/")[-1]
    file = "./data/" + file
    if os.path.exists(file):
        print("end download file exist", url)
        return 
    i = 0
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
                await asyncio.sleep(1)
            if i > 10 :
                print("url maybe not correct:",url)
                break
        except:
            await asyncio.sleep(1)
            continue
    with open(file, "wb") as code:
        code.write(rep.content)
    print("end download ", url)


async def crawl_page(site):
    base_url = "http://geodesy.unr.edu/gps_timeseries/trop/"
    url = base_url + site.strip()
    print("start crawl ", url)
    urls = await asyncio.create_task(get_ztd_list(url,site))
    tasks = []
    for url_ in urls:
        tasks.append(asyncio.create_task(download_file(url_)))
    await asyncio.gather(*tasks)
    print("end crawl ", url)

async def main():
    # sites = pd.read_csv("./data/sites.csv")
    sites = open("./data/sites.csv")
    # print(sites.head())
    tasks = []
    for site in sites.readlines():
        tasks.append(asyncio.create_task(crawl_page(site)))
        # break
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())