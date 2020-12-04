"""

"""

import glob
import asyncio 


def find_years(site):
    for name in glob.iglob('data/'+site+'*'):
        print(name)

def find_days(site, year):
    pass

def write_data(site, years_data):
    pass

def get_day_data(site, year, day):
    pass

async def get_year_data(site, year):
    days = find_days(site,year)
    days_tasks = []
    for day in days:
        days_tasks.append(asyncio.create_task(get_day_data(site,year,day)))
    days_data = []
    for task in days_tasks:
        days_data.append(await days_tasks)
    return days_data  

async def all2one(site):
    years = find_years(site)
    years_tasks = []
    for year in years:
        years_tasks.append(asyncio.create_task(get_year_data(site,year)))
    years_data = []
    for task in years_tasks:
        years_data.append(await years_tasks)
    write_data(site, years_data)

async def main():
    # sites = pd.read_csv("./data/sites.csv")
    sites = open("./data/sites.csv")
    # print(sites.head())
    tasks = []
    for site in sites.readlines():
        tasks.append(asyncio.create_task(all2one(site)))
        # break
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())