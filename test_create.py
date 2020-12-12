import unittest
from clinician import create, delete
from io import StringIO
import code_clinic
import sys
from unittest.mock import patch
import datetime
import os

class TestCase(unittest.TestCase):

    def test_create_wrong_date(self):
        """
        Test Create function if the date is older than now
        """
        service = code_clinic.startup()
        home = os.path.expanduser("~")
        username, email, name = code_clinic.get_credentials(home)        
        
        testdate="01/01/01"
        with patch('sys.stdin', StringIO(f'{testdate}\n')):
            orig_stdout = sys.stdout
            new_string = StringIO()
            sys.stdout = new_string
            create.create(service,username, email)
            output = sys.stdout.getvalue().strip()
            self.assertTrue(f"Bye {username}",output)
            sys.stdout = orig_stdout

        
    def test_create_y(self):
        """
        Test Create function for confirming the creation of an event for y
        """
        service = code_clinic.startup()
        home = os.path.expanduser("~")
        username, email, name = code_clinic.get_credentials(home)
        
        summary = 'Test_create'
        descript = 'Test function create'
        startdate = datetime.datetime.now().date() + datetime.timedelta(days=5)
        starttime = '12:30'        
        
        testdate=str(startdate.day)+"/"+str(startdate.month)+"/"+\
            str(startdate.year)
        with patch('sys.stdin', StringIO(f'{testdate}\n{starttime}\n\
            {summary}\n{descript}\ny\n')):
            orig_stdout = sys.stdout
            new_string = StringIO()
            sys.stdout = new_string
            event_id = create.create(service,username, email)
            output = sys.stdout.getvalue().strip()
            self.assertTrue("Event created",output)
            delete.do_delete(service, email, event_id)
            sys.stdout = orig_stdout


    def test_create_n(self):
        """
        Test Create function for confirming the creation of an event for n
        """
        service = code_clinic.startup()
        home = os.path.expanduser("~")
        username, email, name= code_clinic.get_credentials(home)

        summary = 'Test_create'
        descript = 'Test function create'
        startdate = datetime.datetime.now().date() + datetime.timedelta(days=5)
        starttime = '12:30'
                
        
        testdate=str(startdate.day)+"/"+str(startdate.month)+"/"+\
            str(startdate.year)
        with patch('sys.stdin', StringIO(f'{testdate}\n{starttime}\n{summary}\
            \n{descript}\nn\n')):
            orig_stdout = sys.stdout
            new_string = StringIO()
            sys.stdout = new_string
            event_id = create.create(service,username, email)
            output = sys.stdout.getvalue().strip()
            self.assertTrue("Event not created",output)
            delete.do_delete(service, email, event_id)
            sys.stdout = orig_stdout

    

if __name__ == "__main__":
    unittest.main()
