import json
import collections
import requests
import re
from datetime import date

adoption_js = requests.get('https://www.google.com/intl/en_ALL/ipv6/statistics/data/adoption.js')
adoption_json = re.search('var googleIPv6AdoptionData = (\[.+\]);', adoption_js.text, re.DOTALL).group(1)

data=json.loads(adoption_json)

weeks=collections.defaultdict(list)
for day_data in data:
    year=day_data[0]
    month=day_data[1]+1
    day=day_data[2]
    ipv6_traffic=day_data[3]
    thisdate=date(year, month, day)
    year=thisdate.isocalendar()[0]
    week=thisdate.isocalendar()[1]
    weeks[date.fromisocalendar(year, week, 1)].append(ipv6_traffic)

for week, values in weeks.items():
    high=sorted(values)[-1]
    low=sorted(values)[0]
    range=high-low
    print("{},{},{},{}".format(week, low, high, range))
