import unittest
from datetime import datetime

from ParkingManagement import ParkingManagement


class TestParkingManagement(unittest.TestCase):

    def system(self):
        return ParkingManagement()

    # 1
    def test_vehicle_entry(self):

        p = self.system()

        result = p.vehicle_entry(
            "CAR001",
            "Car",
            datetime(2026, 8, 20, 12, 0)
        )

        self.assertEqual(result["status"], "SUCCESS")

    # 2
    def test_car_slot(self):

        p = self.system()

        result = p.vehicle_entry(
            "CAR002",
            "Car",
            datetime(2026, 8, 20, 12, 0)
        )

        self.assertEqual(result["slot"], "C1")

    # 3
    def test_bike_slot(self):

        p = self.system()

        result = p.vehicle_entry(
            "BIKE001",
            "Bike",
            datetime(2026, 8, 20, 12, 0)
        )

        self.assertEqual(result["slot"], "B1")

    # 4
    def test_suv_slot(self):

        p = self.system()

        result = p.vehicle_entry(
            "SUV001",
            "SUV",
            datetime(2026, 8, 20, 12, 0)
        )

        self.assertEqual(result["slot"], "S1")

    # 5
    def test_truck_slot(self):

        p = self.system()

        result = p.vehicle_entry(
            "TRUCK001",
            "Truck",
            datetime(2026, 8, 20, 12, 0)
        )

        self.assertEqual(result["slot"], "T1")

    # 6
    def test_ev_slot(self):

        p = self.system()

        result = p.vehicle_entry(
            "EV001",
            "Electric Vehicle",
            datetime(2026, 8, 20, 12, 0)
        )

        self.assertEqual(result["slot"], "E1")

    # 7
    def test_full_parking(self):

        p = self.system()

        p.vehicle_entry("C1", "Car",
                        datetime(2026, 8, 20, 12, 0))

        p.vehicle_entry("C2", "Car",
                        datetime(2026, 8, 20, 12, 0))

        p.vehicle_entry("C3", "Car",
                        datetime(2026, 8, 20, 12, 0))

        result = p.vehicle_entry(
            "C4",
            "Car",
            datetime(2026, 8, 20, 12, 0)
        )

        self.assertEqual(result["status"], "FAILED")

    # 8
    def test_wrong_vehicle_type(self):

        p = self.system()

        result = p.vehicle_entry(
            "BUS001",
            "Bus",
            datetime(2026, 8, 20, 12, 0)
        )

        self.assertEqual(result["status"], "FAILED")

    # 9
    def test_duplicate_vehicle(self):

        p = self.system()

        p.vehicle_entry(
            "CAR004",
            "Car",
            datetime(2026, 8, 20, 12, 0)
        )

        result = p.vehicle_entry(
            "CAR004",
            "Car",
            datetime(2026, 8, 20, 13, 0)
        )

        self.assertEqual(result["status"], "FAILED")

    # 10
    def test_vehicle_exit(self):

        p = self.system()

        p.vehicle_entry(
            "CAR005",
            "Car",
            datetime(2026, 8, 20, 12, 0)
        )

        result = p.vehicle_exit(
            "CAR005",
            datetime(2026, 8, 20, 14, 0)
        )

        self.assertEqual(result["status"], "SUCCESS")

    # 11
    def test_early_exit(self):

        p = self.system()

        p.vehicle_entry(
            "CAR006",
            "Car",
            datetime(2026, 8, 20, 12, 0)
        )

        result = p.vehicle_exit(
            "CAR006",
            datetime(2026, 8, 20, 12, 30)
        )

        self.assertEqual(result["fee"], 50)

    # 12
    def test_two_hours(self):

        p = self.system()

        p.vehicle_entry(
            "CAR007",
            "Car",
            datetime(2026, 8, 20, 12, 0)
        )

        result = p.vehicle_exit(
            "CAR007",
            datetime(2026, 8, 20, 14, 0)
        )

        self.assertEqual(result["fee"], 100)

    # 13
    def test_overnight(self):

        p = self.system()

        p.vehicle_entry(
            "CAR008",
            "Car",
            datetime(2026, 8, 20, 22, 0)
        )

        result = p.vehicle_exit(
            "CAR008",
            datetime(2026, 8, 21, 6, 0)
        )

        self.assertEqual(result["fee"], 400)

    # 14
    def test_peak_pricing(self):

        p = self.system()

        fee = p.calculate_fee(
            "Car",
            datetime(2026, 8, 20, 18, 0),
            datetime(2026, 8, 20, 19, 0)
        )

        self.assertEqual(fee, 75)

    # 15
    def test_normal_pricing(self):

        p = self.system()

        fee = p.calculate_fee(
            "Car",
            datetime(2026, 8, 20, 12, 0),
            datetime(2026, 8, 20, 13, 0)
        )

        self.assertEqual(fee, 50)

    # 16
    def test_ev_charging(self):

        p = self.system()

        fee = p.calculate_fee(
            "Electric Vehicle",
            datetime(2026, 8, 20, 12, 0),
            datetime(2026, 8, 20, 13, 0)
        )

        self.assertEqual(fee, 90)

    # 17
    def test_lost_ticket(self):

        p = self.system()

        p.vehicle_entry(
            "CAR009",
            "Car",
            datetime(2026, 8, 20, 12, 0)
        )

        result = p.vehicle_exit(
            "CAR009",
            datetime(2026, 8, 20, 14, 0),
            lost_ticket=True
        )

        self.assertEqual(result["fee"], 1000)

    # 18
    def test_vip(self):

        p = self.system()

        p.vehicle_entry(
            "CAR010",
            "Car",
            datetime(2026, 8, 20, 12, 0),
            vip=True
        )

        result = p.vehicle_exit(
            "CAR010",
            datetime(2026, 8, 20, 13, 0)
        )

        self.assertEqual(result["fee"], 40)

    # 19
    def test_bike_fee(self):

        p = self.system()

        fee = p.calculate_fee(
            "Bike",
            datetime(2026, 8, 20, 12, 0),
            datetime(2026, 8, 20, 14, 0)
        )

        self.assertEqual(fee, 40)

    # 20
    def test_slot_reused(self):

        p = self.system()

        first = p.vehicle_entry(
            "CAR011",
            "Car",
            datetime(2026, 8, 20, 12, 0)
        )

        first_slot = first["slot"]

        p.vehicle_exit(
            "CAR011",
            datetime(2026, 8, 20, 13, 0)
        )

        second = p.vehicle_entry(
            "CAR012",
            "Car",
            datetime(2026, 8, 20, 14, 0)
        )

        self.assertEqual(
            second["slot"],
            first_slot
        )


if __name__ == "__main__":

    print()
    print("======================================")
    print("   SMART PARKING MANAGEMENT - QA")
    print("======================================")
    print()

    unittest.main(verbosity=2)
