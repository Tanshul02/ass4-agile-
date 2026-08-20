import unittest
from datetime import date

from AirlineReservation import AirlineReservation


class TestAirlineReservation(unittest.TestCase):

    def create_system(self, seats=10):

        system = AirlineReservation()

        system.add_flight(
            "AI101",
            "Delhi",
            "Mumbai",
            seats,
            date(2026, 9, 10)
        )

        return system

    # 1. Successful booking
    def test_successful_booking(self):

        system = self.create_system()

        result = system.book_passenger(
            "AI101",
            "Rahul",
            "Adult",
            "Economy",
            date(2026, 8, 20),
            10
        )

        self.assertEqual(result["status"], "SUCCESS")


    # 2. Seat availability
    def test_seat_availability(self):

        system = self.create_system()

        self.assertEqual(
            system.seat_availability("AI101"),
            10
        )


    # 3. Seat decreases after booking
    def test_seat_decreases(self):

        system = self.create_system()

        system.book_passenger(
            "AI101",
            "Rahul",
            "Adult",
            "Economy",
            date(2026, 8, 20),
            10
        )

        self.assertEqual(
            system.seat_availability("AI101"),
            9
        )


    # 4. Flight search
    def test_flight_search(self):

        system = self.create_system()

        result = system.search_flight(
            "Delhi",
            "Mumbai"
        )

        self.assertIn("AI101", result)


    # 5. Invalid flight search
    def test_invalid_flight_search(self):

        system = self.create_system()

        result = system.search_flight(
            "Delhi",
            "Chennai"
        )

        self.assertEqual(result, [])


    # 6. Double booking
    def test_double_booking(self):

        system = self.create_system(seats=2)

        first = system.book_passenger(
            "AI101",
            "Rahul",
            "Adult",
            "Economy",
            date(2026, 8, 20),
            10
        )

        second = system.book_passenger(
            "AI101",
            "Rahul",
            "Adult",
            "Economy",
            date(2026, 8, 20),
            10
        )

        self.assertEqual(first["status"], "SUCCESS")
        self.assertEqual(second["status"], "SUCCESS")


    # 7. Cancellation
    def test_cancellation(self):

        system = self.create_system()

        booking = system.book_passenger(
            "AI101",
            "Rahul",
            "Adult",
            "Economy",
            date(2026, 8, 20),
            10
        )

        result = system.cancel_booking(
            booking["booking_id"]
        )

        self.assertEqual(
            result["status"],
            "CANCELLED"
        )


    # 8. Refund calculation
    def test_refund(self):

        system = self.create_system()

        booking = system.book_passenger(
            "AI101",
            "Rahul",
            "Adult",
            "Economy",
            date(2026, 8, 20),
            10
        )

        cancellation = system.cancel_booking(
            booking["booking_id"]
        )

        expected_refund = booking["total"] * 0.80

        self.assertEqual(
            cancellation["refund"],
            round(expected_refund, 2)
        )


    # 9. Seat restored after cancellation
    def test_seat_restored(self):

        system = self.create_system()

        booking = system.book_passenger(
            "AI101",
            "Rahul",
            "Adult",
            "Economy",
            date(2026, 8, 20),
            10
        )

        system.cancel_booking(
            booking["booking_id"]
        )

        self.assertEqual(
            system.seat_availability("AI101"),
            10
        )


    # 10. Fully booked flight
    def test_fully_booked_flight(self):

        system = self.create_system(seats=1)

        system.book_passenger(
            "AI101",
            "Rahul",
            "Adult",
            "Economy",
            date(2026, 8, 20),
            10
        )

        result = system.book_passenger(
            "AI101",
            "Amit",
            "Adult",
            "Economy",
            date(2026, 8, 20),
            10
        )

        self.assertEqual(
            result["message"],
            "Flight fully booked"
        )


    # 11. Invalid passenger
    def test_invalid_passenger(self):

        system = self.create_system()

        result = system.book_passenger(
            "AI101",
            "",
            "Adult",
            "Economy",
            date(2026, 8, 20),
            10
        )

        self.assertEqual(
            result["message"],
            "Invalid passenger"
        )


    # 12. Invalid passenger type
    def test_invalid_passenger_type(self):

        system = self.create_system()

        result = system.book_passenger(
            "AI101",
            "Rahul",
            "Unknown",
            "Economy",
            date(2026, 8, 20),
            10
        )

        self.assertEqual(
            result["status"],
            "FAILED"
        )


    # 13. Excess baggage
    def test_excess_baggage(self):

        system = self.create_system()

        result = system.book_passenger(
            "AI101",
            "Rahul",
            "Adult",
            "Economy",
            date(2026, 8, 20),
            20
        )

        # Economy free limit = 15 kg
        # Excess = 5 kg
        # Charge = 5 x 500 = 2500

        self.assertEqual(
            result["baggage_charge"],
            2500
        )


    # 14. Free baggage
    def test_free_baggage(self):

        system = self.create_system()

        result = system.book_passenger(
            "AI101",
            "Rahul",
            "Adult",
            "Economy",
            date(2026, 8, 20),
            15
        )

        self.assertEqual(
            result["baggage_charge"],
            0
        )


    # 15. Economy fare
    def test_economy_fare(self):

        system = self.create_system()

        fare = system.calculate_fare(
            "AI101",
            "Adult",
            "Economy",
            date(2026, 8, 20)
        )

        self.assertEqual(
            fare,
            5000
        )


    # 16. Business fare
    def test_business_fare(self):

        system = self.create_system()

        fare = system.calculate_fare(
            "AI101",
            "Adult",
            "Business",
            date(2026, 8, 20)
        )

        # Base Business fare = 10000
        self.assertEqual(
            fare,
            10000
        )


    # 17. First Class fare
    def test_first_class_fare(self):

        system = self.create_system()

        fare = system.calculate_fare(
            "AI101",
            "Adult",
            "First Class",
            date(2026, 8, 20)
        )

        # Base First Class fare = 20000
        self.assertEqual(
            fare,
            20000
        )


    # 18. Child passenger discount
    def test_child_discount(self):

        system = self.create_system()

        adult_fare = system.calculate_fare(
            "AI101",
            "Adult",
            "Economy",
            date(2026, 8, 20)
        )

        child_fare = system.calculate_fare(
            "AI101",
            "Child",
            "Economy",
            date(2026, 8, 20)
        )

        self.assertEqual(
            child_fare,
            adult_fare * 0.70
        )


    # 19. Senior passenger discount
    def test_senior_discount(self):

        system = self.create_system()

        adult_fare = system.calculate_fare(
            "AI101",
            "Adult",
            "Economy",
            date(2026, 8, 20)
        )

        senior_fare = system.calculate_fare(
            "AI101",
            "Senior",
            "Economy",
            date(2026, 8, 20)
        )

        self.assertEqual(
            senior_fare,
            adult_fare * 0.80
        )


    # 20. Dynamic fare calculation
    def test_dynamic_fare(self):

        system = self.create_system(seats=10)

        normal_fare = system.calculate_fare(
            "AI101",
            "Adult",
            "Economy",
            date(2026, 8, 20)
        )

        # Book 8 of 10 seats
        for i in range(8):

            system.book_passenger(
                "AI101",
                "Passenger" + str(i),
                "Adult",
                "Economy",
                date(2026, 8, 20),
                10
            )

        high_demand_fare = system.calculate_fare(
            "AI101",
            "Adult",
            "Economy",
            date(2026, 8, 20)
        )

        self.assertGreater(
            high_demand_fare,
            normal_fare
        )


if __name__ == "__main__":

    print("\n======================================")
    print(" AIRLINE RESERVATION - QA TESTING")
    print("======================================\n")

    unittest.main(verbosity=2)
