import datetime
from datetime import timedelta
from datetime import datetime as dt
from pprint import pprint


def create(service, user, email):
    """
    Get the day and time
    """
    day,year,month,hour,minutes = 0,0,0,0,0

    while day < 1 or day > 31 or month < 1 or month > 12 or year < 1:
        dateinput = input("Enter date (day/month/year): ") .strip()
        if "/" in dateinput:
            date = dateinput.split('/') 
            if len(date) != 3 or not date[0].isdigit()\
                 or not date[1].isdigit() or not date[2].isdigit():
                print("date should be in this format day/month/year")

                continue
        
        else:
            print("date should be in this format day/month/year")

            continue
        day = int(date[0])
        month = int(date[1])
        year = int(date[2])
        if day < 1 or day > 31:
            print("date is invalid.")
        if month < 1 or month > 12:
            print("month is invalid.")
        if year < 1:
            print("year is invalid.")

    """
    Check the date if is passed  and ask
    """
    my_date = datetime.datetime(year, month, day,23,30)
    
    if my_date < datetime.datetime.today():
        message2 = "event cannot be created , day has passed."
        print("{} {}".format(user, message2))
        
        print(f'Bye {user}')

        return message2
        

    while hour<7 or hour>17 or minutes<0 or minutes>59\
        or (hour==17 and min>30):
        timeinput = input("Enter time (HH:MM): ").strip()
        if ":" in timeinput:
            time = timeinput.split(":")
            if len(time) != 2 or not time[0].isdigit()\
                or not time[1].isdigit():
                print("time should be in this format HH:MM")

                continue
        else:
            print("time should be in this format HH:MM")

            continue
        hour = int(time[0])
        minutes = int(time[1])  

        if hour < 7 or hour > 17:
            print("Hour should be between 7 and 17")
        if minutes < 0 or minutes > 59:
            print("minutes should be between 0 and 59")
        if hour == 17 and minutes > 30:
            print("minutes should be between 00-30 since we close at 18:00")            

    hour2 = hour      
    minutes2 = minutes+30

    if minutes >= 30:
        minutes2 = 0
        hour2 += 1
        add = minutes - 30
        minutes2 += add    

    my_date = datetime.datetime(year, month, day, hour, minutes)

    
    if my_date < datetime.datetime.now():
        message2 = "event cannot be created , time has passed."
        print("{} {}".format(user,message2))
        
        print(f'Bye {user}')

        return message2
            
    else:
        startday = str(year)+"-"+str(month)+"-"+str(day)
        starttime = str(hour)+":"+str(minutes)
        endtime = str(hour2)+":"+str(minutes2)

        """
        Checking if you have created Event Before
            - 30 minutes before start time
            - During Available Event
            - Before the End time
        """
        
        if createdevent(service,email,my_date):
            message = "You will be busy during that time"
            
            return message

    
        """
        Creating the event
        """

        summary,description = "",""
        while summary =="":
            summary = input("Name of your topic: ").strip()
            
        while description == "":
            description = input("Describe your topic: ").strip()        

        confirm = ""
        while confirm.lower() != 'y' or confirm.lower() != 'n':
            confirm = input("Confirm event?(y/n): ").strip()
            if confirm.lower() == 'y' or confirm.lower() == 'n':

                break
        
        if confirm.lower() == 'y':
            event=do_create(service,summary,description,startday,starttime,\
                endtime,user,email) 
            message = "Event created successfully"
            print('{}\n - Calender Link: {}'.format(message,\
                event.get('htmlLink'))) 
            
        else:
            message = "Event not created"
            print(message)

        return message


def do_create(service,summary,description,startday,\
    starttime,endtime,username,email):

    """
    Function to create the event and return event id
    """
    event = {
        'summary': 'Code Clinic: {}'.format(summary),
        'description': '{}.'.format(description),
        'start': {
            'dateTime': '{}T{}:00'.format(startday, starttime),
            'timeZone': 'GMT+02',
        },
        'end': {
            'dateTime': '{}T{}:00'.format(startday,endtime),
            'timeZone': 'GMT+02',
        },
        'recurrence': [
            'RRULE:FREQ=DAILY;COUNT=1'
        ],
        'attendees': [
            {
                'displayName': username,
                'email': email,
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

    event = service.events().insert(calendarId='primary', body=event,\
        sendUpdates='all').execute()

    return event


def createdevent(service, myemail,my_date):
    """
    Checking if you have created Event Before
        - 30 minutes before start time
        - During Available Event
        - Before the End time
        - And you are not a patient during that time
        - Return True else return False
    """
    page_token = None
    now = datetime.datetime.now().isoformat() + 'Z'
    
    while True:

        events = service.events().list(calendarId='primary', timeMin=now,
                                       pageToken=page_token).execute()

        for event in events['items']:
            try:                
                start = event['start'].get('dateTime')                 
                start = str(start).split('T')                
                date = start[0]
                time = start[1].split('+')
                time = time[0]
                time = dt.strptime(time, '%H:%M:%S')
                end_t = time + timedelta(minutes=30) 
                start_c = time + timedelta(minutes=-30)               
                time, end_t,start_c = str(time), str(end_t), str(start_c)
                time, end_t = time.split(" "), end_t.split(" ") 
                start_c = start_c.split(" ")
                time, end_t,start_c = time[1], end_t[1], start_c[1]

                admin = event['attendees'][0]['email']
                summary = event['summary']

                dat=date.split('-')
                Tim=end_t.split(':')
                tim=datetime.datetime(int(dat[0]),int(dat[1]),\
                    int(dat[2]),int(Tim[0]),int(Tim[1]))
                Sta=start_c.split(':')
                Sta=datetime.datetime(int(dat[0]),int(dat[1]),\
                    int(dat[2]),int(Sta[0]),int(Sta[1]))

                
                if myemail == admin:
                    if (my_date>Sta and my_date<tim):                        
                        print("Failed to Create a Slot because:")
                        print(f" - You will be busy with {summary}")
                                                
                        return True 

                if len(event['attendees']) == 2:
                    admin = event['attendees'][0]["email"]
                    patient_email = event['attendees'][1]["email"]
                    if myemail == patient_email:                    
                        if (my_date>Sta and my_date<tim):                        
                            print("Failed to Create a slot because:")
                            print(f" - You will be busy with {admin}\
                                 on {summary}")
                            
                            return True
                       
            except KeyError:

                break

            page_token = events.get('nextPageToken')
        if not page_token:

            break
           
    return False
