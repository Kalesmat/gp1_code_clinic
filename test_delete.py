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
        username, email, name = code_clinic.get_credentials()

        Summary = 'KLM'
        Description = 'klmno'
        startD = datetime.datetime.now().date() + datetime.timedelta(days=5)
        startT = '12:30'
        endT = '13:00'
        event = create.do_create(service,Summary,Description,startD
                                 ,startT,endT,username,email)
        event_id = event['id']
        orig_stdout = sys.stdout
        new_string = StringIO()
        sys.stdout = new_string
        delete.delete(service, email,event_id)
        output = sys.stdout.getvalue().strip()
        self.assertTrue("Event Deleted" in output)
        sys.stdout = orig_stdout

    def test_delete_false(self):
        service = code_clinic.startup()
        username, email, name = code_clinic.get_credentials()

        Summary = 'KLM'
        Description = 'klmno'
        startD = datetime.datetime.now().date() + datetime.timedelta(days=7)
        startT = '13:30'
        endT = '14:00'
        event = create.do_create(service,Summary,Description,startD
                                 ,startT,endT,username,email)
        event_id = event['id']
        email2 = f'not{email}'
        orig_stdout = sys.stdout
        new_string = StringIO()
        sys.stdout = new_string
        delete.delete(service, email2,event_id)
        output = sys.stdout.getvalue().strip()
        self.assertTrue('Your are not allowed to delete this event' in output)
        delete.do_delete(service, email, event_id)
        sys.stdout = orig_stdout

    def test_delete_invalid(self):
        service = code_clinic.startup()
        username, email, name = code_clinic.get_credentials()
        orig_stdout = sys.stdout
        new_string = StringIO()
        sys.stdout = new_string
        delete.delete(service, email,'tom')
        output = sys.stdout.getvalue().strip()
        self.assertTrue('Invalid ID' in output)
        sys.stdout = orig_stdout


if __name__ == "__main__":
    unittest.main()