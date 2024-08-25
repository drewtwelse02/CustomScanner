import requests
import os
from datetime import date, timedelta,datetime
from polygon import RESTClient
class Session:
    def __init__(self):
        self.historical_data_url = "https://api.tradier.com/v1/markets/history"
        self.session_auth_url    = "https://api.tradier.com/v1/markets/events/session"
        self.tradier_url         = 'https://api.tradier.com/v1/markets/events/session'
        self.tradier_api_token   =  os.environ.get('TRADIER_TOKEN')
        self.polygon_api_token   =  os.environ.get('POLY_API_KEY')
        self.poly_client         =  RESTClient(api_key=self.polygon_api_token)
        try :
            response = requests.post(self.tradier_url,
                data={},
                headers={'Authorization': 'Bearer '+self.tradier_api_token, 'Accept': 'application/json'}
            )
            json_response = response.json()
            self.session_id   = json_response['stream']['sessionid']
        except Exception as error:
            print("Unable to Create market Session ")
            exit()
            
    def get_session_id(self):
       return self.session_id
    def get_historical_data_url(self):
        return self.historical_data_url
    
    async def get_yt_daily_data(self,ticker):
        # by default the prior trading day should be one day back
        days_back = 1
        # Check to see if its sunday, to move 2 days prior (Friday to Today)
        if (date.today().isoweekday() == 7):
            days_back = 2 
        yt_daily_resp = requests.get(self.historical_data_url,
        params= {'symbol': str(ticker), 'interval': 'daily', 'start': str(date.today()- timedelta(days=days_back)), 'end': date.today(), 'session_filter': 'all'},
        headers={'Authorization': 'Bearer '+ self.tradier_api_token, 'Accept': 'application/json'})
        json_yt_daily_resp = yt_daily_resp.json()
        return json_yt_daily_resp
    def get_last_volume_bars (self,symbol):
        # List Aggregates (Bars)
        aggs = []
        for a in self.poly_client.list_aggs(ticker=symbol, multiplier=2, timespan="minute", from_=str(date.today()- timedelta(days=10)), to=str(date.today()- timedelta(days=1)), limit=50000):
            aggs.append(a.volume)
        return aggs

    
