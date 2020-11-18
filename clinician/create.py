import datetime
from pprint import pprint


def create(service):
    """
    Function to create an event for a Clinician
    """
    message = "Event Created"
    print(message)

    """
    Get the Day and Time

    """
    # today = date.today() 

    hour,Day,Year,Month = 0,0,0,0

    while Year < 1:
        Year = int(input("Enter Year: "))

    while Month < 1 or Month > 12:
        Month = int(input("Enter Month: ")) 

    while Day < 1 or Day > 31:
        Day = int(input("Enter Day: "))

    while hour < 7 or hour > 17:
        hour = int(input("Enter Hour(From (7-17)): "))
    hour2 = hour
    minutes = int(input("Enter Minutes(From (00-60)): "))

    while minutes < 0 or minutes > 60 or (hour == 17 and minutes > 30):
        minutes = int(input("Enter Minutes(From (00-60)): "))
    minutes2 = minutes+30

    if minutes >= 30:
        minutes2 = 0
        hour2 += 1
        add = minutes - 30
        minutes2 += add    

    my_date = datetime.datetime(Year, Month, Day, hour, minutes)#.isoformat()

    print(my_date)
    print(datetime.datetime.now())
    if my_date < datetime.datetime.now():
        print("Too Late, you can't create an event")

    else:
    #Format the date
        """
        Creating the event
        """
        Description = input("Describe your event: ")
        Summary = input("Summary of your event: ")
        event = {
            'summary': '{}'.format(Summary),
        #   'location': '800 Howard St., San Francisco, CA 94103',
            'description': '{}.'.format(Description),
            'start': {
            'dateTime': '{}-{}-{}T{}:{}:00'.format(Year,Month,Day,hour,minutes),
            'timeZone': 'GMT+02',
            },
            'end': {
            'dateTime': '{}-{}-{}T{}:{}:00'.format(Year,Month,Day,hour2,minutes2),
            'timeZone': 'GMT+02',
            },
            'recurrence': [
            'RRULE:FREQ=DAILY;COUNT=1'
            ],
        #   'attendees': [
        #     {'email': 'lpage@example.com'},
        #     {'email': 'sbrin@example.com'},
        #   ],
            'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
            },
        }

        event = service.events().insert(calendarId='primary', body=event).execute()
        pprint('Event created: {}'.format (event.get('htmlLink')))

    return message