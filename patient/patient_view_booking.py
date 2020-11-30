import datetime

def view_booking(service, email):
    '''
    Patient will be able to view all their bookings
    PARAMS : the service instance
    '''
    n=0
    now = datetime.datetime.utcnow()
    now = now.isoformat() + 'Z'
    page_token = None
    while True:
        events = service.events().list(calendarId='primary', timeMin=now,pageToken=page_token).execute()


        for event in events['items']:
            try:
            # Dictionary Unpacking with variables
                summary = event['summary']

                event_creator = event['creator']
                creator = event['attendees'][0]['email']
                id_user = event['id']

                #Unpacking Time Dictionaries
                event_time_start = event['start']
                event_time_end = event['end']
                start = event_time_start['dateTime']
                end = event_time_end['dateTime']

                #Output of the Date
                if len(event['attendees']) == 2:
                    patient_email = event['attendees'][1]["email"]
                    if patient_email == email:
                        n+=1
                        message_storage = (
f"""----------------
{summary} by {creator}
starts at {start} and ends at {end}
Id is: {id_user} """)
                        print(message_storage)
            except KeyError:
                break

            page_token = events.get('nextPageToken')
        if not page_token:
            break
    if n < 1:
        print("You have no booked events")
        return False
    if n == 1:
        print(f"\nYou have {n} booked slot")
    else:
        print(f"\nYou have {n} booked slots")
    return(message_storage)