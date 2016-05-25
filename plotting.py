import http.client
import json
import requests
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.tools as tls
import time
from datetime import datetime, timedelta

DEVICEIDS = ["FriskPI03", "FriskPI05"]
TIMESHIFT = 2


def create_traces(sensorid):
    
    conn = http.client.HTTPSConnection("friskbybergen-1d96.restdb.io")
    headers = {
        'content-type': "application/json",
        'apikey': "somekey",
        'cache-control': "no-cache",
        }

    # get the data for a specific device
    conn.request("GET", "/rest/posts?q=%7B%22deviceid%22%3A%20%22{}%22%7D".format(sensorid), headers=headers)
    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))

    datadict = []
    for i in data:
        datadict.append({'ts':i['timestamp'],'pm10':i['data']['PM10'],'pm25':i['data']['PM25']})

    df = pd.DataFrame().from_dict(datadict)

    df = pd.DataFrame(datadict)
    df['time'] = pd.to_datetime(df['ts'])
    df.index = df['time']

    df.index = df.index + +timedelta(hours=TIMESHIFT)
    df = df.resample('10Min')

    trace1 = go.Scatter( x=df.index,
                         y=df['pm10'],
                         name="{} - PM10".format(sensorid)  )
    trace2 = go.Scatter( x=df.index,
                         y=df['pm25'],
                         name="{} - PM25".format(sensorid)  )
    return (trace1,trace2)


#sign in to plotly
py.sign_in('someuser', 'somekey')

data = []
for device in DEVICEIDS:
    (trace1,trace2)= create_traces(device)
    data.append(trace1)
    data.append(trace2)
url = py.plot(data, filename='friskby-time-series')

