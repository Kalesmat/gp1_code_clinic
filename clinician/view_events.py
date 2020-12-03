from  colorama import Fore
from colorama import Style
import datetime

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
                summary = event['summary']
                creator = event_creator['email']
                

                status = event['status']
                id = event['id']

                #unpack time
                event_time_start = event['start']
                event_time_end = event['end']
                start = event_time_start['dateTime']
                end = event_time_end['dateTime']

                admin = event['attendees'][0]['email']
                if myemail == admin:
                    
                    message = (
                    f"----------------\n{Fore.YELLOW}{summary}{Style.RESET_ALL} created by {admin}\nstarts at {start} and ends at {end}\nId is: {id}")

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



