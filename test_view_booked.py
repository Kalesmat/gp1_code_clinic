import unittest
import patient.patient_view_booking as patient
from code_clinic import startup

service = startup()
class test_booked(unittest.TestCase):
    
    def test_no_slots_booked(self):
        self.assertEqual(patient.view_booking(service,"ltemplem@student.wethinkcode.co.za"), "You have no booked slots")



    #need to add 1 more unit test 
    # def test_booked_slot(self):


if __name__ == "__main__":
    unittest.main()
