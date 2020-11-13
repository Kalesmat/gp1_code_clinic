# import datetime

def view_open_bookings():
    """
    The patient will be able to see a list of all available slots
    """
    avail_slots = """
    9:00 hangman 1 - Summer Smith
    9:30 recursion - Morty Smith
    10:00 TDD(unit testing) - Rick Sanchez
    """
    print(avail_slots)

#     # Call the Calendar API
#     now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
#     print('Getting the upcoming 10 events')
#     events_result = service.events().list(calendarId='codeclinic.team14@gmail.com', timeMin=now,
#                                         maxResults=10, singleEvents=True,
#                                         orderBy='startTime').execute()
#     events = events_result.get('items', [])

#     if not events:
#         print('No upcoming events found.')
#     for event in events:
#         start = event['start'].get('dateTime', event['start'].get('date'))
#         print(start, event['summary'])


    return avail_slots
