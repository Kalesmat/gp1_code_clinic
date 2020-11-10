import unittest
import view_events
from io import StringIO

class TestViewEvents(unittest.TestCase):

    def test_view(self):
        '''Test if function returns a set of booked events.'''
        result = view_events.view()
        self.assertTrue(type(result), set)

    def test_view_result(self):
        '''Test if function resturn the actual list of booked events.'''
        result=view_events.view()
        self.assertEqual(result, "[('Recursion ', ' Luke', '11/11/2020', '14:30')]")
