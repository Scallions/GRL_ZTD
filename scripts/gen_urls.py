# 生成 NOAA ncep 下载链接

types = ["rhum", "hgt", "air"]

for type in types:
    with open(f"{type}-urls.txt", "w") as f:
        for year in range(2015,2022):
            url = f"ftp://ftp2.psl.noaa.gov/Datasets/ncep.reanalysis2/pressure/{type}.{year}.nc"
            f.write(url+"\n")


