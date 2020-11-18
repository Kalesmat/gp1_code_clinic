
def view(service):
   
    '''This function displays the events that have been booked.'''

    page_token = None

    while True:
        events = service.events().list(calendarId='primary', pageToken=page_token).execute()
        for event in events['items']:
            try:
                summary =event['summary']
                
                start=event['start']
                end= event['end']
                status= event['status']
                id= event['id']
                
                print(f'You have a {summary} session event Id {id} at {start} till {end} ')
                print(f'Status: {status}')
            
            except KeyError:
        
                break    
        page_token = events.get('nextPageToken')
        if not page_token:
            break
    #iteration 1
    events_set=['Recursion ' ,' Luke','11/11/2020' ,'14:30']
    for i in range(len(events_set)):

        print(str(events_set[i]))
    return str(events_set)


