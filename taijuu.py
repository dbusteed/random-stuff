from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd
import calendar
import re

df = pd.read_csv('taijuu.csv')

df = df[['Time of Measurement', 'Weight']]
df = df.rename(columns={'Time of Measurement': 'raw_date', 'Weight': 'weight'})

raw_dates = [d.split(' ') for d in df['raw_date']]

months = dict((v,k) for k,v in enumerate(calendar.month_abbr))

df['raw_date'] = [datetime(int(d[2]), months[d[0]], int(d[1][:-1])) for d in raw_dates]
df['weight'] = pd.Series(map(lambda x: re.sub(r'Lb', '', x), df['weight']), dtype='float')

raw_dates = df['raw_date']
start = raw_dates.iloc[-1]
end = raw_dates.iloc[0]

delta = end - start

dates = []

for i in range(delta.days + 1):
	dates.append(start + timedelta(days=i))
	
date_series = pd.Series(dates)
date_series.name = 'day'

df = pd.merge(left=df, right=date_series, how='right', left_on='raw_date', right_on='day')

df = df.drop(columns='raw_date')
df = df.sort_values(by=['day'])

df = df.interpolate(method='linear')

plt.xticks(rotation=45)

plt.plot(df['day'], df['weight'])

plt.show()
