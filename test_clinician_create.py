import unittest
from clinician import create
from io import StringIO
import sys
from code_clinic import startup
import os
import sys
from unittest.mock import patch

class TestCase(unittest.TestCase):

    @patch('sys.stdin', StringIO('2020\n11\n18\n8\n0\n'))
    def test_create(self):
        """
        Testing the return of create.create()
        """
        orig_stdout = sys.stdout
        new_string = StringIO()
        sys.stdout = new_string
        service = startup()
        output = create.create(service)
        self.assertEqual("Event Created", output)
        sys.stdout = orig_stdout


if __name__ == "__main__":
    unittest.main()
