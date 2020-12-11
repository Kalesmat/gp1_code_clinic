import unittest
from unittest.mock import patch
from io import StringIO
from clinician import create
from patient import view_available
from code_clinic import startup
import sys

class TestPatientAvailableView(unittest.TestCase):

    @patch('sys.stdin', StringIO('07/12/2020\n09:30\nUnittest\nGoing through unittest basics\ny\n'))
    def test_view_available(self):

        '''
        Test whether user can view a slot that has been made available
        '''
        orig_stdout = sys.stdout
        new_string = StringIO()
        sys.stdout = new_string
        service = startup()
        username, email = 'ikalonji', 'ikalonji@student.wethinkcode.co.za'
        create.create(service, username, email)
        days_to_display = 7
        events = view_available.view_open_bookings(service, days_to_display)
        self.assertTrue(events==True, 'Not true')
        sys.stdout = orig_stdout

if __name__ == "__main__":
    unittest.main()



