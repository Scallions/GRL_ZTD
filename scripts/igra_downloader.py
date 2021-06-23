import asyncio
import requests_async as requests
import os

POR_OR_Y2D = True # True: POR False: Y2D POR: All period Y2D: 2018~Now
base_url = "https://www1.ncdc.noaa.gov/pub/data/igra/data/"

def load_grl_sites():
    """Find sites in Greenland

    Returns:
        [site_info]: list of sites info
    """
    sites_file = "radio/igra2/igra2-station-list.txt"
    sites_list = []
    with open(sites_file,'r') as f:
        for line in f.readlines():
            data = line.split()
            lat, lon = float(data[1]), float(data[2])
            if 55 < lat < 85 and -75 < lon < -10:
                print(f"{data[0]}: {lat:.2f}, {lon:.2f}")
                sites_list.append(" ".join(data[:3]))
    return sites_list

async def down_site(site):
    print("start download ", site)
    url = f"https://www1.ncdc.noaa.gov/pub/data/igra/data/data-y2d/{site}-data-beg2018.txt.zip"
    url2 = f"https://www1.ncdc.noaa.gov/pub/data/igra/data/data-por/{site}-data.txt.zip"
    file = f"./radio/igra2/{site}.zip"
    file2 = f"./radio/igra2/{site}_2.zip"
    if os.path.exists(file):
        print("end download file exist", url)
        # return 
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


    if os.path.exists(file2):
        print("end download file exist", url2)
        return 
    i = 0
    while True:
        i+=1
        if i > 10 :
            print("url maybe not correct:",url2)
            break
        try:
            rep = await requests.get(url2)
            if rep.status_code == 200:
                break 
            elif rep.status_code == 400:
                print("url not found ", url2)
                break 
            else:
                await asyncio.sleep(1)
            if i > 10 :
                print("url maybe not correct:",url2)
                break
        except:
            await asyncio.sleep(1)
            continue
    with open(file2, "wb") as code:
        code.write(rep.content)
    print("end download ", url2)

async def main(sites):
    tasks = []
    for site in sites:
        tasks.append(asyncio.create_task(down_site(site)))
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    a = load_grl_sites()
    a = [aa.split()[0] for aa in a]
    with open("temp/igra2_sites.csv","w") as f:
        for site in a:
            f.write(site+"\n")
    asyncio.run(main(a))