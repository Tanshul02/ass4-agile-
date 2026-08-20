from datetime import datetime


class ParkingManagement:

    def __init__(self):

        self.slots = {
            "Bike": ["B1", "B2"],
            "Car": ["C1", "C2", "C3"],
            "SUV": ["S1", "S2"],
            "Truck": ["T1"],
            "Electric Vehicle": ["E1", "E2"]
        }

        self.parked_vehicles = {}
        self.tickets = {}
        self.ticket_counter = 1

    # Vehicle Entry
    def vehicle_entry(self, vehicle_number, vehicle_type,
                      entry_time, vip=False):

        if vehicle_number in self.parked_vehicles:
            return {
                "status": "FAILED",
                "message": "Vehicle already parked"
            }

        if vehicle_type not in self.slots:
            return {
                "status": "FAILED",
                "message": "Invalid vehicle type"
            }

        if len(self.slots[vehicle_type]) == 0:
            return {
                "status": "FAILED",
                "message": "Parking lot full"
            }

        # Automatically select first suitable slot
        slot = self.slots[vehicle_type].pop(0)

        ticket = "T" + str(self.ticket_counter)
        self.ticket_counter += 1

        self.parked_vehicles[vehicle_number] = {
            "vehicle_type": vehicle_type,
            "slot": slot,
            "entry_time": entry_time,
            "vip": vip,
            "ticket": ticket
        }

        self.tickets[ticket] = vehicle_number

        return {
            "status": "SUCCESS",
            "vehicle": vehicle_number,
            "slot": slot,
            "ticket": ticket
        }

    # Get allocated slot
    def get_slot(self, vehicle_number):

        if vehicle_number not in self.parked_vehicles:
            return None

        return self.parked_vehicles[vehicle_number]["slot"]

    # Calculate parking fee
    def calculate_fee(self, vehicle_type, entry_time,
                      exit_time, vip=False, lost_ticket=False):

        # Lost ticket
        if lost_ticket:
            return 1000

        duration = exit_time - entry_time

        hours = duration.total_seconds() / 3600

        # Minimum 1 hour
        if hours <= 0:
            hours = 1

        if hours.is_integer():
            hours = int(hours)
        else:
            hours = int(hours) + 1

        rates = {
            "Bike": 20,
            "Car": 50,
            "SUV": 70,
            "Truck": 100,
            "Electric Vehicle": 40
        }

        if vehicle_type not in rates:
            return -1

        fee = rates[vehicle_type] * hours

        # Peak hours: 8-11 AM and 5-8 PM
        if (8 <= entry_time.hour < 11 or
                17 <= entry_time.hour < 20):

            fee = fee * 1.50

        # VIP discount
        if vip:
            fee = fee * 0.80

        # EV charging
        if vehicle_type == "Electric Vehicle":
            fee += 50

        return round(fee, 2)

    # Vehicle Exit
    def vehicle_exit(self, vehicle_number, exit_time,
                     lost_ticket=False):

        if vehicle_number not in self.parked_vehicles:
            return {
                "status": "FAILED",
                "message": "Vehicle not found"
            }

        vehicle = self.parked_vehicles[vehicle_number]

        fee = self.calculate_fee(
            vehicle["vehicle_type"],
            vehicle["entry_time"],
            exit_time,
            vehicle["vip"],
            lost_ticket
        )

        vehicle_type = vehicle["vehicle_type"]
        slot = vehicle["slot"]
        ticket = vehicle["ticket"]

        # Return slot to the FRONT
        # so it can be reused immediately
        self.slots[vehicle_type].insert(0, slot)

        del self.parked_vehicles[vehicle_number]

        if ticket in self.tickets:
            del self.tickets[ticket]

        return {
            "status": "SUCCESS",
            "vehicle": vehicle_number,
            "slot": slot,
            "fee": fee
        }


# ==========================================
# MAIN PROGRAM
# ==========================================

if __name__ == "__main__":

    print("==========================================")
    print("     SMART PARKING MANAGEMENT SYSTEM")
    print("==========================================")

    parking = ParkingManagement()

    result = parking.vehicle_entry(
        "CAR001",
        "Car",
        datetime(2026, 8, 20, 10, 0)
    )

    print("\nVehicle Entry:")
    print(result)

    print("\nAllocated Slot:")
    print(
        parking.get_slot("CAR001")
    )

    exit_result = parking.vehicle_exit(
        "CAR001",
        datetime(2026, 8, 20, 12, 0)
    )

    print("\nVehicle Exit:")
    print(exit_result)

    print("\n==========================================")
    print("       PARKING TRANSACTION COMPLETE")
    print("==========================================")
