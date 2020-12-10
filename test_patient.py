import unittest
from io import StringIO
import sys
import code_clinic
from clinician import create
import datetime
from patient import patient_make_booking, patient_cancels_booking, patient_view_booking, patient_view_open_booking


# for booking

summary = 'Testing for unittests Booking.'
description = 'Test booking and cancelling with the unittest as summary'
start_d = datetime.datetime.now().date() + datetime.timedelta(hours=24)
start_t = '10:00'
end_t = '10:30'

# functions that help with testing for booking and cancellations

service = code_clinic.startup()
creator, admin = "Fake Creator", "fake.creator@gmail.com"
create_slot = create.do_create(service, summary, description, start_d, start_t, end_t, creator, admin)
test_id = create_slot['id']


class PatientTest(unittest.TestCase):
    def test_patient_make_booking(self):
        the_stdout = sys.stdout
        new_string = StringIO()
        sys.stdout = new_string
        username, email = "Booker", "fake.booking@gmail.com"
        book = patient_make_booking.booking(service, username, email, test_id)
        test_result = f"{summary} is successfully booked.."
        self.assertTrue(book, test_result)
        service.events().delete(calendarId='primary', eventId=test_id).execute()
        sys.stdout = the_stdout

    def test_patient_make_double_booking(self):
        the_stdout = sys.stdout
        new_string = StringIO()
        sys.stdout = new_string
        username, email = "Booker", "fake.booking@gmail.com"
        book = patient_make_booking.booking(service, username, email, test_id)
        test_result = f"{username}, number of attendees has been reached, please check for the next slot."
        self.assertTrue(book, test_result)
        sys.stdout = the_stdout

    def test_patient_make_booking_if_is_volunteer(self):
        the_stdout = sys.stdout
        new_string = StringIO()
        sys.stdout = new_string
        username, email = "Fake Creator", "fake.creator@gmail.com"
        book = patient_make_booking.booking(service, username, email, test_id)
        test_result = f'{username}, Unfortunately you cannot book your own event..'
        self.assertTrue(book, test_result)
        sys.stdout = the_stdout

    def test_patient_make_booking_invalid_eventid(self):
        the_stdout = sys.stdout
        new_string = StringIO()
        sys.stdout = new_string
        username, email = "Booker", "fake.booking@gmail.com"
        book = patient_make_booking.booking(service, username, email, "y0hI@mFak3eee33")
        test_result = "Unfortunately that is an invalid event ID.."
        self.assertFalse(book, test_result)
        sys.stdout = the_stdout

    def test_patient_make_booking_empty(self):
        the_stdout = sys.stdout
        new_string = StringIO()
        sys.stdout = new_string
        username, email = "Booker", "fake.booking@gmail.com"
        book = patient_make_booking.booking(service, username, email, 'None')
        test_result = "Unfortunately that is an invalid event ID.."
        self.assertFalse(book, test_result)
        sys.stdout = the_stdout

    def test_patient_booked(self):
        the_stdout = sys.stdout
        new_string = StringIO()
        sys.stdout = new_string
        username, email = "Booker", "fake.booking@gmail.com"
        booked = patient_make_booking.booked(service, email, test_id)
        test_result = f"Failed to book because:\n- You will be consulted by {admin} on {summary}" \
                      f"\n- From {start_t} until {end_t}"
        self.assertFalse(booked, test_result)
        sys.stdout = the_stdout

    def test_clinician_with_a_slot_same_as_patient_booked(self):
        the_stdout = sys.stdout
        new_string = StringIO()
        sys.stdout = new_string
        username, email = "Booker", "fake.booking@gmail.com"
        created = create_slot
        booked = patient_make_booking.booked(service, email, test_id)
        test_result = f"Failed to book because:\n- You are a clinician on {summary}" \
                      f"\n- From {start_t} until {end_t}"
        self.assertTrue(created, booked)
        self.assertFalse(booked, test_result)
        sys.stdout = the_stdout

    def test_patient_cancels_booking(self):
        the_stdout = sys.stdout
        new_string = StringIO()
        sys.stdout = new_string
        username, email = "Booker", "fake.booking@gmail.com"
        cancel = patient_cancels_booking.cancel_booking(service, username, email, test_id)
        test_result = f"{username}, You have successfully cancelled your booking."
        self.assertTrue(cancel, test_result)
        service.events().delete(calendarId='primary', eventId=test_id).execute()
        sys.stdout = the_stdout

    def test_patient_cancels_booking_my_events_is_none(self):
        the_stdout = sys.stdout
        new_string = StringIO()
        sys.stdout = new_string
        username, email = "Booker", "fake.booking@gmail.com"
        my_events = patient_view_booking.view_booking(service, admin)
        cancel = patient_cancels_booking.cancel_booking(service, username, email, my_events)
        self.assertFalse(cancel, my_events is False)
        sys.stdout = the_stdout

    def test_patient_cancels_booking_if_event_is_other_patients(self):
        the_stdout = sys.stdout
        new_string = StringIO()
        sys.stdout = new_string
        username, email = "Booker", "fake.booking@gmail.com"
        events = patient_view_open_booking.view_open_bookings(service)
        cancel = patient_cancels_booking.cancel_booking(service, username, email, events)
        test_result = f"{username}, You are not the attendee on this event."
        self.assertFalse(cancel, test_result)
        sys.stdout = the_stdout

    def test_patient_cancels_booking_invalid_eventid(self):
        the_stdout = sys.stdout
        new_string = StringIO()
        sys.stdout = new_string
        username, email = "Booker", "fake.booking@gmail.com"
        cancel = patient_cancels_booking.cancel_booking(service, username, email, "y0hI@mFak3eee33")
        test_result = "Unfortunately that is an invalid event ID.."
        self.assertFalse(cancel, test_result)
        sys.stdout = the_stdout

    def test_patient_cancels_booking_invalid_empty(self):
        the_stdout = sys.stdout
        new_string = StringIO()
        sys.stdout = new_string
        username, email = "Booker", "fake.booking@gmail.com"
        cancel = patient_cancels_booking.cancel_booking(service, username, email, 'None')
        test_result = "Unfortunately that is an invalid event ID.."
        self.assertFalse(cancel, test_result)
        sys.stdout = the_stdout


if __name__ == '__main__':
    unittest.main()
