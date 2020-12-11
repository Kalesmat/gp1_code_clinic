import io
import sys
import unittest
import patient.patient_view_booking as patient
from code_clinic import startup


service = startup()
class test_booked(unittest.TestCase):


    def test_no_slots_booked(self):
        patient.n = 0
        suppress_text = io.StringIO()
        sys.stdout = suppress_text 
   
        self.assertEqual(patient.view_booking(service,"ltemplem@student.wethinkcode.co.za"), "You have no booked slots\n")
        sys.stdout = sys.__stdout__


    def test_1_booked_slot(self):
        suppress_text = io.StringIO()
        sys.stdout = suppress_text 
        patient.n = 1
        self.assertEqual(patient.view_booking(service,"ltemplem@student.wethinkcode.co.za"), "\nYou have 1 booked slot\n")
        patient.n = 0
        sys.stdout = sys.__stdout__

    def test_2_booked_slots(self):
        suppress_text = io.StringIO()
        sys.stdout = suppress_text 
        patient.n = 2
        self.assertEqual(patient.view_booking(service,"ltemplem@student.wethinkcode.co.za"), "\nYou have 2 booked slots\n")
        patient.n = 0 
        sys.stdout = sys.__stdout__
    
    def test_20_booked_slots(self):
        suppress_text = io.StringIO()
        sys.stdout = suppress_text 
        patient.n = 20
        self.assertEqual(patient.view_booking(service,"ltemplem@student.wethinkcode.co.za"), "\nYou have 20 booked slots\n")
        patient.n = 0 
        sys.stdout = sys.__stdout__

if __name__ == "__main__":
    unittest.main()

