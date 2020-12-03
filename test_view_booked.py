import unittest
import patient.patient_view_booking as patient
from code_clinic import startup
# import 

service = startup()
class test_booked(unittest.TestCase):


    def test_no_slots_booked(self):
        self.assertEqual(patient.view_booking(service,"ltemplem@student.wethinkcode.co.za"), "You have no booked slots")
   

    def test_1_booked_slot(self):
        patient.n = 1
        self.assertEqual(patient.view_booking(service,"ltemplem@student.wethinkcode.co.za"), "\nYou have 1 booked slot")
        patient.n = 0


    def test_2_booked_slots(self):
        patient.n = 2
        self.assertEqual(patient.view_booking(service,"ltemplem@student.wethinkcode.co.za"), "\nYou have 2 booked slots")
        patient.n = 0 

    
    def test_20_booked_slots(self):
        patient.n = 20
        self.assertEqual(patient.view_booking(service,"ltemplem@student.wethinkcode.co.za"), "\nYou have 20 booked slots")
        patient.n = 0 


if __name__ == "__main__":
    unittest.main()