import asyncio

POR_OR_Y2D = True # True: POR False: Y2D POR: All period Y2D: 2018~Now
base_url = "https://www1.ncdc.noaa.gov/pub/data/igra/data/"

def load_grl_sites():
    """Find sites in Greenland

    Returns:
        [site_info]: list of sites info
    """
    sites_file = "radio/wyoming/radiosonde-station-list.txt"
    sites_list = []
    with open(sites_file,'r') as f:
        for line in f.readlines():
            data = line.split()
            lat, lon = float(data[1]), float(data[2])
            if 55 < lat < 85 and -75 < lon < -10:
                print(f"{data[0]}: {lat:.2f}, {lon:.2f}")
                sites_list.append(" ".join(data[:3]))
    return sites_list

async def main():
    pass 

if __name__ == "__main__":
    a = load_grl_sites()
    with open("temp/igra2_sites.csv","w") as f:
        for site in a:
            f.write(site+"\n")
    asyncio.run(main())