import pandas as pd
import matplotlib.pyplot as plt
# plt.style.use('seaborn-whitegrid')
from scipy import stats
import numpy as np
from datetime import timedelta
from scipy.stats import gaussian_kde


filename = 'loads2.csv'
df = pd.read_csv(filename)

df['posted_date'] = pd.to_datetime(df['modified_date'], format='%Y-%m-%d %H:%M:%S')
df['start_time'] = pd.to_datetime(df['earliest_availability'], format='%Y-%m-%d %H:%M:%S')
df['end_time'] = pd.to_datetime(df['latest_availability'], format='%Y-%m-%d %H:%M:%S')

df = df.drop(['modified_date', 'earliest_availability', 'latest_availability'], axis=1)

df = df.sort_values(by='collected_timestamp')
df = df.drop_duplicates(subset=['load_id'], keep='last')
# print(df)

# df['cost_per_mile'] = df['price'] / df['mileage']

# df['from_to'] = df['from'] + '---' + df['to']
df['from-to-start_time'] = df['origin'] + '---' + df['destination'] + '---' + df['start_time'].dt.strftime("%d-%b-%Y %H:%M:%S")

df = df[df['rate_per_mile'] > 3.5]
df = df[df['rate_per_mile'] < 10]
# df = df[df['mileage'] > 300]

df = df[df['mileage'] > 900]
df = df[df['mileage'] < 1200]


print('RATE_PER_MILE')
print(df['rate_per_mile'].describe())
print()

# print('RATE')
# print(df['rate'].describe())
# print()

print('MILEAGE')
print(df['mileage'].describe())
print()

print('TIME_DIFF')
time_diff = df['end_time'] - df['posted_date']
df['time_diff'] = time_diff
x = df['time_diff'] / np.timedelta64(1, 'h')
print(x.describe())


plt.hist(df['mileage'], bins=50)
plt.show()

plt.hist(df['rate_per_mile'], bins=100)
plt.show()

# plt.hist(df['rate'], bins=100)
# plt.show()

# ### SCATTER
# x = df['mileage']
# y = df['rate_per_mile']

# xy = np.vstack([x,y])
# z = gaussian_kde(xy)(xy)

# plt.scatter(x, y, c=z, s=100)
# plt.show()

# ### SCATTER
# x = df['mileage']
# y = df['rate']

# xy = np.vstack([x,y])
# z = gaussian_kde(xy)(xy)

# plt.scatter(x, y, c=z, s=100)
# plt.show()


x = df['time_diff'] / np.timedelta64(1, 'h')
plt.hist(x, bins=200)
plt.show()


### SCATTER
x = df['time_diff'] / np.timedelta64(1, 'h')
y = df['rate_per_mile']

xy = np.vstack([x,y])
z = gaussian_kde(xy)(xy)

plt.scatter(x, y, c=z, s=100)
plt.show()
