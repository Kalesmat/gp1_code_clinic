from googleapiclient.errors import HttpError


def cancel_booking(service, username, email, uuid):

    try:
        event_id = uuid
        event = service.events().get(calendarId='primary', eventId=event_id).execute()

        event['status'] = 'confirmed'
        admin = event['attendees'][0]['email']
        email2 = event['attendees'][1]['email']

        if email == email2:
            event['attendees'] = [
                {'email': admin},
            ]
            sendNotifications = True
            updated_event = service.events().update(calendarId='primary', eventId=event_id,
                                                    body=event, sendUpdates='all').execute()
            print(f"{username},You have successfully cancelled your booking.")
            return True
        else:
            print(f"{username}, You are not the attendee on this event.")
            return False

    except HttpError:
        print("Unfortunately that is an invalid event ID..")
        return False

    except IndexError:
        print(f"{username}, You are not the attendee on this event.")
        return True
