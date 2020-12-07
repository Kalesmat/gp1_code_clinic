from pprint import pprint
from googleapiclient.errors import HttpError
from patient import patient_view_booking


def cancel_booking(service, username, email, uuid):
    try:
        my_events = patient_view_booking.view_booking(service, email)
        if not my_events:
            return False
        else:
            eventid = uuid
            event = service.events().get(calendarId='primary', eventId=eventid).execute()

            event['status'] = 'confirmed'
            admin = event['attendees'][0]['email']
            email2 = event['attendees'][1]['email']

            if email == email2:
                event['attendees'] = [
                    {'email': admin},
                ]
                updated_event = service.events().update(calendarId='primary', eventId=eventid, body=event, ).execute()
                pprint(updated_event['updated'])
                pprint(f"{username},You have successfully cancelled your booking.")
                return True
            else:
                pprint(f"{username}, You are not the attendee on this event.")
                return False

    except HttpError:
        print("Unfortunately that is an invalid event ID..")
        return False

    except IndexError:
        return True
