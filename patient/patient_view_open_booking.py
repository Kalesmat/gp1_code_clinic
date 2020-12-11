import datetime
from datetime import timedelta
from datetime import datetime as dt
from colours import colour

def view_open_bookings(service, days_to_display):
   '''Function to get the next 7 days events'''
   # Call the Calendar API
 
   now = datetime.datetime.utcnow()
   end_time = now + timedelta(days=days_to_display)
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
      try:
         id_event = event['id'].split('_')
         eventId = colour(id_event[0], 'blue')
         event_summary = colour(event['summary'], 'green')
         print(event_summary.strip(), 'by', event['attendees'][0]['email'],"\n", date, '', time,'-',end_t,'\n', "To book the session run:\n",f"python3 code_clinic.py book{eventId}",'\n','-'*70)
         i += 1
      except KeyError as keyerr:
         pass
   print("\nThere are {} slots available\n".format(i))
   return True

