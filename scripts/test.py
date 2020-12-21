import matplotlib.pyplot as plt 
import numpy as np 
import pandas as pd



filepath = "data/AASI/all.txt"

    
names=['Site', 'Epoch', 'TroTot', 'TroStd',"TrWet",'TgnTot', 'TgnStd', 'TgeTot', 'TgeStd',"WVapor","WVStd","MTem"]
df = pd.read_csv(filepath,header=None,sep="\s+",names=names)
df["Epoch"] = pd.to_datetime(df['Epoch'].str[:6], format='%y:%j') + \
    pd.to_timedelta(df['Epoch'].str[7:].astype(int), unit='s')
df = df.set_index("Epoch")
print(df.head())
print(df.tail())
plt.scatter(df.index, df["TroTot"],s=1)
plt.savefig("figs/test.png")