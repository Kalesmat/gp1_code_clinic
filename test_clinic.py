import unittest
from io import StringIO
from os import system
import contextlib


class MyTestCase(unittest.TestCase):

    def test_run_clinic(self):
        '''Testing the run clinic function'''
        
        output = StringIO()
        with contextlib.redirect_stdout(output):
            
            system("python3 code_clinic.py")
            print("hello")
        self.assertTrue(output,"""*Volunteer and book slots for Code Clinic sessions.  
    
    Available options:

    help                    Display the help menu.
    config                  Run user configuration.
    version                 Display program version.
    add_slot                Add slot to calender as a volunteer.
    view_created            View volunteering slots that you have created.
    view_available          View slots available to book as a patient.
    view_booked             View slots you have booked as a patient.
    book <uuid>             Book an avalable slot as a patient.
    delete <uuid>           Delete a slot that you have volunteered for.
    cancel <uuid>           Cancel a slot that you have booked.""" in output.getvalue())

if __name__ == '__main__':
    unittest.main()
