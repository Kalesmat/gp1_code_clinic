import unittest
from clinician import delete
from io import StringIO
import sys
import code_clinic
from clinician import create
import datetime


class TestCase(unittest.TestCase):

    def test_delete_true(self):
        service = code_clinic.startup()
        username, email = code_clinic.get_credentials()

        Summary = 'KLM'
        Description = 'klmno'
        startD = datetime.datetime.now().date() + datetime.timedelta(days=4)
        startT = '12:30'
        endT = '13:00'
        event = create.do_create(service,Summary,Description,startD,startT,endT,username,email)
        event_id = event['id']
        orig_stdout = sys.stdout
        new_string = StringIO()
        sys.stdout = new_string
        output = delete.do_delete(service, email, event_id)
        self.assertEqual("Event Deleted", output)
        sys.stdout = orig_stdout

    def test_delete_false(self):
        service = code_clinic.startup()
        username, email = code_clinic.get_credentials()

        Summary = 'KLM'
        Description = 'klmno'
        startD = datetime.datetime.now().date() + datetime.timedelta(days=4)
        startT = '12:30'
        endT = '13:00'
        event = create.do_create(service,Summary,Description,startD,startT,endT,username,'L@m.com')
        event_id = event['id']
        orig_stdout = sys.stdout
        new_string = StringIO()
        sys.stdout = new_string
        output = delete.do_delete(service, 'k@m.com', event_id)
        self.assertEqual('Your are not allowed to delete this event', output)
        sys.stdout = orig_stdout


if __name__ == "__main__":
    unittest.main()