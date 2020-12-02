import unittest
from io import StringIO
from unittest.mock import patch
from configparser import ConfigParser
import code_clinic as cc
import sys
from os import system
import contextlib


class MyTestCase(unittest.TestCase):

    @patch('sys.stdin', StringIO('y\nTOm@\n.com\nTom'))
    @patch('getpass.getpass')
    def test_make_config(self, getpass):
        getpass.return_value = 'Harry'
        cc.make_config()
        config_object = ConfigParser()
        config_object.read(".config.ini")

        userinfo = config_object["USERINFO"]
        self.assertEqual(userinfo["email"], "tom@student.wethinkcode.co.za")
        self.assertEqual(userinfo["password"], "Harry")
        self.assertEqual(userinfo["username"], 'tom')


    def test_run_clinic(self):
        '''Testing the run clinic function'''
        output = StringIO()
        with contextlib.redirect_stdout(output):
            system("python3 code_clinic.py")
        self.assertTrue(output,"""usage: Create and book slots for Code Clinics: -h or --help of list of options

       [-h] [-c] [-v] [-a] [-b] [-d] [-s] [-i] [-w] [-q]

optional arguments:
  -h, --help            show this help message and exit
  -c, --config          User configuration
  -v, --version         Display program version
  -a, --add_slot        Add slot to calender.
  -b, --book            book avalable slot.
  -d, --delete          Delete slot.
  -s, --view_created    See slots created.
  -i, --view_booked     View booked slots.
  -w, --view_available  View available slots.
  -q, --cancel_booking  Cancel booking.""" in output.getvalue())

if __name__ == '__main__':
    unittest.main()



        # # cc.sys.argv.append("-h") #appending the option to commandline
        # system("python3 code_clinic.py")
        # # cc.run_clinic()
        # std_output = sys.stdout
        # output_value = StringIO()
        # sys.stdout = output_value
        # sys.stdout = system("python3 code_clinic.py")
        # output = sys.stdout.getvalue().strip()
        # print(output)
#         self.assertEqual(output,"""usage: Create and book slots for Code Clinics: -h or --help of list of options

#        [-h] [-c] [-v] [-a] [-b] [-d] [-s] [-i] [-w] [-q]

# optional arguments:
#   -h, --help            show this help message and exit
#   -c, --config          User configuration
#   -v, --version         Display program version
#   -a, --add_slot        Add slot to calender.
#   -b, --book            book avalable slot.
#   -d, --delete          Delete slot.
#   -s, --view_created    See slots created.
#   -i, --view_booked     View booked slots.
#   -w, --view_available  View available slots.
#   -q, --cancel_booking  Cancel booking.""")