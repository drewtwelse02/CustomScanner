import asyncio
import websockets
import requests
import os 
import json
import pytz
from datetime import date, timedelta,datetime

from polygon import RESTClient
import statistics

historical_data_url = "https://api.tradier.com/v1/markets/history"
session_auth_url    = "https://api.tradier.com/v1/markets/events/session"
Stock_List = ["AAPL","GOOGL","RDDT","MSTR","MARA","COIN","MU","QCOM","AMD","AVGO","NVDL","SMCI","TSLA","RIVN","WFC","GS","BOFA","AXP","MS","JPM","FDX","UPS","AMZN"]

# Create Market Session 
api_key = os.environ['TRADIER_API_KEY']

# Polygon API setup 
client = RESTClient(api_key=os.environ['POLY_API_KEY'])


def convert_date(ts):
    timestamp = ts/1000.0
    date_obj = datetime.fromtimestamp(timestamp).astimezone(pytz.timezone('America/Chicago'))
    # Filter By time to Avoid sending Alerts at bad time of the day 
    # From 8:00 AM to 16:00 PM
    if date_obj.hour < 15 and date_obj.hour >= 8 : 
        formated_date = date_obj.strftime('%Y-%m-%d %H:%M:%S  %Z %z')
        return str(formated_date)
    
def backtest(tickers):
    # Using the last 30 days of data, calculate the STD Dev of the last 10 days and compare it with the current 2mns bar
    i = 0
    td_date = (date.today()-timedelta(days=1))
    chk_date = date.today()
    while i < 30:    
        # Calculate the Std deviation of the last 10 days of 2mns bar data      
        td_date = td_date -timedelta(days=1)
        aggs = []
        std_dev = 0
        for a in client.list_aggs(ticker=tickers[12], multiplier=2, timespan="minute", from_=str(td_date-timedelta(days=10)), to=str(td_date), limit=50000):
            #print("Working")
            aggs.append(a.volume)
        std_dev = statistics.stdev(aggs)
        #print(f"Standard Deviation of sample is {std_dev}")
        # Compare each 2mns bar of data with the std dev 

        for d in client.list_aggs(ticker=tickers[0], multiplier=2, timespan="minute", from_=str(chk_date), to=str(chk_date), limit=50000):
            if (d.volume > 5* std_dev ):
                print(f"5x std dev found {convert_date(d.timestamp)} ")

        td_date  = td_date-timedelta(days=1)
        chk_date = chk_date-timedelta(days=1)
        i = i+1

#Connect to the web socket Server 
async def ws_connect(sl):
    uri = "wss://ws.tradier.com/v1/markets/events"
    async with websockets.connect(uri, ssl=True, compression=None) as websocket:
        payload = '{"symbols": ["AAPL","GOOGL","RDDT","MSTR","MARA","COIN","MU","QCOM","AMD","AVGO","NVDL","SMCI","TSLA","RIVN","WFC","GS","BOFA","AXP","MS","JPM","FDX","UPS","AMZN"], "sessionid": "'+ SESSION_ID +'", "filter": ["trade"], "linebreak": true}'
        await websocket.send(payload)
        async for ticker in websocket:
            print(f"<<< {ticker}")
            # Multiple Threads 
            #await scan(json.loads(ticker))

##asyncio.run(ws_connect(Stock_List))
backtest(Stock_List)