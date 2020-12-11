from googleapiclient.errors import HttpError
import datetime
from datetime import timedelta
from datetime import datetime as dt


def booking(service, username, email, uuid):
    """
    Books an available slot created  by a clinician
    :param service: Instance that allows that patient to book a slot
    :param username: User credentials to interact with the user
    :param email: User credentials helps with checks
    :param uuid: Event code that we use when we book a session
    :return: Bool
    """
    try:
        event_id = uuid
        event = service.events().get(calendarId='primary', eventId=event_id).execute()

        event['status'] = 'confirmed'
        admin = event['attendees'][0]['email']

        if admin == email:
            print(f'{username}, Unfortunately you cannot book your own event..')
            return True
        elif len(event['attendees']) >= 2:
            print(f"{username}, number of attendees has been reached, "
                  f"please check for the next slot.")
            return True
        else:
            if booked(service, email, event_id):
                return True

            event['attendees'] = [
                {'email': admin},
                {'email': email},
            ]
            sendNotifications = True
            updated_event = service.events().update(calendarId='primary', eventId=event_id,
                                                    body=event, sendUpdates='all').execute()
            print(f"{event['summary']} is successfully booked..")
            return True

    except HttpError:
        print("Unfortunately that is an invalid event ID..")
        return False


def booked(service, email, event_id):
    """
    Prevents patient from double booking themselves
    :param service: Instance that allows that patient to book a slot
    :param email: User credentials helps with checks
    :param event_id: Event code that we use when we book a session
    :return: Boolean
    """
    n = 0
    now = datetime.datetime.utcnow()
    now = now.isoformat() + 'Z'
    page_token = None
    while True:
        events = service.events().list(calendarId='primary', timeMin=now
                                       , pageToken=page_token).execute()

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
                patient_email = ""

                if len(event['attendees']) == 2:
                    patient_email = event['attendees'][1]["email"]

                d_date = date.split('-')
                t_time = end_t.split(':')
                t_time = datetime.datetime(int(d_date[0]), int(d_date[1]), int(d_date[2]),
                                           int(t_time[0]), int(t_time[1]))
                s_start = start_c.split(':')
                s_start = datetime.datetime(int(d_date[0]), int(d_date[1]), int(d_date[2]),
                                            int(s_start[0]), int(s_start[1]))

                event = service.events().get(calendarId='primary', eventId=event_id).execute()

                event_2_time = event['start']['dateTime']

                event_2_time = str(event_2_time).split('T')

                date_two = event_2_time[0]
                event_2_time = str(event_2_time[1]).split('+')
                time = event_2_time[0]

                d_date = date.split('-')

                time_l = time.split(':')
                time_two = datetime.datetime(int(d_date[0]), int(d_date[1]), int(d_date[2]),
                                             int(time_l[0]), int(time_l[1]))

                start_two = start_c.split(':')
                start_two = datetime.datetime(int(d_date[0]), int(d_date[1]), int(d_date[2]),
                                              int(start_two[0]), int(start_two[1]))

                if email == patient_email:
                    clinician = admin.rstrip('@student.wethinkcode.co.za')
                    if s_start < time_two < t_time:
                        print(f"Failed to book because:\n- You will be consulted by {clinician} on {summary}"
                              f"\n- From {busy_time} until {end_t}")
                        n += 1
                        return True

                elif email == admin:
                    if s_start <= time_two <= t_time:
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

