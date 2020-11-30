from pprint import pprint
from googleapiclient.errors import HttpError
from patient import patient_view_booking


def cancel_booking(service, username, email):
    try:
        my_events = patient_view_booking.view_booking(service, email)
        if my_events is None:
            pprint(f"{username}, There are no recent bookings made.")
            return False
        else:
            eventid = input("Please insert the event ID: ")
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
                pprint(f"{username},You have successfully cancelled slot.")  # will ask Lesedi to include username because I want to be uniform
                return True
            else:
                pprint(f"{username}, You are not the attendee on this event.")
                return False

    except HttpError:
        print("Unfortunately that is an invalid event ID..")
        return False

    except IndexError:
        return True

