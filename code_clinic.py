from configparser import ConfigParser
import getpass
from patient import patient_cancels_booking, patient_make_booking, patient_view_booking, patient_view_open_booking
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

    username, email = '', ''
    username = username.upper()

    if os.path.exists('.config.ini'):
        username, email = get_credentials()

    # parser = argparse.ArgumentParser("Create and book slots for Code Clinics: -h or --help of list of options\n")

    # parser.add_argument("-c","--config", help="User configuration", action="store_true")
    # parser.add_argument("-v","--version", help="Display program version", action="version", version='version 0.01')
    # parser.add_argument("-a","--add_slot", help="Add slot to calender.", action="store_true")
    # parser.add_argument("-b","--book", help="book avalable slot.", action="store_true")
    # parser.add_argument("-d","--delete", help="Delete slot.", action="store_true")
    # parser.add_argument("-s","--view_created", help="See slots created.", action="store_true")
    # parser.add_argument("-i","--view_booked", help="View booked slots.", action="store_true")
    # parser.add_argument("--view_available", help="View available slots.", action="store_true")
    # parser.add_argument("-q","--cancel_booking", help="Cancel booking.", action="store_true")
    option_req_args = ['book', 'delete', 'cancel']
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
        print(f"Welcome {username}")
        help()
        # parser.print_help()
        return True
    elif option == 'version':
        version()
        # args = parser.parse_args() #Parsing argument received from the commandline

    '''Statements to handle args received from clinician'''

    if option == 'add_slot' and os.path.exists('.config.ini'):
        print(f"Welcome {username}")
        create.create(service, username, email)

    elif option == 'delete' and uuid != None and os.path.exists('.config.ini'):
        print(f"Welcome {username}")
        delete.delete(service, email, uuid)

    elif option == 'view_created' and os.path.exists('.config.ini'):
        print(f"Welcome {username}")
        view_events.view(service, email)

    # Statements to handle args received form the patient

    elif option == 'view_available' and os.path.exists('.config.ini'):
        print(f"Welcome {username}")
        patient_view_open_booking.view_open_bookings(service)

    elif option == 'book' and uuid != None and os.path.exists('.config.ini'):
        print(f"Welcome {username}")
        patient_make_booking.booking(service, username, email, uuid)

    elif option == 'view_booked' and os.path.exists('.config.ini'):
        print(f"Welcome {username}")
        patient_view_booking.view_booking(service, email)

    elif option == 'cancel_booking' and uuid != None and os.path.exists('.config.ini'):
        print(f"Welcome {username}")
        patient_cancels_booking.cancel_booking(service, username, email, uuid)

    elif option == 'config':
        print("Welcome to Code Clinic")
        make_config()

    elif not os.path.exists('.config.ini'):
        print("\n")
        print('No config file please add a config file')
        print('Please run:\n> python3 code_clinic.py --config')


def get_credentials():
    """
    Returns the user credentials from the config file
    :return: username and email
    """
    try:
        con_obj = ConfigParser()
        con_obj.read('.config.ini')
        credentials = con_obj['USERINFO']
        return credentials['username'], credentials['email']
    except KeyError:
        print('Redo config')


def make_config():
    """
    Takes email and password from user and creates a config file for that user
    :return:
    """

    # Get configparser object
    con_obj = ConfigParser()

    # Get credentials from user
    while True:
        status = input('Are you a student [y/n]?: ').strip()
        if status.lower() == 'n':
            mail = '@wethinkcode.co.za'
            break
        if status.lower() == 'y':
            mail = '@student.wethinkcode.co.za'
            break

    while True:
        username = input("Username: ").strip()
        if '@' in username or '.' in username:
            print('Not a valid username')
        else:
            break

    email = username + mail

    # Create a userinfo section in the config
    password = getpass.getpass()
    con_obj["USERINFO"] = {
        "username": username.lower(),
        "email": email.lower(),
        "password": password
    }

    # Write the section to config.ini file
    with open(".config.ini", "w") as con:
        con_obj.write(con)
        print('Config file created successfully')


def help():
    '''Function should display the help menu
    if no options are provided or if help is called
    '''
    menu = '''*Volunteer and book slots for Code Clinic sessions.  

    Available options:

    help                    Display the help menu.
    config                  Run user configuration.
    version                 Display program version.
    add_slot                Add slot to calender as a volunteer.
    view_created            View volunteering slots that you have created.
    view_available          View slots available to book as a patient.
    view_booked             View slots you have booked as a patient.
    book <uuid>             Book an avalable slot as a patient.
    delete <uuid>           Delete a slot that you have volunteered for.
    cancel <uuid>           Cancel a slot that you have booked.'''
    menu = colour(menu, 'cyan')
    print(menu)


def version():
    '''Display the current version'''
    prog_version = 'Code_Clinic version: 0.6'
    print(prog_version)


if __name__ == '__main__':
    os.system('clear')
    run_clinic()
