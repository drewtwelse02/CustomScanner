import requests
import os
from datetime import date, timedelta,datetime
class Session:
    def __init__(self):
        self.historical_data_url = "https://api.tradier.com/v1/markets/history"
        self.session_auth_url    = "https://api.tradier.com/v1/markets/events/session"
        self.tradier_url         = 'https://api.tradier.com/v1/markets/events/session'
        self.api_token           =  os.environ.get('TRADIER_TOKEN')
        try :
            response = requests.post(self.tradier_url,
                data={},
                headers={'Authorization': 'Bearer '+self.api_token, 'Accept': 'application/json'}
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
        yt_daily_resp = requests.get(self.historical_data_url,
        params= {'symbol': str(ticker), 'interval': 'daily', 'start': str(date.today()- timedelta(days=1)), 'end': date.today(), 'session_filter': 'all'},
        headers={'Authorization': 'Bearer '+ self.api_token, 'Accept': 'application/json'})
        json_yt_daily_resp = yt_daily_resp.json()
        #print(json_yt_daily_resp.status_code)
        return json_yt_daily_resp
    
