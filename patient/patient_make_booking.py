from pprint import pprint
from googleapiclient.errors import HttpError
from patient import patient_view_open_booking


def booking(service, username, email):
    """
     Adds a booking to the google calendar
    """
    try:
        events = patient_view_open_booking.view_open_bookings(service)
        if events is None:
            return 0
        else:
            eventid = input("Please insert the event ID: ")
            event = service.events().get(calendarId='primary', eventId=eventid).execute()

            event['status'] = 'confirmed'
            admin = event['attendees'][0]['email']
            if admin == email:
                print(f'{username}, Unfortunately that is an invalid action.')
            else:
                event['attendees'] = [
                    {'email': admin},
                    {'email': email},
                ]
                updated_event = service.events().update(calendarId='primary', eventId=eventid, body=event).execute()
                pprint(updated_event['updated'])
                pprint(f"{eventid} is successfully booked..")

    except HttpError:
        pprint("Unfortunately that is an invalid event ID..")






