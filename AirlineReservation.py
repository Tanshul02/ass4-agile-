from datetime import date


class AirlineReservation:

    def __init__(self):
        self.flights = {}
        self.bookings = {}
        self.booking_counter = 1

    # -----------------------------------------
    # Add Flight
    # -----------------------------------------
    def add_flight(
        self,
        flight_id,
        source,
        destination,
        total_seats,
        travel_date
    ):

        self.flights[flight_id] = {
            "source": source,
            "destination": destination,
            "total_seats": total_seats,
            "available_seats": total_seats,
            "travel_date": travel_date
        }

    # -----------------------------------------
    # Flight Search
    # -----------------------------------------
    def search_flight(
        self,
        source,
        destination
    ):

        results = []

        for flight_id, flight in self.flights.items():

            if (
                flight["source"] == source
                and
                flight["destination"] == destination
            ):
                results.append(flight_id)

        return results

    # -----------------------------------------
    # Seat Availability
    # -----------------------------------------
    def seat_availability(self, flight_id):

        if flight_id not in self.flights:
            return -1

        return self.flights[flight_id]["available_seats"]

    # -----------------------------------------
    # Dynamic Fare
    # -----------------------------------------
    def calculate_fare(
        self,
        flight_id,
        passenger_type,
        travel_class,
        booking_date
    ):

        if flight_id not in self.flights:
            return -1

        flight = self.flights[flight_id]

        # Base fare according to class
        if travel_class == "Economy":
            base_fare = 5000

        elif travel_class == "Business":
            base_fare = 10000

        elif travel_class == "First Class":
            base_fare = 20000

        else:
            return -1

        # -----------------------------------------
        # Seat availability pricing
        # -----------------------------------------
        available = flight["available_seats"]
        total = flight["total_seats"]

        occupancy = 1 - (available / total)

        if occupancy >= 0.80:
            base_fare *= 1.50

        elif occupancy >= 0.50:
            base_fare *= 1.25

        # -----------------------------------------
        # Booking date pricing
        # -----------------------------------------
        days_before_travel = (
            flight["travel_date"] - booking_date
        ).days

        if days_before_travel <= 3:
            base_fare *= 1.30

        elif days_before_travel <= 7:
            base_fare *= 1.15

        # -----------------------------------------
        # Passenger type
        # -----------------------------------------
        if passenger_type == "Child":
            base_fare *= 0.70

        elif passenger_type == "Senior":
            base_fare *= 0.80

        elif passenger_type == "Adult":
            base_fare *= 1.00

        else:
            return -1

        return round(base_fare, 2)

    # -----------------------------------------
    # Booking
    # -----------------------------------------
    def book_passenger(
        self,
        flight_id,
        passenger_name,
        passenger_type,
        travel_class,
        booking_date,
        baggage_kg
    ):

        # Invalid passenger
        if not passenger_name or passenger_name.strip() == "":
            return {
                "status": "FAILED",
                "message": "Invalid passenger"
            }

        # Flight doesn't exist
        if flight_id not in self.flights:
            return {
                "status": "FAILED",
                "message": "Flight not found"
            }

        flight = self.flights[flight_id]

        # Fully booked
        if flight["available_seats"] <= 0:
            return {
                "status": "FAILED",
                "message": "Flight fully booked"
            }

        # Calculate fare
        fare = self.calculate_fare(
            flight_id,
            passenger_type,
            travel_class,
            booking_date
        )

        if fare == -1:
            return {
                "status": "FAILED",
                "message": "Invalid passenger or class"
            }

        # Baggage charges
        baggage_charge = self.calculate_baggage_charge(
            baggage_kg,
            travel_class
        )

        total_fare = fare + baggage_charge

        booking_id = "B" + str(self.booking_counter)

        self.booking_counter += 1

        self.bookings[booking_id] = {
            "flight_id": flight_id,
            "passenger": passenger_name,
            "passenger_type": passenger_type,
            "class": travel_class,
            "fare": fare,
            "baggage": baggage_charge,
            "total": total_fare,
            "booking_date": booking_date
        }

        flight["available_seats"] -= 1

        return {
            "status": "SUCCESS",
            "booking_id": booking_id,
            "fare": fare,
            "baggage_charge": baggage_charge,
            "total": total_fare
        }

    # -----------------------------------------
    # Baggage Charges
    # -----------------------------------------
    def calculate_baggage_charge(
        self,
        baggage_kg,
        travel_class
    ):

        # Free baggage allowance
        if travel_class == "Economy":
            free_limit = 15

        elif travel_class == "Business":
            free_limit = 30

        elif travel_class == "First Class":
            free_limit = 40

        else:
            return -1

        if baggage_kg <= free_limit:
            return 0

        excess = baggage_kg - free_limit

        return excess * 500

    # -----------------------------------------
    # Cancellation
    # -----------------------------------------
    def cancel_booking(self, booking_id):

        if booking_id not in self.bookings:
            return {
                "status": "FAILED",
                "message": "Booking not found"
            }

        booking = self.bookings[booking_id]

        total = booking["total"]

        # Refund policy
        refund = total * 0.80

        flight_id = booking["flight_id"]

        self.flights[flight_id]["available_seats"] += 1

        del self.bookings[booking_id]

        return {
            "status": "CANCELLED",
            "refund": round(refund, 2)
        }


# =========================================
# AUTOMATIC DEMONSTRATION
# =========================================

if __name__ == "__main__":

    print("==========================================")
    print("       AIRLINE RESERVATION SYSTEM")
    print("==========================================")

    system = AirlineReservation()

    system.add_flight(
        "AI101",
        "Delhi",
        "Mumbai",
        10,
        date(2026, 9, 10)
    )

    print("\nAvailable Flights:")

    print(
        system.search_flight(
            "Delhi",
            "Mumbai"
        )
    )

    print("\nAvailable Seats:")

    print(
        system.seat_availability("AI101")
    )

    booking = system.book_passenger(
        "AI101",
        "Rahul",
        "Adult",
        "Economy",
        date(2026, 9, 1),
        20
    )

    print("\nBooking Result:")

    print(booking)

    print("\nRemaining Seats:")

    print(
        system.seat_availability("AI101")
    )

    print("\n==========================================")
