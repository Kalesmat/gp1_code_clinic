import datetime
from datetime import timedelta

def view_open_bookings(service):
    '''Function to get the next 7 days events'''
    # Call the Calendar API
    now = datetime.datetime.utcnow()
    end_time = now + timedelta(days=7)
    end_time = end_time.isoformat() + 'Z' # 'Z' indicates UTC time
    now = now.isoformat() + 'Z' # 'Z' indicates UTC time
    
    print('Getting the upcoming events for the next 7 days')
    events_result = service.events().list(calendarId='codeclinic.team14@gmail.com', timeMin=now,
                                        timeMax=end_time, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        if len(events['attendees']) > 2:
            pass
        else:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'], event['eventID'])


    # return avail_slots
