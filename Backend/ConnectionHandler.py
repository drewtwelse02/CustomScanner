import os 
import asyncio
import websockets
import Session
import requests
import pytz
import json
from datetime import date, timedelta,datetime
from Custom.PrintColor import info,error
from polygon import RESTClient
import statistics



class ConnectionHandler :
    def __init__(self):
        self.historical_data_url = "https://api.tradier.com/v1/markets/history"
        #Get Market Session from Tradier 
        self.session_id  = Session.Session().get_session_id()
        # Create new Client With Polygon 
        self.client = RESTClient(os.getenv("POLY_API_KEY"))

    async def message_handler(self,websocket):
        async for message in websocket:
            await self.LaunchScanners()
    async def setup(self):
        async with websockets.serve(self.message_handler, "localhost", 3001):
            await asyncio.Future()  # run forever
    async def LaunchScanners (self):
            uri = "wss://ws.tradier.com/v1/markets/events"
            async with websockets.connect(uri, ssl=True, compression=None) as websocket:
                payload = '{"symbols": ["AAPL","GOOGL","RDDT","MSTR","MARA","COIN","MU","QCOM","AMD","AVGO","NVDL","SMCI","TSLA","RIVN","WFC","GS","BOFA","AXP","MS","JPM","FDX","UPS","AMZN"], "sessionid": "'+ self.session_id +'", "filter": ["trade"], "linebreak": true}'
                await websocket.send(payload)
                async for ticker in websocket:
                    # Launch PDL Scanner 
                    #await self.pdl_scan(json.loads(ticker))
                    await self.std_dev_scan(json.loads(ticker))
    async def pdl_scan(self,ticker):
        # Look for Potential Prior Bar Low Break on Big Caps
        # Get Previous Day OCHL data
        yt_date = date.today()-timedelta(days=1)
        try: 
            pd = requests.get(self.historical_data_url,
                        params={'symbol': ticker['symbol'], 'interval': 'daily', 'start': "2024-07-25", 'end': "2024-07-25", 'session_filter': 'open'},
                        headers={'Authorization': 'Bearer '+ os.environ.get('TRADIER_TOKEN'), 'Accept': 'application/json'} )
            pd_json = pd.json()
            current_stock_price = float(ticker['price'])
            yt_low              = float(pd_json["history"]['day']['low'])
            info(yt_low)
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
            error("Error Occured while fetching daily data for", error)

    def std_dev_scan(self,tickers):
        # Using the last 30 days of data, calculate the STD Dev of the last 10 days and compare it with the current 2mns bar
        i = 0
        td_date = (date.today()-timedelta(days=1))
        info(td_date)
        chk_date = date.today()
        while i < 10:    
            # Calculate the Std deviation of the last 10 days of 2mns bar data      
            td_date = td_date -timedelta(days=1)
            aggs = [] 
            std_dev = 0
            #Get Daily data 10 days prior yesterday 
            for a in self.client.list_aggs(ticker=tickers[0], multiplier=2, timespan="minute", from_=str(td_date-timedelta(days=10)), to=str(td_date), limit=50000):
                # Store each 2mns volume bar in an []
                aggs.append(a.volume)
            std_dev = statistics.stdev(aggs)
            #print(f"Standard Deviation of sample is {std_dev}")
            # Compare each 2mns bar of data with the std dev 
            try :
                for d in self.client.list_aggs(ticker=tickers[0], multiplier=2, timespan="minute", from_=str(chk_date), to=str(chk_date), limit=50000):
                    if (d.volume > 1.5* std_dev ):
                        converted_date = self.convert_date(d.timestamp)
                        if converted_date is not None:
                            print(f"{std_dev}- High std dev found {converted_date} ")
            except Exception as error :
                # Weekends 
                w=1 # Dummy Var 
            td_date  = td_date-timedelta(days=1)
            chk_date = chk_date-timedelta(days=1)
            i = i+1
    def convert_date(self,ts):
        timestamp = ts/1000.0
        date_obj = datetime.fromtimestamp(timestamp).astimezone(pytz.timezone('America/Chicago'))
        # Filter By time to Avoid sending Alerts at bad time of the day 
        # From 8:00 AM to 16:00 PM
        if date_obj.hour < 15 and date_obj.hour >= 8 : 
            formated_date = date_obj.strftime('%Y-%m-%d %H:%M:%S  %Z %z')
            return str(formated_date)
            
            

        