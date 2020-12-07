from pprint import pprint
import datetime
from googleapiclient.errors import HttpError
from patient import patient_view_open_booking, patient_view_booking


def booking(service, username, email, uuid):
    """
     Adds a booking to the google calendar
     return: Error message if the ID is invalid.
    """
    try:
        events = patient_view_open_booking.view_open_bookings(service)
        if not events:
            return False

        # my_events = patient_view_booking.view_booking(service, email)
        # for event in my_events:
        #     if event['start'] is:
        #         pprint(f"{username}, Please note that you will be in session.")
        #         return False

        else:
            eventid = uuid
            event = service.events().get(calendarId='primary', eventId=eventid).execute()

            event['status'] = 'confirmed'
            admin = event['attendees'][0]['email']

            if admin == email:
                pprint(f'{username}, Unfortunately you cannot book your own event..')
                return True
            elif len(event['attendees']) >= 2:
                pprint(f"{username}, number of attendees has been reached, please check for the next slot.")
                return True
            else:
                event['attendees'] = [
                    {'email': admin},
                    {'email': email},
                ]
                updated_event = service.events().update(calendarId='primary', eventId=eventid, body=event).execute()
                pprint(updated_event['updated'])
                pprint(f"{event['summary']} is successfully booked..")
                return True

    except HttpError:
        pprint("Unfortunately that is an invalid event ID..")
        return False
