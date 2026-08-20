import unittest

from HospitalManagement import HospitalManagement


class TestHospitalManagement(unittest.TestCase):

    # 1. Regular patient
    def test_regular_patient(self):

        patient = HospitalManagement(
            "P001",
            35,
            "Regular",
            [],
            [],
            None
        )

        bill = patient.generate_bill()

        self.assertEqual(
            bill["Consultation Fee"],
            1000
        )


    # 2. Emergency patient
    def test_emergency_patient(self):

        patient = HospitalManagement(
            "P002",
            35,
            "Emergency",
            [],
            [],
            None
        )

        bill = patient.generate_bill()

        self.assertEqual(
            bill["Consultation Fee"],
            1500
        )


    # 3. Senior citizen
    def test_senior_citizen(self):

        patient = HospitalManagement(
            "P003",
            65,
            "Regular",
            [],
            [],
            None
        )

        bill = patient.generate_bill()

        self.assertEqual(
            bill["Consultation Fee"],
            800
        )


    # 4. Senior citizen emergency
    def test_senior_emergency(self):

        patient = HospitalManagement(
            "P004",
            65,
            "Emergency",
            [],
            [],
            None
        )

        bill = patient.generate_bill()

        self.assertEqual(
            bill["Consultation Fee"],
            1500
        )


    # 5. Follow-up consultation
    def test_follow_up(self):

        patient = HospitalManagement(
            "P005",
            40,
            "Follow-up",
            [],
            [],
            None
        )

        bill = patient.generate_bill()

        self.assertEqual(
            bill["Consultation Fee"],
            500
        )


    # 6. Senior citizen follow-up
    def test_senior_follow_up(self):

        patient = HospitalManagement(
            "P006",
            65,
            "Follow-up",
            [],
            [],
            None
        )

        bill = patient.generate_bill()

        self.assertEqual(
            bill["Consultation Fee"],
            400
        )


    # 7. Blood test
    def test_blood_test(self):

        patient = HospitalManagement(
            "P007",
            30,
            "Regular",
            ["Blood"],
            [],
            None
        )

        bill = patient.generate_bill()

        self.assertEqual(
            bill["Lab Charges"],
            300
        )


    # 8. Multiple lab tests
    def test_multiple_lab_tests(self):

        patient = HospitalManagement(
            "P008",
            30,
            "Regular",
            ["Blood", "Urine", "Xray"],
            [],
            None
        )

        bill = patient.generate_bill()

        self.assertEqual(
            bill["Lab Charges"],
            1000
        )


    # 9. MRI test
    def test_mri(self):

        patient = HospitalManagement(
            "P009",
            30,
            "Regular",
            ["MRI"],
            [],
            None
        )

        bill = patient.generate_bill()

        self.assertEqual(
            bill["Lab Charges"],
            3000
        )


    # 10. Medicine charges
    def test_medicine_charges(self):

        medicines = [
            {
                "name": "Paracetamol",
                "price": 100,
                "quantity": 2
            }
        ]

        patient = HospitalManagement(
            "P010",
            30,
            "Regular",
            [],
            medicines,
            None
        )

        bill = patient.generate_bill()

        self.assertEqual(
            bill["Medicine Charges"],
            200
        )


    # 11. Multiple medicines
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
            "Regular",
            [],
            medicines,
            None
        )

        bill = patient.generate_bill()

        self.assertEqual(
            bill["Medicine Charges"],
            700
        )


    # 12. No insurance
    def test_no_insurance(self):

        patient = HospitalManagement(
            "P012",
            30,
            "Regular",
            ["Blood"],
            [],
            None
        )

        bill = patient.generate_bill()

        self.assertEqual(
            bill["Insurance Coverage"],
            0
        )


    # 13. 50% insurance
    def test_insurance_50_percent(self):

        patient = HospitalManagement(
            "P013",
            30,
            "Regular",
            ["Blood"],
            [],
            {
                "coverage": 50,
                "max_amount": 5000
            }
        )

        bill = patient.generate_bill()

        # Consultation = 1000
        # Blood = 300
        # Total = 1300
        # Insurance = 650

        self.assertEqual(
            bill["Insurance Coverage"],
            650
        )


    # 14. Insurance maximum limit
    def test_insurance_maximum_limit(self):

        patient = HospitalManagement(
            "P014",
            30,
            "Regular",
            ["MRI"],
            [],
            {
                "coverage": 90,
                "max_amount": 1000
            }
        )

        bill = patient.generate_bill()

        self.assertEqual(
            bill["Insurance Coverage"],
            1000
        )


    # 15. Complete bill
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
            "Regular",
            ["Blood"],
            medicines,
            None
        )

        bill = patient.generate_bill()

        # Consultation = 1000
        # Blood = 300
        # Medicine = 400
        # Total = 1700

        self.assertEqual(
            bill["Total Bill"],
            1700
        )


    # 16. Patient payable amount
    def test_patient_payable(self):

        patient = HospitalManagement(
            "P016",
            35,
            "Regular",
            ["Blood"],
            [],
            {
                "coverage": 50,
                "max_amount": 5000
            }
        )

        bill = patient.generate_bill()

        # Total = 1300
        # Insurance = 650
        # Payable = 650

        self.assertEqual(
            bill["Patient Payable"],
            650
        )


    # 17. Emergency with lab
    def test_emergency_with_lab(self):

        patient = HospitalManagement(
            "P017",
            45,
            "Emergency",
            ["Blood", "Xray"],
            [],
            None
        )

        bill = patient.generate_bill()

        # Emergency = 1500
        # Blood = 300
        # Xray = 500
        # Total = 2300

        self.assertEqual(
            bill["Total Bill"],
            2300
        )


    # 18. Emergency with insurance
    def test_emergency_with_insurance(self):

        patient = HospitalManagement(
            "P018",
            45,
            "Emergency",
            [],
            [],
            {
                "coverage": 50,
                "max_amount": 1000
            }
        )

        bill = patient.generate_bill()

        # 50% of 1500 = 750

        self.assertEqual(
            bill["Insurance Coverage"],
            750
        )


    # 19. Unknown lab test
    def test_unknown_lab_test(self):

        patient = HospitalManagement(
            "P019",
            30,
            "Regular",
            ["Unknown"],
            [],
            None
        )

        bill = patient.generate_bill()

        self.assertEqual(
            bill["Lab Charges"],
            0
        )


    # 20. Zero medicines
    def test_zero_medicines(self):

        patient = HospitalManagement(
            "P020",
            30,
            "Regular",
            [],
            [],
            None
        )

        bill = patient.generate_bill()

        self.assertEqual(
            bill["Medicine Charges"],
            0
        )


if __name__ == "__main__":

    print("\n======================================")
    print(" HOSPITAL MANAGEMENT - QA TESTING")
    print("======================================\n")

    unittest.main(verbosity=2)
