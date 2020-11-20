import datetime

def view(service):
   
    '''This function displays the events that have been booked.'''

    page_token = None
    now = datetime.datetime.now().isoformat() + 'Z'
    n = 0
    while True:
        events = service.events().list(calendarId='primary', timeMin=now, pageToken=page_token).execute()
        for event in events['items']:
            try:
                summary =event['summary']
                
                start=event['start']
                end= event['end']
                status= event['status']
                id= event['id']

                n+=1
                print(f'You have a {summary} session event Id {id} at {start} till {end} ')
                print(f'Status: {status}')

            except KeyError:
        
                break
        if n < 1:
            print('You have not volunteered')
        page_token = events.get('nextPageToken')
        if not page_token:
            break


