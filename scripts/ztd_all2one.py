"""

"""

import glob
import asyncio 
import zipfile
import subprocess
import os
import os.path
import gzip
import shlex


def unzip_file(zip_src, dst_dir):
    r = zipfile.is_zipfile(zip_src)
    if r:     
        fz = zipfile.ZipFile(zip_src, 'r')
        for file in fz.namelist():
            fz.extract(file, dst_dir)       
    else:
        print('This is not zip')

def find_years(site):
    
    # file name AASI.2005.trop.zip
    years = []
    for name in glob.iglob('data/ztd/'+site+'/[0-9][0-9][0-9][0-9]'):
        # print(name)
        years.append(name.split('/')[-1])
        # 判断并解压文件
        files = glob.glob(name+'/*')
        if len(files) == 1 and files[0].endswith('.zip'):
            # 解压
            unzip_file(files[0],name+'/')

    years = sorted(years)
    return years

def find_days(site, year):
    days = []
    for name in glob.iglob('data/ztd/'+site+'/' + year+'/*'):
        # print(name)
        if not name.endswith('.gz'):
            continue
        days.append(name.split('.')[-3])
    days = sorted(days)
    return days

def write_data(site, years_data):
    outfile = f"data/ztd/{site}/all.txt"
    print(f"write {site} data to {outfile}")
    with open(outfile,"w") as f:
        f.write("".join(years_data))

def read_gzfile(file_path):
    '''
    dir_path: 压缩文件夹路径
    '''
    # 以文本形式读取压缩文件
    res = ""
    flag = False
    c = 0
    with gzip.open(file_path, 'rt') as f:
        for line in f.readlines():
            if "+TROP/SOLUTION" in line:
                flag = True
                continue 
            if "-TROP/SOLUTION" in line:
                return res
            if flag:
                if c > 0:
                    res += line
                c += 1


async def get_day_data(site, year, day):
    file = f"data/ztd/{site}/{year}/{site}.{year}.{day}.trop.gz"
    # cmd = f"zgrep -A1000 -m1 '^[+-]TROP/SOLUTION' {file}"
    # cmd1 = shlex.split(cmd)
    # cmd2 = shlex.split("tail -n+3")
    # cmd3 = shlex.split("head -n-2")

    # 异步 执行失败 不能 fork fork太多？
    # task = asyncio.create_subprocess_shell(
    #     cmd, stdout=asyncio.subprocess.PIPE
    # )
    # proc = await task
    # data = await proc.stdout.readlines()

    # 同步
    # task1 = subprocess.Popen(cmd1, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # task2 = subprocess.Popen(cmd2, shell=False, stdin=task1.stdout, stdout=subprocess.PIPE)
    # task3 = subprocess.Popen(cmd3, shell=False, stdin=task2.stdout, stdout=subprocess.PIPE)
    # data = task3.stdout.readlines()
    # data = [s.decode("ascii") for s in data]

    # python 读取gz文件
    text = read_gzfile(file)
    return text
    

async def get_year_data(site, year):
    print(f"start {site} {year}")
    days = find_days(site,year)
    days_tasks = []
    for day in days:
        days_tasks.append(asyncio.create_task(get_day_data(site,year,day)))
        # break
    days_data = []
    for task in days_tasks:
        days_data.append(await task)
    print(f"end {site} {year}")
    years_data = "".join(days_data)  
    filename = f"data/ztd/{site}/{year}/all.txt"
    with open(filename, "w") as f:
        f.write(years_data)
        print(f"wirte {site} {year} to {filename}")
    return years_data

async def all2one(site):
    print(f"start {site}")
    years = find_years(site)
    if len(years) == 0:
        print(f"end {site}")
        return
    years_tasks = []
    for year in years:
        years_tasks.append(asyncio.create_task(get_year_data(site,year)))
        # break
    years_data = []
    for task in years_tasks:
        years_data.append(await task)
    write_data(site, years_data)
    print(f"end {site}")

async def main():
    # sites = pd.read_csv("./data/sites.csv")
    sites = open("./data/ztd/sites.csv")
    # print(sites.head())
    tasks = []
    for site in sites.readlines():
        tasks.append(asyncio.create_task(all2one(site.strip())))
        # break
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())