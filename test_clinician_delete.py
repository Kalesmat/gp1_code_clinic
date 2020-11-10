import unittest
from clinician import delete
from io import StringIO
import sys

class TestCase(unittest.TestCase):

    def test_create(self):
        """
        Testing the return of delete.delete()
        """
        orig_stdout = sys.stdout
        new_string = StringIO()
        sys.stdout = new_string
        output = delete.delete()
        self.assertEqual("Event Deleted", output)
        sys.stdout = orig_stdout


if __name__ == "__main__":
    unittest.main()