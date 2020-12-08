import datetime
from datetime import timedelta
from datetime import datetime as dt
from pprint import pprint


def create(service, user, email):
    """
    Get the Day and Time
    """
    Day,Year,Month,hour,Min = 0,0,0,0,0

    while Day < 1 or Day > 31 or Month < 1 or Month > 12 or Year < 1:
        Datei = input("Enter Date (Day/Month/Year): ") .strip()
        if "/" in Datei:
            Date = Datei.split('/') 
            if len(Date) != 3 or not Date[0].isdigit() or not Date[1].isdigit() or not Date[2].isdigit():
                print("Date should be in this format Day/Month/Year")
                continue
        
        else:
            print("Date should be in this format Day/Month/Year")
            continue
        Day = int(Date[0])
        Month = int(Date[1])
        Year = int(Date[2])
        if Day < 1 or Day > 31:
            print("Date is invalid.")
        if Month < 1 or Month > 12:
            print("Month is invalid.")
        if Year < 1:
            print("Year is invalid.")

    """
    Check the date if is passed  and ask
    """
    my_date = datetime.datetime(Year, Month, Day,23,30)
    
    if my_date < datetime.datetime.today():
        message2 = "event cannot be created , day has passed."
        print("{} {}".format(user, message2))
        yes = ""
        while yes != 'y' or yes != 'n':
            yes = input("Would you like to create a new event(y/n)?: ").strip()
            if yes.lower() == 'y':
                create(service, user, email)
            elif yes.lower() == 'n':
                print(f'Bye {user}')
                return message2
            else:
                print("Invalid input! Please enter y or n.")

    while hour<7 or hour>17 or Min<0 or Min>59 or (hour==17 and Min>30):
        Timei = input("Enter Time (HH:MM): ").strip()
        if ":" in Timei:
            Time = Timei.split(":")
            if len(Time) != 2 or not Time[0].isdigit() or not Time[1].isdigit():
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
            print("Minutes should be between 00-30 since we close at 18:00")            

    hour2 = hour      
    min2 = Min+30

    if Min >= 30:
        min2 = 0
        hour2 += 1
        add = Min - 30
        min2 += add    

    my_date = datetime.datetime(Year, Month, Day, hour, Min)

    
    if my_date < datetime.datetime.now():
        message2 = "event cannot be created , time has passed."
        print("{} {}".format(user,message2))
        yes = ""
        while yes!='y' or yes!='n' :
            yes = input("Would you like to create a new event(y/n)?: ").strip()
            if yes.lower() == 'y':
                create(service,user,email)
            elif yes.lower() == 'n':
                print(f'Bye {user}')
                return message2
            else:
                print("Invalid input! Please enter y or n.")
    else:
        startD = str(Year)+"-"+str(Month)+"-"+str(Day)
        startT = str(hour)+":"+str(Min)
        endT = str(hour2)+":"+str(min2)

        """
        Checking if you have created Event Before
            - 30 minutes before start Time
            - During Available Event
            - Before the End Time
        """
        
        if createdE(service,email,my_date,endT):
            message = "You will be busy during that time"
            print(message)
            return message
    
        """
        Creating the event
        """

        Summary,Descript = "",""
        while Summary =="":
            Summary = input("Name of your topic: ").strip()
            
        while Descript == "":
            Descript = input("Describe your topic: ").strip()

        

        confirm = ""
        while confirm.lower() != 'y' or confirm.lower() != 'n':
            confirm = input("Confirm event?(y/n): ").strip()
            if confirm.lower() == 'y' or confirm.lower() == 'n':
                break
        
        if confirm.lower() == 'y':
            event=do_create(service,Summary,Descript,startD,startT,endT,user,email) 
            message = event['id']       
            pprint('{}: {}'.format(message, event.get('htmlLink')))        # print(event['id'])
            
        else:
            message = "you have not created the event"
            print(message)
        return message


def do_create(service,Summary,Descript,startD,startT,endT,username,email):

    event = {
        'summary': 'Code Clinic: {}'.format(Summary),
        'description': '{}.'.format(Descript),
        'start': {
            'dateTime': '{}T{}:00'.format(startD, startT),
            'timeZone': 'GMT+02',
        },
        'end': {
            'dateTime': '{}T{}:00'.format(startD,endT),
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

    event = service.events().insert(calendarId='primary', body=event).execute()
    return event


def createdE(service, myemail,my_date,endT):
    page_token = None
    now = datetime.datetime.now().isoformat() + 'Z'
    n = 0
    
    while True:

        events = service.events().list(calendarId='primary', timeMin=now,
                                       pageToken=page_token).execute()

        for event in events['items']:
            try:                
                start = event['start'].get('dateTime')                 
                start = start.split('T')                
                date = start[0]
                time = start[1].split('+')
                time = time[0]
                time = dt.strptime(time, '%H:%M:%S')
                end_t = time + timedelta(minutes=30) 
                start_c = time + timedelta(minutes=-30)               
                time, end_t,start_c = str(time), str(end_t), str(start_c)
                time, end_t,start_c = time.split(" "), end_t.split(" "), start_c.split(" ")
                time, end_t,start_c = time[1], end_t[1], start_c[1]

                admin = event['attendees'][0]['email']

                Dat=date.split('-')
                Tim=end_t.split(':')
                tim=datetime.datetime(int(Dat[0]),int(Dat[1]),int(Dat[2]),int(Tim[0]),int(Tim[1]))
                Sta=start_c.split(':')
                Sta=datetime.datetime(int(Dat[0]),int(Dat[1]),int(Dat[2]),int(Sta[0]),int(Sta[1]))

                
                if myemail == admin:
                    if (my_date>Sta and my_date<tim):                        
                        n += 1                   
                        
            except KeyError:

                break
        if n < 1:
            return False
        
        else:
            return True
