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
        cc.sys.argv.append("-cd")

        std_output = sys.stdout
        output_value = StringIO()
        sys.stdout = output_value
        # output = os.system("python3 code_clinic.py -cd")
        # cc.create.create()HA
        cc.run_clinic()
        output = sys.stdout.getvalue().strip()

        self.assertEqual(output,"Welcome clinician\nEvent Deleted")



if __name__ == '__main__':
    unittest.main()