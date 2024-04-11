import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
from scipy import stats
import numpy as np
from datetime import timedelta


filename = 'loads.csv'
df = pd.read_csv(filename)

df['posted_date'] = pd.to_datetime(df['modified_date'], format='%Y-%m-%d %H:%M:%S')
df['start_time'] = pd.to_datetime(df['earliest_availability'], format='%Y-%m-%d %H:%M:%S')
df['end_time'] = pd.to_datetime(df['latest_availability'], format='%Y-%m-%d %H:%M:%S')

df = df.drop(['modified_date', 'earliest_availability', 'latest_availability'], axis=1)

df = df.sort_values(by='start_time')

# df['cost_per_mile'] = df['price'] / df['mileage']

# df['from_to'] = df['from'] + '---' + df['to']
df['from-to-start_time'] = df['origin'] + '---' + df['destination'] + '---' + df['start_time'].dt.strftime("%d-%b-%Y %H:%M:%S")

df = df[df['rate_per_mile'] > 4]
df = df[df['mileage'] > 300]

print('RATE_PER_MILE')
print(df['rate_per_mile'].describe())
print()

print('MILEAGE')
print(df['mileage'].describe())
print()

print('TIME_DIFF')
time_diff = df['end_time'] - df['posted_date']
df['time_diff'] = time_diff
print(time_diff.describe())


plt.hist(df['mileage'], bins=20)
plt.show()

plt.hist(df['end_time'].dt.hour, bins=23)
plt.show()