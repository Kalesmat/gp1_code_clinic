import datetime
from datetime import timedelta
from datetime import datetime as dt
import colours
def view(service, myemail):
    '''This function displays the events that have been booked.'''

    message = ''
    page_token = None
    now = datetime.datetime.now().isoformat() + 'Z'
    n = 0
    while True:

        events = service.events().list(calendarId='primary', timeMin=now,
                                       pageToken=page_token).execute()

        for event in events['items']:
            try:

                event_creator = event['creator']
                summary = event['summary'].strip()
                creator = event_creator['email']
                

                status = event['status']
                id = event['id']

                #Issa's code for making a suitable time output
                start = event['start'].get('dateTime') 
                start = start.split('T')
                date = start[0]
                time = start[1].split('+')
                time = time[0]
                time = dt.strptime(time, '%H:%M:%S')
                end_t = time + timedelta(minutes=30)
                time, end_t = str(time), str(end_t)
                time, end_t = time.split(" "), end_t.split(" ")
                time, end_t = time[1], end_t[1]



                admin = event['attendees'][0]['email']
                if myemail == admin:

                    summary = colours.colour(summary, 'yellow')
                    message = (f"""----------------
{summary} by {creator}
{date} starts at {time} and ends at {end_t}
To delete run:
code_clinic.py delete {id} """)

                    print(message)
                    n += 1
            except KeyError:

                break
        if n < 1:
            message = 'You have not volunteered'
            print(message)
        elif n == 1:
            print(f"----------------\nYou have {n} event")
            message = "You have volunteered"
        else:
            print(f"----------------\nYou have {n} events")
            message = "You have volunteered"
        page_token = events.get('nextPageToken')
        if not page_token:
            break

    return message



