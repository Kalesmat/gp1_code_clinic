import unittest
from clinician import create
from io import StringIO
import sys

class TestCase(unittest.TestCase):

    def test_create(self):
        """
        Testing the return of create.create()
        """
        orig_stdout = sys.stdout
        new_string = StringIO()
        sys.stdout = new_string
        output = create.create()
        self.assertEqual("Event Created", output)
        sys.stdout = orig_stdout


if __name__ == "__main__":
    unittest.main()