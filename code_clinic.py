import optparse
from configparser import ConfigParser


def run_clinic():
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
    password = input("Password: ")

    # Create a userinfo section in the config
    con_obj["USERINFO"] = {
        "email": email,
        "password": password
    }

    # Write the section to config.ini file
    with open("config.ini", "w") as con:
        con_obj.write(con)


if __name__ == '__main__':
    run_clinic()