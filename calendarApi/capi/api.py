from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle


def assigndata():

    def insertEvent():
    # with open('credentials.json', 'w') as f:
    #     myfile = File(f)
    #     myfile.write('{"installed":{"client_id":"1011984601039-uk1ell4orsc4b6hjgui3fvtp18u67nbc.apps.googleusercontent.com","project_id":"calenderapi-246115","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"RKUFLZQTdbep-pCeuOqGwI26","redirect_uris":["urn:ietf:wg:oauth:2.0:oob","http://localhost"]}}')
    
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    event = {
    'summary': 'Google I/O 2015',
    'location': '800 Howard St., San Francisco, CA 94103',
    'description': 'A chance to hear more about Google\'s developer products.',
    'start': {
        'dateTime': '2019-07-28T09:00:00-07:00',
        
    },
    'end': {
        'dateTime': '2019-07-29T17:00:00-07:00',
        
    },
    
    'attendees': [
        {'email': 'lpage@example.com'},
        {'email': 'sbrin@example.com'},
    ],
    'reminders': {
        'useDefault': False,
        'overrides': [
        {'method': 'email', 'minutes': 24 * 60},
        {'method': 'popup', 'minutes': 10},
        ],
    },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    return event