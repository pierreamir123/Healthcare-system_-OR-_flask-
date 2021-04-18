from __future__ import print_function
from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools


def sync_cal(message,st,et,y,m,d):
    SCOPES = 'https://www.googleapis.com/auth/calendar'
    store = file.Storage('storage.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)
    GCAL = discovery.build('calendar', 'v3', http=creds.authorize(Http()))
    DAY = str(d)
    MONTH = str(m) 
    YEAR = str(y)
    OP = message
    ENDH = str(et)
    START = str(st)
    GMT_OFF = '+02:00'   
    dataS= (YEAR,MONTH,DAY,START,GMT_OFF)
    dataM= (YEAR,MONTH,DAY,ENDH,GMT_OFF)   # PDT/MST/GMT-7
    EVENT = {
        'summary': OP,
        'start':  {'dateTime': '%s-%s-%sT%s:00:00%s' % dataS},
        'end':    {'dateTime': '%s-%s-%sT%s:00:00%s'% dataM},
        'attendees': [
            {'email': 'friend1@example.com'},
            {'email': 'friend2@example.com'},
        ],
    }

    e = GCAL.events().insert(calendarId='primary',
            sendNotifications=True, body=EVENT).execute()

    print('''*** %r event added:
        Start: %s
        End:   %s''' % (e['summary'].encode('utf-8'),
            e['start']['dateTime'], e['end']['dateTime']))

