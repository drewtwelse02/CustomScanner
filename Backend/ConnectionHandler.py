import os 
import asyncio
import websockets
import Session
import requests
from datetime import date, timedelta
import json

class ConnectionHandler :
    def __init__(self):
        self.historical_data_url = "https://api.tradier.com/v1/markets/history"
        #Get Market Session 
        self.session_id  = Session.Session().get_session_id()
        #asyncio(self.LaunchScanner())

    async def message_handler(self,websocket):
        async for message in websocket:
            await self.LaunchScanner()
    async def setup(self):
        async with websockets.serve(self.message_handler, "localhost", 3001):
            await asyncio.Future()  # run forever
    async def LaunchScanner (self):
            uri = "wss://ws.tradier.com/v1/markets/events"
            async with websockets.connect(uri, ssl=True, compression=None) as websocket:
                payload = '{"symbols": ["AAPL","GOOGL","RDDT","MSTR","MARA","COIN","MU","QCOM","AMD","AVGO","NVDL","SMCI","TSLA","RIVN","WFC","GS","BOFA","AXP","MS","JPM","FDX","UPS","AMZN"], "sessionid": "'+ self.session_id +'", "filter": ["trade"], "linebreak": true}'
                await websocket.send(payload)
                async for ticker in websocket:
                     # Launch PDL Scanner 
                    await self.pdl_scan(json.loads(ticker))
                    #print((json.loads(ticker))['symbol'])
    async def pdl_scan(self,ticker):
        # Look for Potential Prior Bar Low Break on Big Caps
        # Get Previous Day OCHL data 
        yt_date = date.today()-timedelta(days=1)
        try: 
            pd = requests.get(self.historical_data_url,
                        params={'symbol': ticker['symbol'], 'interval': 'daily', 'start': yt_date, 'end': yt_date, 'session_filter': 'open'},
                        headers={'Authorization': 'Bearer '+ os.environ.get('TRADIER_TOKEN'), 'Accept': 'application/json'} )
            pd_json = pd.json()
            current_stock_price = float(ticker['price'])
            yt_low              = float(pd_json["history"]['day']['low'])
            print(yt_low)
            #Check if the stock price is less than 200 and currently $1 away from the PDL, then Alert
            if ( current_stock_price <= 200 and (current_stock_price - yt_low) <= 1):
                print (f"Send Alert (1 + ) - {ticker['symbol']}")
            elif (current_stock_price > 200 and  current_stock_price < 400 and (current_stock_price - yt_low) <= 1.5 ):
                print (f"Send Alert (200 + ) - {ticker['symbol']}")
            #SMCI AVGO ETC 
            elif(current_stock_price > 400 and (current_stock_price - yt_low) <= 5 and (current_stock_price - yt_low) > 0):
                #print(ticker)
                print (f"Send Alert (400+) - {ticker['symbol']}")	      
        except Exception as error :
            #print (f"Error Occured while fetching daily data for  {ticker['symbol']}")
            print ("Error Occured while fetching daily data for", error)
        
        

    