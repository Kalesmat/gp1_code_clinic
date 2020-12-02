import datetime
from datetime import timedelta
from datetime import datetime as dt

def view_open_bookings(service):
   '''Function to get the next 7 days events'''
   # Call the Calendar API
 
   now = datetime.datetime.utcnow()
   end_time = now + timedelta(days=7)
   end_time = end_time.isoformat() + 'Z' # 'Z' indicates UTC time
   now = now.isoformat() + 'Z' # 'Z' indicates UTC time
   events_result = service.events().list(
      calendarId='codeclinic.team14@gmail.com', timeMin=now,
      timeMax=end_time, singleEvents=True,maxAttendees=1,
      orderBy='startTime').execute()
   events = events_result.get('items', [])

   if not events:
      print('No upcoming events found.')
      return False
   i = 0 

   for event in events:
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
      try:
         id_event = event['id'].split('_')
         eventId = id_event[0]
         print(date, '', time,'-',end_t,"\n",event['summary'],'\n', eventId,'\n', event['attendees'][0]['email'],'\n','-'*100)
         i += 1
      except KeyError as keyerr:
         print('no attendees on the event\n', '-'*20)
   print("There are {} slots available".format(i))   
   return True

