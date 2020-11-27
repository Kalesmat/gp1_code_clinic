import unittest
from unittest.mock import patch
from io import StringIO
from clinician import create
from patient import patient_view_open_booking
from code_clinic import startup

class TestPatientAvailableView(unittest.TestCase):

    @patch('sys.stdin', StringIO('07/12/2020\n09:30\nUnittest\nGoing through unittest basics\n'))
    def test_view_available(self):

        '''
        Test whether user can view a slot that has been made available
        '''
        service = startup()
        username, email = 'ikalonji', 'ikalonji@student.wethinkcode.co.za'
        create.create(service, username, email)
        events = patient_view_open_booking.view_open_bookings(service)
        self.assertTrue(events==True, 'Not true')

if __name__ == "__main__":
    unittest.main()



