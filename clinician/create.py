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
    Day,Year,Month,hour,Min = 0,0,0,0,0

    while Day < 1 or Day > 31 or Month < 1 or Month > 12 or Year < 1:
        Datei = input("Enter Date (Day/Month/Year): ") 
        if "/" in Datei:
            Date = Datei.split('/')  
            if len(Date) != 3:
                print("Date should be in this format Day/Month/Year")
                continue
        # elif "-" in Datei:
        #     Date = Datei.split('-')
        else:
            print("Date should be in this format Day/Month/Year")
            continue
        Day = int(Date[0])
        Month = int(Date[1])
        Year = int(Date[2])
        if Day < 1 or Day > 31:
            print("Date is Wrong")
        if Month < 1 or Month > 12:
            print("Month is Wrong")
        if Year < 1:
            print("Year is Wrong")

    while hour<7 or hour>17 or Min<0 or Min>59 or (hour==17 and Min>30):
        Timei = input("Enter Time (HH:MM): ")
        if ":" in Timei:
            Time = Timei.split(":")
            if len(Time) != 2:
                print("Time should be in this format HH:MM")
                continue
        else:
            print("Time should be in this format HH:MM")
            continue
        hour = int(Time[0])
        Min = int(Time[1])  

        if hour < 7 or hour > 17:
            print("Hour should be between 7 and 17")
        if Min < 0 or Min > 59:
            print("Minutes should be between 0 and 59")
        if hour == 17 and Min > 30:
            print("Minutes shoul be between 00-30 since we close at 18:00")            

    hour2 = hour      
    min2 = Min+30

    if Min >= 30:
        min2 = 0
        hour2 += 1
        add = Min - 30
        min2 += add    

    my_date = datetime.datetime(Year, Month, Day, hour, Min)

    # print(my_date)
    # print(datetime.datetime.now())
    if my_date < datetime.datetime.now():
        message2 = "you can't create an event, Too late"
        print("{} {}".format(myusername,message2))

        return message2
    else:
    
        """
        Creating the event
        """

        Summary,Description = "",""
        while Summary =="":
            Summary = input("Name of your topic: ")
            if Summary != "":
                AgreeM = "Press enter if you agree else type No: "
                Agree = input(f"Summary is {Summary}. {AgreeM}")
                if Agree != '':
                    continue
        while Description == "":
            Description = input("Describe your topic: ")

        startD = str(Year)+"-"+str(Month)+"-"+str(Day)

        event = do_create(service, Summary, Description, startD, hour, Min, hour2, min2, myusername, myemail)

        pprint('{}: {}'.format(message, event.get('htmlLink')))

        # print(event['id'])
        return event['id']


def do_create(service, Summary, Description, startD, hour, Min, hour2, min2, myusername, myemail):

    event = {
        'summary': 'Code Clinic: {}'.format(Summary),
        #   'location': '800 Howard St., San Francisco, CA 94103',
        'description': '{}.'.format(Description),
        'start': {
            'dateTime': '{}T{}:{}:00'.format(startD, hour, Min),
            'timeZone': 'GMT+02',
        },
        'end': {
            'dateTime': '{}T{}:{}:00'.format(startD, hour2, min2),
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

    return event

