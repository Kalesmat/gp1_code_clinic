import datetime
from datetime import timedelta

def view_open_bookings(service):
    '''Function to get the next 7 days events'''
    # Call the Calendar API
 
    now = datetime.datetime.utcnow()
    end_time = now + timedelta(days=7)
    end_time = end_time.isoformat() + 'Z' # 'Z' indicates UTC time
    now = now.isoformat() + 'Z' # 'Z' indicates UTC time
    events_result = service.events().list(
       calendarId='codeclinic.team14@gmail.com', timeMin=now,
       timeMax=end_time, singleEvents=True,maxAttendees=1,
       orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
       print('No upcoming events found.')
    for event in events:
       start = event['start'].get('dateTime') #, event['start'].get('date')
       print(start.strip("T12:00:00+02:00"), event['summary'], event['id'], event['creator'])

  
