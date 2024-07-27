import requests
import os
class Session:
    def __init__(self):
        self.historical_data_url = "https://api.tradier.com/v1/markets/history"
        self.session_auth_url    = "https://api.tradier.com/v1/markets/events/session"
        self.tradier_url         = 'https://api.tradier.com/v1/markets/events/session'
        try :
            response = requests.post(self.tradier_url,
                data={},
                headers={'Authorization': 'Bearer '+ str(os.environ.get('TRADIER_TOKEN')), 'Accept': 'application/json'}
            )
            json_response = response.json()
            self.session_id   = json_response['stream']['sessionid']
        except Exception as error:
            print("Unable to Create market Session ")
            exit()
            
    
    def get_session_id(self):
       return self.session_id
    
