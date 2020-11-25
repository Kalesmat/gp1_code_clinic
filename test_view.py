import unittest
from clinician import create
from io import StringIO
import sys
from code_clinic import startup
from code_clinic import get_credentials
from clinician import view_events

from io import StringIO
import sys

class TestViewEvents(unittest.TestCase):

    #to test if the user with the correct config file is able to view their events
    def test_valid_config(self):
        service = startup()
        
        email = get_credentials()[1]
        result= view_events.view(service,email)
        
        self.assertEqual(result, '----------------\n\
Code Clinic: List Comprehension created by moolivie@student.wethinkcode.co.za\n\
starts at 2020-12-16T09:30:00+02:00 and ends at 2020-12-16T10:00:00+02:00\n\
Id is: vkbf4q8qspfov2q9cr8ln87vro')

    # to test if the user with the no events volunteered is able to view events they did not create.
    def test_invalid_config(self):
        service = startup()

        email = get_credentials()[1]
        result = view_events.view(service, email)
       
        self.assertEqual(result, 'You have not volunteered')

if __name__ == '__main__':
    unittest.main()

