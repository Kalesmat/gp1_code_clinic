from pprint import pprint
from googleapiclient.errors import HttpError
import datetime
from datetime import timedelta
from datetime import datetime as dt
import colours


def booking(service, username, email, uuid):
    """
    Books an available slot created  by a clinician
    :param service: Instance that allows that patient to book a slot
    :param username: User credentials to interact with the user
    :param email: User credentials helps with checks
    :param uuid: Event code that we use when we book a session
    :return: B
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
            print(f"{username}, number of attendees has been reached, please check for the next slot.")
            return True
        else:
            if booked(service, email, eventid):
                return True

            event['attendees'] = [
                {'email': admin},
                {'email': email},
            ]
            updated_event = service.events().update(calendarId='primary', eventId=eventid, body=event).execute()
            # pprint(updated_event['updated'])
            pprint(f"{event['summary']} is successfully booked..")
            return True

    except HttpError:
        pprint("Unfortunately that is an invalid event ID..")
        return False


def booked(service, email, eventid):
    """
    Prevents patient from double booking themselves
    :param service: Instance that allows that patient to book a slot
    :param email: User credentials helps with checks
    :param eventid: Event code that we use when we book a session
    :return: Boolean
    """
    n = 0
    now = datetime.datetime.utcnow()
    now = now.isoformat() + 'Z'
    page_token = None
    while True:
        events = service.events().list(calendarId='primary', timeMin=now,pageToken=page_token).execute()

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
                busy_time = time
                admin = event['attendees'][0]["email"]
                summary = event['summary']
                patient_email=""

                if len(event['attendees']) == 2:
                    patient_email = event['attendees'][1]["email"]

                Dat = date.split('-')
                Tim = end_t.split(':')
                tim = datetime.datetime(int(Dat[0]), int(Dat[1]), int(Dat[2]), int(Tim[0]), int(Tim[1]))
                Sta = start_c.split(':')
                Sta = datetime.datetime(int(Dat[0]), int(Dat[1]), int(Dat[2]), int(Sta[0]), int(Sta[1]))

                event = service.events().get(calendarId='primary', eventId=eventid).execute()

                event2T = event['start']['dateTime']

                event2T = str(event2T).split('T')

                date2 = event2T[0]
                event2T = str(event2T[1]).split('+')
                time = event2T[0]

                Dat = date.split('-')

                Timl = time.split(':')
                tim2 = datetime.datetime(int(Dat[0]), int(Dat[1]), int(Dat[2]), int(Timl[0]), int(Timl[1]))

                Sta2 = start_c.split(':')
                Sta2 = datetime.datetime(int(Dat[0]), int(Dat[1]), int(Dat[2]), int(Sta2[0]), int(Sta2[1]))

                if email == patient_email:
                    clinician = admin.rstrip('@student.wethinkcode.co.za')
                    if (tim2 > Sta and tim2 < tim):
                        print(f"Failed to book because:\n- You will be consulted by {clinician} on {summary}"
                              f"\n- From {busy_time} until {end_t}")
                        n += 1
                        return True

                elif email == admin:
                    if (tim2 >= Sta and tim2 <= tim):
                        print(f"Failed to book because:\n- You are a clinician on {summary}"
                              f"\n- From {busy_time} until {end_t}")
                        n += 1
                        return True

            except KeyError:
                break

            page_token = events.get('nextPageToken')
        if not page_token:
            break

    return False
