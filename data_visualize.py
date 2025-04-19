import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv('alldata.csv')
data.drop_duplicates(inplace=True)
data.replace('-', np.nan, inplace=True)
data.dropna(inplace=True)
tmp = data.loc[(data['SiteName']=='松山')]
print(tmp)
so2 = tmp['SO2'].to_list()
time = tmp['time'].to_list()
no2 = tmp['NO2'].to_list()
no = tmp['NO'].to_list()
nox = tmp['NOx'].to_list()
pm = tmp['PM2.5'].to_list()
aqi = tmp['AQI'].to_list()
co = tmp['CO'].to_list()
o3 = tmp['O3'].to_list()
pm10 = tmp['PM10'].to_list()
days = tmp['days'].to_list()

plt.figure()
plt.title('days')
plt.scatter(days, pm)

plt.figure()
plt.title('so2')
plt.scatter(so2, pm)

plt.figure()
plt.title('no2')
plt.scatter(no2, pm)

plt.figure()
plt.title('no')
plt.scatter(no, pm)

plt.figure()
plt.title('nox')
plt.scatter(nox, pm)

plt.figure()
plt.title('AQI')
plt.scatter(aqi, pm)

plt.figure()
plt.title('CO')
plt.scatter(co, pm)

plt.figure()
plt.title('O3')
plt.scatter(o3, pm)

plt.figure()
plt.title('PM10')
plt.scatter(pm10, pm)

plt.show()