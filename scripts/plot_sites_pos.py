import pygmt 
import pandas as pd

df = pd.read_csv("temp/igra2_sites.csv", header=None, sep=" ")
print(df.head())
print(df.shape)
fig = pygmt.Figure()

fig.basemap(region="-75/-10/55/86", projection="L-40/30/35/25/6i", frame=True)
fig.coast(shorelines=True, water="lightblue")
fig.plot(x=df.iloc[:,2],y=df.iloc[:,1], style="c0.1c", color="red", pen="black")


fig.savefig("figs/greenland.jpg")