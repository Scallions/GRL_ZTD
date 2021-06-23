import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from loguru import logger

sns.set_style('darkgrid')

test_fp = "../radio/wyoming/04339/tm.txt"


df = pd.read_csv(test_fp, header=None)
df[0] = pd.to_datetime(df[0], format="%y%m%d/%H%M")
# df.rei
print(df.head())

# df[5].plot()
plt.plot(df[0], df[4], label="Ts")
plt.plot(df[0], df[5], label="Tm")
plt.legend()
# sns.lineplot(df[0], df[5])
# sns.scatterplot(df[0], df[5])
plt.show()