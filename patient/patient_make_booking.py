from pprint import pprint
from googleapiclient.errors import HttpError
import datetime
from datetime import timedelta
from datetime import datetime as dt


def booking(service, username, email, uuid):
    """
     Adds a booking to the google calendar
     :param uuid: An event ID code that is used for booking a session
     :param username: The user's credentials we use to interact more with the user
     :param service: Instance that helps with adding an event in the calendar
     :param email:The user's credentials that we use for checks
     return: Error message if the ID is invalid.
    """
    try:
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
            if booked(service, email, eventid):
                print(f"{username}, There is a session booked for this time.")
                return True

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


def booked(service, email, eventid):
    """
    Here we check if the user is not trying to double book themselves
    :param service: Instance that helps with adding an event in the calendar
    :param email: The user's credentials that we use for checks
    :param eventid: An event ID code that is used for booking a session
    :return: Boolean
    """

    n = 0
    now = datetime.datetime.utcnow()
    now = now.isoformat() + 'Z'
    page_token = None
    while True:
        events = service.events().list(calendarId='primary', timeMin=now, pageToken=page_token).execute()

        for event in events['items']:
            try:
                start = event['start'].get('dateTime')
                start = start.split('T')
                date = start[0]
                time = start[1].split('+')
                time = time[0]
                time = dt.strptime(time, '%H:%M:%S')
                end_t = time + timedelta(minutes=30)
                start_c = time + timedelta(minutes=-30)
                time, end_t, start_c = str(time), str(end_t), str(start_c)
                time, end_t, start_c = time.split(" "), end_t.split(" "), start_c.split(" ")
                time, end_t, start_c = time[1], end_t[1], start_c[1]

                dat = date.split('-')
                tim = end_t.split(':')
                tim = datetime.datetime(int(dat[0]), int(dat[1]), int(dat[2]), int(tim[0]), int(tim[1]))
                sta = start_c.split(':')
                sta = datetime.datetime(int(dat[0]), int(dat[1]), int(dat[2]), int(sta[0]), int(sta[1]))

                event = service.events().get(calendarId='primary', eventId=eventid).execute()

                event2_t = event['start']['dateTime']
                event2_t = str(event2_t).split('T')
                event2_t = str(event2_t[1]).split('+')
                time = event2_t[0]
                dat = date.split('-')
                timl = time.split(':')
                tim2 = datetime.datetime(int(dat[0]), int(dat[1]), int(dat[2]), int(timl[0]), int(timl[1]))
                sta2 = start_c.split(':')
                sta2 = datetime.datetime(int(dat[0]), int(dat[1]), int(dat[2]), int(sta2[0]), int(sta2[1]))

                if sta <= tim2 <= tim:
                    n += 1
            except KeyError:
                break

            page_token = events.get('nextPageToken')
        if not page_token:
            break
    if n < 1:
        return False
    else:
        return True
