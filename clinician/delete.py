import code_clinic
from clinician import view_events
from googleapiclient.errors import HttpError

def delete(service):
    """
    Gets the eventID from the user and deletes the event from the calendar
    :param service: service instance of the google api
    :return: message of response
    """

    try:
        view_events.view(service)

        id = input('Please give event ID: ')

        event = service.events().get(calendarId='primary', eventId=id).execute()
        creator = event['attendees']
        delete = False
        for i in creator:
            if i['email'] == code_clinic.get_credentials()[1]:
                delete = True
        if delete:
            delete_event = service.events().delete(calendarId='primary', eventId=id).execute()
            message = 'Event delete'
        else:
            message = 'Your are not allowed to delete this event'
        print(message)

        return message
    except KeyError:
        print('Key does not exist')
    except HttpError:
        print('Wrong event ID')