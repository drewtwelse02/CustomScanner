import asyncio
import websockets
import requests
import os 
import json
from datetime import date, timedelta
from polygon import RESTClient
import statistics

historical_data_url = "https://api.tradier.com/v1/markets/history"
session_auth_url    = "https://api.tradier.com/v1/markets/events/session"
Stock_List = ["AAPL","GOOGL","RDDT","MSTR","MARA","COIN","MU","QCOM","AMD","AVGO","NVDL","SMCI","TSLA","RIVN","WFC","GS","BOFA","AXP","MS","JPM","FDX","UPS","AMZN"]

# Create Market Session 
api_key = os.environ['TRADIER_API_KEY']

# Polygon API setup 
client = RESTClient(api_key=os.environ['POLY_API_KEY'])



def backtest(tickers):
    # Using the last 30 days of data, calculate the STD Dev of the last 10 days and compare it with the current 2mns bar
    i = 0
    td_date = date.today()  
    aggs = []
    for a in client.list_aggs(ticker=tickers[0], multiplier=2, timespan="minute", from_=str(td_date-timedelta(days=10)), to=str(td_date), limit=50000):
        print("Working")
        aggs.append(a.volume)
    print("Standard Deviation of sample is % s "
                % (statistics.stdev(aggs)))


"""     while i < 30:    
        # Calculate the Std deviation of the last 10 days of 2mns bar data     

        # Go back 1 day prior to move the start date 
        td_date = td_date -timedelta(days=1)
        i = i+1 """

"""     
    try: 
        pd = requests.get(historical_data_url,
                      params={'symbol': tickers['symbol'], 'interval': 'daily', 'start': yt_date, 'end': date.today(), 'session_filter': 'open'},
                      headers={'Authorization': 'Bearer '+api_key, 'Accept': 'application/json'} )
 """
    

#Connect to the web socket Server 
async def ws_connect(sl):
    uri = "wss://ws.tradier.com/v1/markets/events"
    async with websockets.connect(uri, ssl=True, compression=None) as websocket:
        payload = '{"symbols": ["AAPL","GOOGL","RDDT","MSTR","MARA","COIN","MU","QCOM","AMD","AVGO","NVDL","SMCI","TSLA","RIVN","WFC","GS","BOFA","AXP","MS","JPM","FDX","UPS","AMZN"], "sessionid": "'+ SESSION_ID +'", "filter": ["trade"], "linebreak": true}'
        await websocket.send(payload)
        async for ticker in websocket:
            #print(f"<<< {ticker}")
            # Multiple Threads 
            await scan(json.loads(ticker))

##asyncio.run(ws_connect(Stock_List))
backtest(Stock_List)