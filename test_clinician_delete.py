import unittest
from clinician import delete
from io import StringIO
from unittest.mock import patch
import sys
import code_clinic
from clinician import create


class TestCase(unittest.TestCase):

    @patch('sys.stdin', StringIO('2020\n12\n10\n13\n13\nKLM\nKLMKLM'))
    def do_create(self):
        service = code_clinic.startup()
        id = create.create(service)
        return id

    @patch('sys.stdin', StringIO(f'{id}\n'))
    def test_delete(self):
        """
        Testing the return of delete.delete()
        """
        service = code_clinic.startup()
        email = code_clinic.get_credentials()[1]
        orig_stdout = sys.stdout
        new_string = StringIO()
        sys.stdout = new_string
        output = delete.delete(service, email)
        self.assertEqual("Event Deleted", output)
        sys.stdout = orig_stdout


if __name__ == "__main__":
    unittest.main()