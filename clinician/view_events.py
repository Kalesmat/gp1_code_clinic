import datetime


def view(service,myemail):
   
    '''This function displays the events that have been booked.'''
    
    page_token = None
    now = datetime.datetime.now().isoformat() + 'Z'
    n = 0
    while True:
        events = service.events().list(calendarId='primary', timeMin=now, pageToken=page_token).execute()
        for event in events['items']:
            try:
                

                summary =event['summary']
                event_creator = event['creator']
                creator = event_creator['email']
                
                status= event['status']
                id= event['id']

                #unpack time
                event_time_start = event['start']
                event_time_end = event['end']
                start = event_time_start['dateTime']
                end = event_time_end['dateTime']
                
            
                
                admin = event['attendees'][0]['email']
                if myemail == admin:
                    print("----------------")
                    print(f'{summary} created by {admin}')
                    print(f'starts at {start} and ends at {end}')
                    print(f'Id is: {id}')
                    n += 1
                
            except KeyError:
              
                break
        if n < 1:
            print('You have not volunteered')
        page_token = events.get('nextPageToken')
        if not page_token:
            break

