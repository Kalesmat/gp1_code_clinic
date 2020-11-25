import unittest
from clinician import delete
from io import StringIO
import sys
import code_clinic
from clinician import create


class TestCase(unittest.TestCase):

    def test_delete_true(self):
        """
        Testing the return of delete.delete()
        """
        service = code_clinic.startup()
        username, email = code_clinic.get_credentials()

        Summary = 'KLM'
        Description = 'klmno'
        startD = '2020-11-30'
        hour = 15
        Min = 20
        hour2 = hour
        min2 = Min + 30
        event = create.do_create(service, Summary, Description, startD, hour, Min, hour2, min2, username, email)
        event_id = event['id']
        orig_stdout = sys.stdout
        new_string = StringIO()
        sys.stdout = new_string
        output = delete.do_delete(service, email, event_id)
        self.assertEqual("Event Deleted", output)
        sys.stdout = orig_stdout


if __name__ == "__main__":
    unittest.main()