import unittest
from patient import review
from io import StringIO
import sys

class TestCase(unittest.TestCase):

    def test_review(self):
        """
        Testing the return of create.create()
        """
        orig_stdout = sys.stdout
        new_string = StringIO()
        sys.stdout = new_string
        output = review.review()
        self.assertEqual("Event Created", output)
        sys.stdout = orig_stdout


if __name__ == "__main__":
    unittest.main()
