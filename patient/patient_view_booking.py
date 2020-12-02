import datetime
from datetime import timedelta
from datetime import datetime as dt
import colours

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
                summary = colours.colour(summary,"green")
                event_creator = event['creator']
                creator = event['attendees'][0]['email']
                creator = colours.colour(creator,"yellow")
                id_user = event['id']
                id_user = colours.colour(id_user,"cyan")

                #Issa's code for making a suitable time output
                start = event['start'].get('dateTime') #, event['start'].get('date') #.strip("T12:00:00+02:00")
                start = start.split('T')
                date = start[0]
                time = start[1].split('+')
                time = time[0]
                time = dt.strptime(time, '%H:%M:%S')
                end_t = time + timedelta(minutes=30)
                time, end_t = str(time), str(end_t)
                time, end_t = time.split(" "), end_t.split(" ")
                time, end_t = time[1], end_t[1]



                #Output of the Date
                if len(event['attendees']) == 2:
                    patient_email = event['attendees'][1]["email"]
                    if patient_email == email:
                        n+=1
                        message_storage = (
f"""----------------
{summary} by {creator}
starts at {time} and ends at {end_t}
Id is: {id_user} """)
                        print(message_storage)
            except KeyError:
                break

            page_token = events.get('nextPageToken')
        if not page_token:
            break
    if n < 1:
        final_string = "You have no booked slots"
        print(final_string)
        return(final_string)
    if n == 1:
        final_string = f"\nYou have {n} booked slot"
        print(final_string)
        return(final_string)
        
    else:
        final_string = f"\nYou have {n} booked slots"
        print(final_string)
        return(final_string)
 