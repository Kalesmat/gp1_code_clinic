def view_booking(service):
    '''
    Patient will be able to view all their bookings
    PARAMS : the service instance
    '''

    print("These Are Your Booked Events:")
    page_token = None
    while True:
        events = service.events().list(calendarId='primary', pageToken=page_token).execute()
        
        for event in events['items']:
            try:
            # Dictionary Unpacking with variables
                summary = event['summary']
                
                event_creator = event['creator']
                creator = event_creator['email']
                id_user = event['id']

                #Unpacking Time Dictionaries
                event_time_start = event['start']
                event_time_end = event['end']
                start = event_time_start['dateTime']
                end = event_time_end['dateTime']
                
                #Output of the Data
                if event['status'] == "confirmed":
                    print("----------------")
                    print(f'{summary} by {creator}')
                    print(f'starts at {start} and ends at {end}')
                    print(f'Id is: ({id_user})')

            except KeyError:
                break

            page_token = events.get('nextPageToken')
        if not page_token:
            break
        