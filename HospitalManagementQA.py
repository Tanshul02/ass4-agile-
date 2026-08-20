import unittest

from HospitalManagement import HospitalManagement


class TestHospitalManagement(unittest.TestCase):

    # -----------------------------------------
    # 1. Regular patient
    # -----------------------------------------
    def test_regular_patient(self):

        patient = HospitalManagement(
            "P001",
            35,
            "Dr. Sharma",
            "Cardiology",
            "Regular",
            30,
            [],
            [],
            None
        )

        bill = patient.calculate_bill()

        self.assertEqual(
            bill["consultation_fee"],
            1000
        )


    # -----------------------------------------
    # 2. Emergency patient
    # -----------------------------------------
    def test_emergency_patient(self):

        patient = HospitalManagement(
            "P002",
            35,
            "Dr. Kumar",
            "Emergency",
            "Emergency",
            30,
            [],
            [],
            None
        )

        bill = patient.calculate_bill()

        self.assertEqual(
            bill["consultation_fee"],
            1500
        )


    # -----------------------------------------
    # 3. Senior citizen
    # -----------------------------------------
    def test_senior_citizen(self):

        patient = HospitalManagement(
            "P003",
            65,
            "Dr. Sharma",
            "General",
            "Regular",
            30,
            [],
            [],
            None
        )

        bill = patient.calculate_bill()

        self.assertEqual(
            bill["consultation_fee"],
            800
        )


    # -----------------------------------------
    # 4. Senior citizen emergency
    # -----------------------------------------
    def test_senior_emergency(self):

        patient = HospitalManagement(
            "P004",
            70,
            "Dr. Kumar",
            "Emergency",
            "Emergency",
            30,
            [],
            [],
            None
        )

        bill = patient.calculate_bill()

        self.assertEqual(
            bill["consultation_fee"],
            1500
        )


    # -----------------------------------------
    # 5. Follow-up consultation
    # -----------------------------------------
    def test_follow_up(self):

        patient = HospitalManagement(
            "P005",
            40,
            "Dr. Sharma",
            "General",
            "Follow-up",
            20,
            [],
            [],
            None
        )

        bill = patient.calculate_bill()

        self.assertEqual(
            bill["consultation_fee"],
            500
        )


    # -----------------------------------------
    # 6. Senior citizen follow-up
    # -----------------------------------------
    def test_senior_follow_up(self):

        patient = HospitalManagement(
            "P006",
            65,
            "Dr. Sharma",
            "General",
            "Follow-up",
            20,
            [],
            [],
            None
        )

        bill = patient.calculate_bill()

        self.assertEqual(
            bill["consultation_fee"],
            400
        )


    # -----------------------------------------
    # 7. Blood test
    # -----------------------------------------
    def test_blood_test(self):

        patient = HospitalManagement(
            "P007",
            30,
            "Dr. Sharma",
            "General",
            "Regular",
            30,
            ["Blood"],
            [],
            None
        )

        bill = patient.calculate_bill()

        self.assertEqual(
            bill["lab_charges"],
            300
        )


    # -----------------------------------------
    # 8. Multiple lab tests
    # -----------------------------------------
    def test_multiple_lab_tests(self):

        patient = HospitalManagement(
            "P008",
            30,
            "Dr. Sharma",
            "General",
            "Regular",
            30,
            ["Blood", "Urine", "Xray"],
            [],
            None
        )

        bill = patient.calculate_bill()

        self.assertEqual(
            bill["lab_charges"],
            1000
        )


    # -----------------------------------------
    # 9. MRI test
    # -----------------------------------------
    def test_mri(self):

        patient = HospitalManagement(
            "P009",
            40,
            "Dr. Sharma",
            "Neurology",
            "Regular",
            30,
            ["MRI"],
            [],
            None
        )

        bill = patient.calculate_bill()

        self.assertEqual(
            bill["lab_charges"],
            3000
        )


    # -----------------------------------------
    # 10. Medicine charges
    # -----------------------------------------
    def test_medicine_charges(self):

        medicines = [
            {
                "name": "Medicine A",
                "price": 200,
                "quantity": 2
            }
        ]

        patient = HospitalManagement(
            "P010",
            30,
            "Dr. Sharma",
            "General",
            "Regular",
            30,
            [],
            medicines,
            None
        )

        bill = patient.calculate_bill()

        self.assertEqual(
            bill["medicine_charges"],
            400
        )


    # -----------------------------------------
    # 11. Multiple medicines
    # -----------------------------------------
    def test_multiple_medicines(self):

        medicines = [
            {
                "name": "Medicine A",
                "price": 200,
                "quantity": 2
            },
            {
                "name": "Medicine B",
                "price": 100,
                "quantity": 3
            }
        ]

        patient = HospitalManagement(
            "P011",
            30,
            "Dr. Sharma",
            "General",
            "Regular",
            30,
            [],
            medicines,
            None
        )

        bill = patient.calculate_bill()

        self.assertEqual(
            bill["medicine_charges"],
            700
        )


    # -----------------------------------------
    # 12. No insurance
    # -----------------------------------------
    def test_no_insurance(self):

        patient = HospitalManagement(
            "P012",
            30,
            "Dr. Sharma",
            "General",
            "Regular",
            30,
            ["Blood"],
            [],
            None
        )

        bill = patient.calculate_bill()

        self.assertEqual(
            bill["insurance_coverage"],
            0
        )


    # -----------------------------------------
    # 13. 50% insurance
    # -----------------------------------------
    def test_insurance_50_percent(self):

        patient = HospitalManagement(
            "P013",
            30,
            "Dr. Sharma",
            "General",
            "Regular",
            30,
            ["Blood"],
            [],
            {
                "coverage": 50,
                "max_amount": 5000
            }
        )

        bill = patient.calculate_bill()

        # Total = 1000 + 300 = 1300
        # 50% = 650
        self.assertEqual(
            bill["insurance_coverage"],
            650
        )


    # -----------------------------------------
    # 14. Insurance maximum limit
    # -----------------------------------------
    def test_insurance_maximum_limit(self):

        patient = HospitalManagement(
            "P014",
            30,
            "Dr. Sharma",
            "General",
            "Regular",
            30,
            ["MRI"],
            [],
            {
                "coverage": 90,
                "max_amount": 1000
            }
        )

        bill = patient.calculate_bill()

        self.assertEqual(
            bill["insurance_coverage"],
            1000
        )


    # -----------------------------------------
    # 15. Complete bill
    # -----------------------------------------
    def test_complete_bill(self):

        medicines = [
            {
                "name": "Medicine A",
                "price": 200,
                "quantity": 2
            }
        ]

        patient = HospitalManagement(
            "P015",
            35,
            "Dr. Sharma",
            "Cardiology",
            "Regular",
            30,
            ["Blood"],
            medicines,
            None
        )

        bill = patient.calculate_bill()

        # Consultation = 1000
        # Lab = 300
        # Medicine = 400
        # Total = 1700

        self.assertEqual(
            bill["total_bill"],
            1700
        )


    # -----------------------------------------
    # 16. Patient payable amount
    # -----------------------------------------
    def test_patient_payable(self):

        patient = HospitalManagement(
            "P016",
            35,
            "Dr. Sharma",
            "General",
            "Regular",
            30,
            ["Blood"],
            [],
            {
                "coverage": 50,
                "max_amount": 5000
            }
        )

        bill = patient.calculate_bill()

        # Total = 1300
        # Insurance = 650
        # Payable = 650

        self.assertEqual(
            bill["patient_payable"],
            650
        )


    # -----------------------------------------
    # 17. Emergency with lab
    # -----------------------------------------
    def test_emergency_with_lab(self):

        patient = HospitalManagement(
            "P017",
            45,
            "Dr. Kumar",
            "Emergency",
            "Emergency",
            45,
            ["Blood", "Xray"],
            [],
            None
        )

        bill = patient.calculate_bill()

        # Emergency = 1500
        # Lab = 800

        self.assertEqual(
            bill["total_bill"],
            2300
        )


    # -----------------------------------------
    # 18. Emergency with insurance
    # -----------------------------------------
    def test_emergency_with_insurance(self):

        patient = HospitalManagement(
            "P018",
            45,
            "Dr. Kumar",
            "Emergency",
            "Emergency",
            45,
            [],
            [],
            {
                "coverage": 50,
                "max_amount": 1000
            }
        )

        bill = patient.calculate_bill()

        self.assertEqual(
            bill["insurance_coverage"],
            750
        )


    # -----------------------------------------
    # 19. Unknown lab test
    # -----------------------------------------
    def test_unknown_lab_test(self):

        patient = HospitalManagement(
            "P019",
            30,
            "Dr. Sharma",
            "General",
            "Regular",
            30,
            ["Unknown Test"],
            [],
            None
        )

        bill = patient.calculate_bill()

        self.assertEqual(
            bill["lab_charges"],
            0
        )


    # -----------------------------------------
    # 20. Zero medicines
    # -----------------------------------------
    def test_zero_medicines(self):

        patient = HospitalManagement(
            "P020",
            30,
            "Dr. Sharma",
            "General",
            "Regular",
            30,
            [],
            [],
            None
        )

        bill = patient.calculate_bill()

        self.assertEqual(
            bill["medicine_charges"],
            0
        )


if __name__ == "__main__":

    print("\n======================================")
    print(" HOSPITAL MANAGEMENT - QA TESTING")
    print("======================================\n")

    unittest.main(verbosity=2)
