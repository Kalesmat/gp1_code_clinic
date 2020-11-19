from patient import patient_view_booking
from pprint import  pprint

def cancel_booking(service):
    """
    Patient cancels booking after giving a reason for cancellation.
    """
    text = "Booking cancelled."
    print(text)

    events = patient_view_booking.view_booking(service)
    pprint(events)
    eventid = input("Please insert the event ID: ")
    event = service.events().get(calendarId='primary', eventId=eventid).execute()

    event['status'] = 'confirmed'
    admin = event['attendees'][0]['email']
    event['attendees'] = [
        {'email': admin},

    ]

    updated_event = service.events().update(calendarId='primary', eventId=eventid, body=event, ).execute()
    pprint(updated_event['updated'])
    pprint("Event Cancelled")
    return text
