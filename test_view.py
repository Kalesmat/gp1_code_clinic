import unittest
from clinician import view_events
from io import StringIO
import sys

class TestViewEvents(unittest.TestCase):

    def test_view(self):
        '''Test if function returns a set of booked events.'''
        orig_stdout = sys.stdout
        new_string = StringIO()
        sys.stdout = new_string
        result = view_events.view()
        self.assertTrue(type(result), set)
        sys.stdout = orig_stdout

    def test_view_result(self):
        '''Test if function resturn the actual list of booked events.'''
        orig_stdout = sys.stdout
        new_string = StringIO()
        sys.stdout = new_string
        result=view_events.view()
        self.assertEqual(result, "['Recursion ', ' Luke', '11/11/2020', '14:30']")
        sys.stdout = orig_stdout



if __name__ == '__main__':
    unittest.main()
