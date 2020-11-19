from pprint import pprint
from patient import patient_view_open_booking


def booking(service):
    """
     Adds a booking to the google calendar
    """
    events = patient_view_open_booking.view_open_bookings(service)
    pprint(events)
    eventid = input("Please insert the event ID: ")
    event = service.events().get(calendarId='primary', eventId=eventid).execute()

    event['status'] = 'confirmed'
    admin = event['attendees'][0]['email']
    event['attendees'] = [
        {'email': admin},
        {'email': 'patient.cc.team14@gmail.com'},
    ]

    updated_event = service.events().update(calendarId='primary', eventId=eventid,body=event, ).execute()
    pprint(updated_event['updated'])




