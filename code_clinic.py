from configparser import ConfigParser
from patient import cancel_booking, make_booking, view_booking, view_available
from clinician import create, delete, view_events
import pickle
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import sys
from colours import colour

SCOPES = ['https://www.googleapis.com/auth/calendar']


def startup():
    """
    Creates a service instance of the Google API and returns it
    :return: a service instance of the Google API
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_id.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service


def run_clinic():
    '''Function to run Code Clinic and parse through commands from user'''

    service = startup()
    home = os.path.expanduser("~")
    username, email, name = '', '', ''
    username = username.upper()

    if os.path.exists(f"{home}/.config.ini"):
        username, email, name = get_credentials(home)

    option_req_args = ['book', 'delete', 'cancel']
    valid_option = ['add','view_created', 'view_available', 'view_booked', 'config', 'version']
    uuid = None
    option = None

    # check if option was provided, if not default to help
    try:
        option = sys.argv[1]
    except IndexError as IndErr:
        pass

    # Check if provided option requires the uuid, if so and not provided, exit with a message
    if option in option_req_args:
        try:
            uuid = sys.argv[2]
        except IndexError as IndErr:
            print("This option requires a <uuid>")

    if option == 'help' or option == None:
        print(f"Welcome {name}\n")
        help()
        return True
    elif not option in option_req_args and not option in valid_option:
        print("An Invalid option was provided, redirected to \'help\'")
        help()
    elif option == 'version':
        version()

    '''Statements to handle args received from clinician'''

    if option == 'add' and os.path.exists(f"{home}/.config.ini"):
        print(f"Welcome {name}\n")
        create.create(service, name, email)

    elif option == 'delete' and uuid != None and os.path.exists(f"{home}/.config.ini"):
        print(f"Welcome {name}\n")
        delete.delete(service, email, uuid)

    elif option == 'view_created' and os.path.exists(f"{home}/.config.ini"):
        print(f"Welcome {name}\n")
        view_events.view(service,email)

    # Statements to handle args received from the patient

    elif option == 'view_available' and os.path.exists(f"{home}/.config.ini"):
        print(f"Welcome {name}\n")
        #If specific amount of days is provided as an argument then only those amount
        # of days will be displayed, else default is 7 days
        try:
            days_to_display = int(sys.argv[2])
            view_available.view_open_bookings(service, days_to_display)
        except IndexError as IndErr:
            days_to_display = 7
            view_available.view_open_bookings(service, days_to_display)
        except ValueError as ValErr:
            days_to_display = 7
            view_available.view_open_bookings(service, days_to_display)
    elif option == 'book' and uuid != None and os.path.exists(f"{home}/.config.ini"):
        print(f"Welcome {name}\n")
        make_booking.booking(service, username, email, uuid)

    elif option == 'view_booked' and os.path.exists(f"{home}/.config.ini"):
        print(f"Welcome {name}\n")
        view_booking.view_booking(service,email)

    elif option == 'cancel' and uuid != None and os.path.exists(f"{home}/.config.ini"):
        print(f"Welcome {name}\n")
        cancel_booking.cancel_booking(service, username, email, uuid)

    elif option == 'config':
        print("Welcome to Code Clinic")
        make_config(home)

    elif not os.path.exists(f"{home}/.config.ini"):
        print("\n")
        print('No config file please add a config file')
        print('Please run:\n> python3 code_clinic.py config')


def get_credentials(home):
    """
    Returns the user credentials from the config file
    :return: username and email
    """
    try:
        con_obj = ConfigParser()
        con_obj.read(f"{home}/.config.ini")
        credentials = con_obj['USERINFO']
        return credentials["username"], credentials["email"], credentials["name"]
    except KeyError:
        print("Redo config")
        return '', '', ''


def make_config(home):
    """
    Takes email and password from user and creates a config file for that user
    :return:
    """

    if os.path.exists("token2.pickle"):
        os.remove("token2.pickle")

    # Get configparser object
    con_obj = ConfigParser()

    # Get credentials from user
    mail = "@student.wethinkcode.co.za"
    users = get_users()
    username = input("Username: ")
    if username in users:
        email = username + mail

        service = request()
        mail = get_email(service)
        if email == mail:
            # Create a userinfo section in the config
            name = get_user_details(username)
            con_obj["USERINFO"] = {
                "username": username,
                "email": email,
                "name": name
            }

            # Write the section to config.ini file
            with open(f"{home}/.config.ini", "w") as con:
                con_obj.write(con)
            print("Config file create")
        else:
            print("You have given the wrong email")
            os.remove("token2.pickle")
    else:
        print("This username is not valid")


def request():
    """
    Responsible for requesting permission for this program to
    use the users student email
    :return: service instance of google api
    """
    creds = None
    if os.path.exists("token2.pickle"):
        with open("token2.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_id.json", SCOPES)
            creds = flow.run_local_server(port=0, prompt="consent"
                                          , authorization_prompt_message="")

        with open("token2.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build("calendar", "v3", credentials=creds)
    return service


def get_users():
    """
    Retrieves a list of usernames from the usernames file
    :return: a list of username strings
    """

    try:
        file = open("usernames", "r")
        user_file = file.readlines()
        users = []
        for i in user_file:
            users.append(i.split()[0])
        file.close()
        return users
    except FileNotFoundError:
        pass


def get_user_details(username):
    """
    Retrieves the name of the user from the usernames file
    :param username: username of the user
    :return: the name of the user
    """

    try:
        file = open("usernames", "r")
        user_file = file.readlines()
        name = ''
        for i in user_file:
            details = i.split()
            if username in details:
                name = details[1]
        return name
    except FileNotFoundError:
        pass


def get_email(service):
    """
    Uses the service instance to retrieve the email of the accounts primary calendar
    :param service: service instance that should be connected to the student email
    :return: email of the primary calendar
    """

    calendar_list_entry = service.calendarList().get(calendarId="primary").execute()
    return calendar_list_entry["summary"]


def help():
    '''Function should display the help menu
    if no options are provided or if help is called
    '''
    menu = '''*Volunteer and book slots for Code Clinic sessions.  

    Available options:

    help                    Display the help menu.
    config                  Run user configuration.
    version                 Display program version.
    add                     Add slot to calender as a volunteer.
    view_created            View volunteering slots that you have created.
    view_available          View slots available to book as a patient. You can optionally provide
                            the amount of days to view. Default is 7 days.
    view_booked             View slots you have booked as a patient.
    book <uuid>             Book an avalable slot as a patient.
    delete <uuid>           Delete a slot that you have volunteered for.
    cancel <uuid>           Cancel a slot that you have booked.'''
    menu = colour(menu, 'cyan')
    print(menu)


def version():
    '''Display the current version'''
    prog_version = 'Code_Clinic version: 1.0'
    print(prog_version)


if __name__ == '__main__':
    os.system('clear')
    run_clinic()
