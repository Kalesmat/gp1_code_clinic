import unittest
from clinician import create
from io import StringIO
import sys
# from code_clinic import startup
import code_clinic
import os
import sys
from unittest.mock import patch
import datetime


class TestCase(unittest.TestCase):

    def test_create_wrong_date_n(self):
        service = code_clinic.startup()
        username, email = code_clinic.get_credentials()

        Summary = 'Test_create'
        Descript = 'Test function create'
        # startD = datetime.datetime.now().date() + datetime.timedelta(days=5)
        startT = '12:30'        
        
        TestD="01/01/01"
        with patch('sys.stdin', StringIO(f'{TestD}\nn\n')):
            orig_stdout = sys.stdout
            new_string = StringIO()
            sys.stdout = new_string
            create.create(service,username, email)
            output = sys.stdout.getvalue().strip()
            self.assertTrue(f"Bye {username}" in output)
            sys.stdout = orig_stdout

        
    def test_create_y(self):
        service = code_clinic.startup()
        username, email = code_clinic.get_credentials()

        Summary = 'Test_create'
        Descript = 'Test function create'
        startD = datetime.datetime.now().date() + datetime.timedelta(days=5)
        startT = '12:30'        
        
        TestD=str(startD.day)+"/"+str(startD.month)+"/"+str(startD.year)
        with patch('sys.stdin', StringIO(f'{TestD}\n{startT}\n{Summary}\n{Descript}\ny\n')):
            orig_stdout = sys.stdout
            new_string = StringIO()
            sys.stdout = new_string
            create.create(service,username, email)
            output = sys.stdout.getvalue().strip()
            self.assertTrue("Event Created" in output)
            sys.stdout = orig_stdout

    def test_create_n(self):
        service = code_clinic.startup()
        username, email = code_clinic.get_credentials()

        Summary = 'Test_create'
        Descript = 'Test function create'
        startD = datetime.datetime.now().date() + datetime.timedelta(days=5)
        startT = '12:30'
        endT = '13:00'
        # event = create.do_create(service,Summary,Description,startD,startT,endT,username,email)
        # event_id = event['id']
        
        TestD=str(startD.day)+"/"+str(startD.month)+"/"+str(startD.year)
        with patch('sys.stdin', StringIO(f'{TestD}\n{startT}\n{Summary}\n{Descript}\nn\n')):
            orig_stdout = sys.stdout
            new_string = StringIO()
            sys.stdout = new_string
            create.create(service,username, email)
            output = sys.stdout.getvalue().strip()
            self.assertTrue("you have not created the event" in output)
            sys.stdout = orig_stdout

    # def test_do_create(self):
    #     """
    #     Testing the return of create.do_create()
    #     """
        
    #     # orig_stdout = sys.stdout
    #     # new_string = StringIO()
    #     # sys.stdout = new_string

    #     user, email = code_clinic.get_credentials()
    #     day = datetime.datetime.now().date() + datetime.timedelta(days=4)
    #     # day = day.isoformat() + 'Z'
    #     print(day)
    #     sum = "Testing do_Create"
    #     des = "Using datetime"


    #     ser = code_clinic.startup()
    #     output=create.do_create(ser,sum,des,day,"12:00","12:30",user,email)
    #     print(output)
        
    


if __name__ == "__main__":
    unittest.main()
