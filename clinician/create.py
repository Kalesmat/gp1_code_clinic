import datetime
from pprint import pprint
from code_clinic import get_credentials


def create(service):
    """
    Function to create an event for a Clinician
    """
    message = "Event Created"
    # print(message)
    myusername,myemail = get_credentials()

    """
    Get the Day and Time
    """
    hour,Day,Year,Month = 0,0,0,0
    #Date = input("Enter Date (Day/Month/Year)")
    #Time = input("Enter Time (HH:MM")
    while Year < 1:
        Year = int(input("Enter Year: "))

    while Month < 1 or Month > 12:
        Month = int(input("Enter Month: ")) 

    while Day < 1 or Day > 31:
        Day = int(input("Enter Day: "))

    while hour < 7 or hour > 17:
        hour = int(input("Enter Hour(From 7-17): "))
    hour2 = hour
    minutes = int(input("Enter Minutes(From 00-59): "))

    while minutes < 0 or minutes > 59 or (hour == 17 and minutes > 30):
        minutes = int(input("Enter Minutes(From 00-59): "))
    min2 = minutes+30

    if minutes >= 30:
        min2 = 0
        hour2 += 1
        add = minutes - 30
        min2 += add    

    my_date = datetime.datetime(Year, Month, Day, hour, minutes)

    # print(my_date)
    # print(datetime.datetime.now())
    if my_date < datetime.datetime.now():
        print("{} you can't create an event, Too late".format(myusername))

    else:
    
        """
        Creating the event
        """
        
        Summary,Description = "",""
        while Summary =="":
            Summary = input("Name of your topic: ")
        while Description == "":
            Description = input("Describe your topic: ")
        event = {
            'summary': 'Code Clinic: {}'.format(Summary),
        #   'location': '800 Howard St., San Francisco, CA 94103',
            'description': '{}.'.format(Description),
            'start': {
            'dateTime': '{}-{}-{}T{}:{}:00'.format(Year,Month,Day,hour,minutes),
            'timeZone': 'GMT+02',
            },
            'end': {
            'dateTime': '{}-{}-{}T{}:{}:00'.format(Year,Month,Day,hour2,min2),
            'timeZone': 'GMT+02',
            },
            'recurrence': [
            'RRULE:FREQ=DAILY;COUNT=1'
            ],
          'attendees': [
            {
                'displayName': myusername,
                'email': myemail,
                'optional': True,
                'comment': 'Creator',
                'responseStatus': 'accepted',
            },            
          ],
            'anyoneCanAddSelf': True,
            
            'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
            },
        }

        event = service.events().insert(calendarId='primary', body=event).execute()
        pprint('{}: {}'.format (message, event.get('htmlLink')))
