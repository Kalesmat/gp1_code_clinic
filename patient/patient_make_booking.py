from pprint import pprint
from googleapiclient.errors import HttpError
from patient import patient_view_open_booking


def booking(service, username, email):
    """
     Adds a booking to the google calendar
    """

    try:
        patient_view_open_booking.view_open_bookings(service)
        eventid = input("Please insert the event ID: ")
        event = service.events().get(calendarId='primary', eventId=eventid).execute()

        event['status'] = 'confirmed'
        admin = event['attendees'][0]['email']
        if admin == email:
            print(f'{username}, You can not book your own slot')
        else:
            event['attendees'] = [
                {'email': admin},
                {'email': email},
            ]

            updated_event = service.events().update(calendarId='primary', eventId=eventid,body=event, ).execute()
            pprint(updated_event['updated'])
            pprint(f"Slot ({eventid}) is successfully booked..")

    except HttpError:
        pprint("Invalid event ID..")






