#!

import argparse
from configparser import ConfigParser
import getpass
from patient import patient_cancels_booking,patient_make_booking,patient_view_booking,patient_view_open_booking,review
from clinician import create, delete,view_events
import pickle
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import sys

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

    parser = argparse.ArgumentParser("Create and book slots for Code Clinics: -h or --help of list of options\n")

    parser.add_argument("-c","--config", help="User configuration", action="store_true")
    parser.add_argument("-v","--version", help="Display program version", action="version", version='version 0.01')
    parser.add_argument("-a","--add_slot", help="Add slot to calender.", action="store_true")
    parser.add_argument("-b","--book", help="book avalable slot.", action="store_true")
    parser.add_argument("-d","--delete", help="Delete slot.", action="store_true")
    parser.add_argument("-s","--view_created", help="See slots created.", action="store_true")
    parser.add_argument("-i","--view_booked", help="View booked slots.", action="store_true")
    parser.add_argument("-w","--view_available", help="View available slots.", action="store_true")
    parser.add_argument("-q","--cancel_booking", help="Cancel booking.", action="store_true")

    if len(sys.argv) < 2:
        print("Welcome to Code Clinic")
        parser.print_help()
    
    args = parser.parse_args() #Parsing argument received from the commandline

    '''Statements to handle args received from clinician'''


    if args.add_slot and os.path.exists('.config.ini'):
        print("Welcome clinician")
        create.create(service)
    elif args.delete and os.path.exists('.config.ini'):
        print("Welcome clinician")
        delete.delete(service)
    elif args.view_created and os.path.exists('.config.ini'):
        print("Welcome clinician")
        view_events.view(service)

    #Statements to handle args received form the patient

    elif args.view_available and os.path.exists('.config.ini'):
        print("Welcome patient")
        patient_view_open_booking.view_open_bookings(service)
    elif args.book and os.path.exists('.config.ini'):
        print("Welcome patient")
        patient_make_booking.booking(service)
    elif args.view_booked and os.path.exists('.config.ini'):
        print("Welcome patient")
        patient_view_booking.view_booking(service)
    elif args.cancel_booking and os.path.exists('.config.ini'):
        print("Welcome patient")
        patient_cancels_booking.cancel_booking(service)
    elif args.config:
        print("Welcome to Code Clinic")
        make_config()
    elif not os.path.exists('.config.ini'):
        print("\n")
        print('No config file please add a config file')
        print('Please run:\n> python3 code_clinic.py --config')
    # elif args.review and os.path.exists('.config.ini'):
    #     review.review(service)


def get_credentials():
    """
    Returns the user credentials from the config file
    :return: username and email
    """
    con_obj = ConfigParser()
    con_obj.read('.config.ini')
    credentials = con_obj['USERINFO']
    return credentials['username'], credentials['email']


def make_config():
    """
    Takes email and password from user and creates a config file for that user
    :return:
    """

    # Get configparser object
    con_obj = ConfigParser()

    # Get credentials from user
    status = input('Are you a student [y/n]?: ')
    mail = '@wethinkcode.co.za'
    if status.lower() == 'y':
        mail = '@student.wethinkcode.co.za'
    username = input("Username?: ")
    email = username + mail

    # Create a userinfo section in the config
    password = getpass.getpass()
    con_obj["USERINFO"] = {
        "username": username,
        "email": email,
        "password": password
    }

    # Write the section to config.ini file
    with open(".config.ini", "w") as con:
        con_obj.write(con)
        print('Config file created successfully')


if __name__ == '__main__':
    run_clinic()