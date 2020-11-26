import unittest
from io import StringIO
from unittest.mock import patch
from configparser import ConfigParser
import code_clinic as cc
import os
import sys


class MyTestCase(unittest.TestCase):

    @patch('sys.stdin', StringIO('Dick\n'))
    @patch('getpass.getpass')
    def test_make_config(self, getpass):
        getpass.return_value = 'Harry'
        cc.make_config()
        config_object = ConfigParser()
        config_object.read(".config.ini")

        userinfo = config_object["USERINFO"]
        self.assertEqual(userinfo["email"], "Dick")
        self.assertEqual(userinfo["password"], "Harry")


    def test_run_clinic(self):
        '''Testing the run clinic function'''
        cc.sys.argv.append("-h") #appending the option to commandline

        std_output = sys.stdout
        output_value = StringIO()
        sys.stdout = output_value

        cc.run_clinic()
        output = sys.stdout.getvalue().strip()

        self.assertEqual(output,"""usage: Create and book slots for Code Clinics: -h or --help of list of options

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
  -q, --cancel_booking  Cancel booking.""")



if __name__ == '__main__':
    unittest.main()