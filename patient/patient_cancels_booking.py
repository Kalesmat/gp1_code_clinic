from pprint import pprint
from googleapiclient.errors import HttpError
from patient import patient_view_booking


def cancel_booking(service):
    """
    Patient cancels booking after giving a reason for cancellation.
    """

    try:
        my_events = patient_view_booking.view_booking(service)
        if my_events is None:
            pprint("There are no bookings made.")
            return 0
        else:
            eventid = input("Please insert the event ID: ")
            event = service.events().get(calendarId='primary', eventId=eventid).execute()

            event['status'] = 'confirmed'
            admin = event['attendees'][0]['email']
            event['attendees'] = [
                {'email': admin},
            ]

            updated_event = service.events().update(calendarId='primary', eventId=eventid, body=event, ).execute()
            pprint(updated_event['updated'])
            pprint("Event Cancelled.")

    except HttpError:
        return"Invalid event ID.."
