import argparse
from configparser import ConfigParser
import getpass


def run_clinic():
    '''Function to run Code Clinic and parse through commands from user'''
    
    parser = argparse.ArgumentParser(" Create and book slots for Code Clinics")

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

    args = parser.parse_args()
    if args.clinician:
        print("Welcome clinician")
    elif args.patient:
        print("Welcome patient")
    elif args.add_slot:
        print("Adding a slot")
    elif args.book:
        print("Booking slot")
    elif args.delete:
        print("Deleting slot")
    elif args.review:
        print("Reviewing clinician")
    elif args.view_booked:
        print("Viewing booked slots")
    elif args.view_available:
        print("Viewing available slots")
    elif args.config:
        make_config()
    
    #par = optparse.OptionParser()
    #par.add_option("-c", "--config", help="create a config file")
    #par.add_option("-q", "--quit", help="bye bye")

    #(options, args) = par.parse_args()
    make_config()
    pass


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