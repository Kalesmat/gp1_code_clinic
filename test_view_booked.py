import unittest
from clinician import create
from io import StringIO
import sys
from code_clinic import startup
import os
import sys
from unittest.mock import patch
import patient.patient_view_booking

service = startup()
class test_booked(unittest.TestCase):
    
    def test_booked(self):
        self.assertEqual(patient.patient_view_booking.view_booking(service,"ltemplem@student.wethinkcode.co.za"),"""----------------
Code Clinic: yeetus by jmotebej@student.wethinkcode.co.za
starts at 2020-11-28T12:00:00+02:00 and ends at 2020-11-28T12:30:00+02:00
Id is: 618hhpv0bro56h0o01bf0eubsc """)

    def test_wrongbooked(self):
        self.assertNotEqual(patient.patient_view_booking.view_booking(service,"ltemplem@student.wethinkcode.co.za"),"""----------------
Code Clinic: yeetus by jmotebej@student.wethinkcode.co.za
starts at 2020-11-28T12:00:00+02:00 and ends at 2020-11-28T12:30:00+02:
Id is: 618hhpv0bro56h0o01bf0eubsc """)
if __name__ == "__main__":
    unittest.main()