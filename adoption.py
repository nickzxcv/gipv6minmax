import json
import collections
import requests
import re
import matplotlib.pyplot as plt
from datetime import date


adoption_js = requests.get('https://www.google.com/intl/en_ALL/ipv6/statistics/data/adoption.js')
adoption_json = re.search('var googleIPv6AdoptionData = (\[.+\]);', adoption_js.text, re.DOTALL).group(1)

data=json.loads(adoption_json)

# each week starts as an empty list
weeks=collections.defaultdict(list)
for day_data in data:
    year=day_data[0]
    month=day_data[1]+1
    day=day_data[2]
    ipv6_traffic=day_data[3]
    thisdate=date(year, month, day)
    year=thisdate.isocalendar()[0]
    week=thisdate.isocalendar()[1]
    # each day gets converted to its week and data added to weeks list
    weeks[date.fromisocalendar(year, week, 1)].append(ipv6_traffic)

# initialize lists to plot
week_plot=list()
low_plot=list()
high_plot=list()
range_plot=list()
# find the range, high, and low values for each week
for week, values in weeks.items():
    high=sorted(values)[-1]
    low=sorted(values)[0]
    high_plot.append(high)
    low_plot.append(low)
    range_plot.append(high-low)
    week_plot.append(week)

plt.plot(week_plot, high_plot)
plt.plot(week_plot, low_plot)
plt.plot(week_plot, range_plot)

plt.savefig('adoption.svg')
