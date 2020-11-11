#!

import argparse
from configparser import ConfigParser
import getpass
from patient import patient_cancels_booking,patient_make_booking,patient_view_booking,patient_view_open_booking
from clinician import create, delete,view_events
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


def startup():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
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

    parser = argparse.ArgumentParser("Create and book slots for Code Clinics: -h or --help of list of options")

    parser.add_argument("--config", help="User configuration", action="store_true")
    parser.add_argument("-i","--version", help="Display program version", action="version", version=0.01)
    parser.add_argument("-c","--clinician", help="Use the system as clinician", action="store_true")
    parser.add_argument("-p","--patient", help="Use system as patient", action="store_true")
    parser.add_argument("-a","--add_slot", help="Add slot to calender(Clinician)", action="store_true")
    parser.add_argument("-b","--book", help="book avalable slot", action="store_true")
    parser.add_argument("-d","--delete", help="Delete slot", action="store_true")
    parser.add_argument("-r","--review", help="Review clinician", action="store_true")
    parser.add_argument("-v","--view_booked", help="View booked slots", action="store_true")
    parser.add_argument("-w","--view_available", help="View available slots", action="store_true")

    args = parser.parse_args() #Parsing argument received from the commandline

    '''Statements to handle args received from clinician'''

    if args.clinician and args.add_slot:
        print("Welcome clinician")
        create.create()
    elif args.clinician and args.delete:
        print("Welcome clinician")
        delete.delete()
    elif args.clinician and args.view_booked:
        print("Welcome clinician")
        view_events.view()

    '''Statements to handle args received form the patient'''

    if args.patient and args.view_available:
        print("Welcome patient")
        patient_view_open_booking.view_open_bookings(service)
    elif args.patient and args.book:
        print("Welcome patient")
        patient_make_booking.booking()
    elif args.patient and args.view_booked:
        print("Welcome patient")
        patient_view_booking.view_booking()
    elif args.patient and args.delete:
        print("Welcome patient")
        patient_cancels_booking.cancel_booking()
    elif args.config:
        make_config()
    
    #par = optparse.OptionParser()
    #par.add_option("-c", "--config", help="create a config file")
    #par.add_option("-q", "--quit", help="bye bye")

    #(options, args) = par.parse_args()
    # make_config()
    # pass


def make_config():
    """
    Takes email and password from user and creates a config file for that user
    :return:
    """

    # Get configparser object
    con_obj = ConfigParser()

    # Get credentials from user
    email = input("Email address: ")
    password = getpass.getpass()

    # Create a userinfo section in the config
    con_obj["USERINFO"] = {
        "email": email,
        "password": password
    }

    # Write the section to config.ini file
    with open(".config.ini", "w") as con:
        con_obj.write(con)


if __name__ == '__main__':
    run_clinic()