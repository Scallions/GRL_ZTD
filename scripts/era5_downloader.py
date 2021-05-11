import cdsapi
# import asyncio
import multiprocessing
import os
from calendar import monthrange
import requests
response = requests.get(url='', verify=False)

def get_data_in(year, month, day):
    if not os.path.exists(f"data/era5/{year}/"):
        os.makedirs(f"data/era5/{year}/")
    # 判断是否已经下载过 文件已经存在且大于100M
    if os.path.exists(f'data/era5/{year}/era5_{year}_{month}_{day}.nc') and os.path.getsize(f'data/era5/{year}/era5_{year}_{month}_{day}.nc')/float(1024*1024) > 100:
        return
    c = cdsapi.Client(quiet=True)
    c.retrieve(
        'reanalysis-era5-pressure-levels',
        {
            'product_type': 'reanalysis',
            'format': 'netcdf',
            'variable': [
                'geopotential', 'relative_humidity', 'temperature',
            ],
            'pressure_level': [
                '1', '2', '3',
                '5', '7', '10',
                '20', '30', '50',
                '70', '100', '125',
                '150', '175', '200',
                '225', '250', '300',
                '350', '400', '450',
                '500', '550', '600',
                '650', '700', '750',
                '775', '800', '825',
                '850', '875', '900',
                '925', '950', '975',
                '1000',
            ],
            'year': year,
            'month': month,
            'day': day,
            'time': [
                '00:00', '01:00', '02:00',
                '03:00', '04:00', '05:00',
                '06:00', '07:00', '08:00',
                '09:00', '10:00', '11:00',
                '12:00', '13:00', '14:00',
                '15:00', '16:00', '17:00',
                '18:00', '19:00', '20:00',
                '21:00', '22:00', '23:00',
            ],
            'area': [
                85, -75, 55,
                -10,
            ],
        },
        f'data/era5/{year}/era5_{year}_{month}_{day}.nc')

def get_year_month(year, month):
    for day in range(1,monthrange(year,month)[1]+1):
        get_data_in(year, month, day)

def get_year(year):
    for month in range(1,13):
        get_year_month(year, month)

def main():
    # s1 = asyncio.Semaphore(5)
    # async with s1:
    pool = multiprocessing.Pool(processes=6)
    for year in range(2015,2020):
        pool.apply_async(get_year, args = (year,))
    pool.close()
    pool.join()

if __name__ == "__main__":
    main()

