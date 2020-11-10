import unittest
from io import StringIO
from unittest.mock import patch
from configparser import ConfigParser
import code_clinic as cc


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


if __name__ == '__main__':
    unittest.main()