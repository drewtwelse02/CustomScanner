import os 
import pytz
from datetime import date, timedelta,datetime
import json
from polygon import RESTClient
import statistics

class StdDev:
    def __init__(self):
        self.historical_data_url = "https://api.tradier.com/v1/markets/history"
        self.session_auth_url    = "https://api.tradier.com/v1/markets/events/session"
        #self.Stock_List = ["QQQ","SPY","META","RDDT","MSTR","MARA","COIN","MU","QCOM","AMD","AVGO","NVDL","SMCI","TSLA","RIVN","WFC","GS","BOFA","AXP","MS","JPM","FDX","UPS","AMZN"]
        # Polygon API setup 
        self.client = RESTClient(api_key=os.environ['POLY_API_KEY'])
    def convert_date(ts):
        timestamp = ts/1000.0
        date_obj = datetime.fromtimestamp(timestamp).astimezone(pytz.timezone('America/Chicago'))
        # Filter By time to Avoid sending Alerts at bad time of the day 
        # From 8:00 AM to 16:00 PM
        if date_obj.hour < 15 and date_obj.hour >= 8 : 
            formated_date = date_obj.strftime('%Y-%m-%d %H:%M:%S  %Z %z')
            return str(formated_date)
    def runstd_dev(self,ticker):

        td_date = (date.today()-timedelta(days=1))  
        chk_date = date.today()
     
        # Calculate the Std deviation of the last 10 days of 2mns bar data      
        yt_date = td_date -timedelta(days=1) # Using YT date as stop date
        aggs = [] 
        std_dev = 0
        #Get Daily data 10 days prior yesterday 
        for a in self.client.list_aggs(ticker=ticker['symbol'], multiplier=2, timespan="minute", from_=str(yt_date-timedelta(days=10)), to=str(yt_date), limit=50000):
        # Store each 2mns volume bar in an []
            aggs.append(a.volume)
        std_dev = statistics.stdev(aggs)
        print(std_dev)
        # Compare the  Std Dev Found with the current 
        #print(f"Standard Deviation of sample is {std_dev}")
        # Compare each 2mns bar of data with the std dev 
        # try :
        #     for d in self.client.list_aggs(ticker=ticker['symbol'], multiplier=2, timespan="minute", from_=str(chk_date), to=str(chk_date), limit=50000):
        #         if (d.volume > 1.5* std_dev ):
        #             converted_date = self.convert_date(d.timestamp)
        #             if converted_date is not None:
        #                 print(f"{std_dev}- High std dev found {converted_date} ")
        # except Exception as error :
        #     # Weekends 
        #     w=1 # Dummy Var 

        td_date  = td_date-timedelta(days=1)
        chk_date = chk_date-timedelta(days=1)
        i = i+1

