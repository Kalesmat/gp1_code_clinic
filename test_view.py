import unittest
from clinician import create
from io import StringIO
import sys
from code_clinic import startup
from code_clinic import get_credentials
from clinician import view_events
from clinician import create
from clinician import delete
from io import StringIO
import sys
import datetime

class TestViewEvents(unittest.TestCase):
    #test if the user has slots opened
    def test_did_not_volunteer(self):
        service = startup()

        email = 'moolivi@student.wethinkcode.co.za'
        orig_stdout = sys.stdout
        new_string = StringIO()
        sys.stdout = new_string
        result = view_events.view(service, email)
       
        self.assertEqual(result, 'You have not volunteered')
        sys.stdout = orig_stdout
    # checks if user is able to view their events by creating an event and then testing for it
    def test_valid_user_event(self):
        service=startup()
        user='moolivie'
        email='moolivie@student.wethinkcode.co.za'
        Date = datetime.datetime.now().date() + datetime.timedelta(days=5)
        summary = "Morglin Test Case"
        Descript = "Testing"
        orig_stdout = sys.stdout
        new_string = StringIO()
        sys.stdout = new_string
        event=create.do_create(service,summary,Descript,Date,"12:00","12:30",user,email,'y')
        
        result = view_events.view(service, email)

        self.assertEqual(result, "You have Volunteered")
        id = event['id']

        deleting = delete.do_delete(service, email, id)

        sys.stdout = orig_stdout

       
if __name__ == '__main__':
    unittest.main()



