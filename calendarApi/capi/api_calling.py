from __future__ import print_function
import datetime   
import pytz
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from django.core.files import File

#from capi.models import Availabledata

import json
    
def insertevents(start_time,end_time,email):
    start_time=start_time.isoformat()
    end_time=end_time.isoformat()
    
    # with open('client_secret.json', 'w') as f:
    #     myfile = File(f)
    #     myfile.write('{"installed":{"client_id":"1011984601039-uk1ell4orsc4b6hjgui3fvtp18u67nbc.apps.googleusercontent.com","project_id":"calenderapi-246115","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"RKUFLZQTdbep-pCeuOqGwI26","redirect_uris":["urn:ietf:wg:oauth:2.0:oob","http://localhost"]}}')
   
    scopes = ['https://www.googleapis.com/auth/calendar']
    # flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes=scopes)
    # credentials = flow.run_console()
    # pickle.dump(credentials, open("token.pkl", "wb"))
    credentials = pickle.load(open("token.pkl", "rb"))
    service = build("calendar", "v3", credentials=credentials)

    event = {
        'summary': 'Meeting Sceduled',
        'description': 'Time for work.',
        'start': {
            'dateTime': start_time,
            "TimeZone": "Asia/Kolkata", 
        },
        'end': {
            'dateTime': end_time,
            "TimeZone": "Asia/Kolkata",
            
        },
        
        'attendees': [
            {'email': email},
        ],
        }

    event = service.events().insert(calendarId='primary', body=event).execute()
    return event
        
    
    
    
    
    
    
    
    
    
    
    
    
