import datetime
from datetime import timedelta
from datetime import datetime as dt
import colours
n=0


def view_booking(service, email):
    global n
    '''
    Patient will be able to view all their bookings
    PARAMS : the service instance
    '''
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
#                         message_storage = (
# f"""----------------\n{summary} by {creator}
# starts on {date} at {time} and ends at {end_t}
# To cancel attendance run:
# python3 code_clinic.py cancel{id_user} """)
                        # print(message_storage)
                        print(summary.strip(), 'by', event['attendees'][0]['email'],"\n", date, '', time,'-',end_t,'\n', "To cancel the session run:\n",f"python3 code_clinic.py cancel{id_user}",'\n','-'*70)
            except KeyError:
                break

            page_token = events.get('nextPageToken')
        if not page_token:
            break
    if n < 1:
        final_string = "You have no booked slots\n"
        print(final_string)
        return(final_string)
    if n == 1:
        final_string = f"\nYou have {n} booked slot\n"
        print(final_string)
        return(final_string)

    else:
        final_string = f"\nYou have {n} booked slots\n"
        print(final_string)
        return(final_string)
 