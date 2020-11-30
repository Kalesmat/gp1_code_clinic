from clinician import view_events
from googleapiclient.errors import HttpError


def delete(service, email):
    """
    Gets the eventID from the user and deletes the event from the calendar
    :param service: service instance of the google api
    :param email: email from config file
    """
    view_events.view(service, email)

    while True:
        event_id = input('\nPlease give event ID: ').strip()
        if event_id:
            break
        else:
            print('No event ID was inputted please input an event ID')

    do_delete(service, email, event_id)


def do_delete(service, email, id):
    """
    Does the delete with an email and event ID with the google API
    :param service: service instance of the google api
    :param email: email from config file
    :param id: event ID
    :return:  message of response
    """
    try:
        event = service.events().get(calendarId='primary', eventId=id).execute()
        creator = event['attendees']
        to_delete = False
        for i in creator:
            if i['email'] == email:
                to_delete = True
        if to_delete:
            delete_event = service.events().delete(calendarId='primary', eventId=id).execute()
            message = 'Event Deleted'
        else:
            message = 'Your are not allowed to delete this event'
        print(message)
        return message
    except KeyError:
        print('Key does not exist')
    except HttpError:
        print('Invalid ID')