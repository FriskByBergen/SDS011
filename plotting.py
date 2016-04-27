import http.client
import json
import requests
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.tools as tls
import time

DEVICEID1 = "FriskPI03"
DEVICEID2 = "FriskPI05"

#sign in to plotly
py.sign_in('plotly username', 'get your own')

conn = http.client.HTTPSConnection("friskbybergen-1d96.restdb.io")

headers = {
    'content-type': "application/json",
    'apikey': "571ff001c6dd47c4178ee222",
    'cache-control': "no-cache",
    }

# get the data for a specific device
conn.request("GET", "/rest/posts?q=%7B%22deviceid%22%3A%20%22{}%22%7D".format(DEVICEID1), headers=headers)
res = conn.getresponse()
data = json.loads(res.read().decode("utf-8"))

datadict = []
for i in data:
    datadict.append({'ts':i['timestamp'],'pm10':i['data']['PM10'],'pm25':i['data']['PM25']})

df = pd.DataFrame().from_dict(datadict)

df = pd.DataFrame(datadict)
df['time'] = pd.to_datetime(df['ts'])
df.index = df['time']
df = df.resample('10Min')

trace1 = go.Scatter( x=df.index,
                     y=df['pm10'],
                     name="{} - PM10".format(DEVICEID1)  )
trace2 = go.Scatter( x=df.index,
                     y=df['pm25'],
                     name="{} - PM25".format(DEVICEID1)  )

conn.request("GET", "/rest/posts?q=%7B%22deviceid%22%3A%20%22{}%22%7D".format(DEVICEID2), headers=headers)
res = conn.getresponse()
data = json.loads(res.read().decode("utf-8"))

datadict = []
for i in data:
    datadict.append({'ts':i['timestamp'],'pm10':i['data']['PM10'],'pm25':i['data']['PM25']})

df = pd.DataFrame().from_dict(datadict)

df = pd.DataFrame(datadict)
df['time'] = pd.to_datetime(df['ts'])
df.index = df['time']
df = df.resample('10Min')

trace3 = go.Scatter( x=df.index,
                     y=df['pm10'],
                     name="{} - PM10".format(DEVICEID2)  )
trace4 = go.Scatter( x=df.index,
                     y=df['pm25'],
                     name="{} - PM25".format(DEVICEID2)  )

data = [trace1,trace2,trace3, trace4]
url = py.plot(data, filename='pandas-time-series')
