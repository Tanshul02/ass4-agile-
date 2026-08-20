import unittest

from LoanProcessingSystem import LoanProcessingSystem


class LoanProcessingQA(unittest.TestCase):

    # 1. Minimum age
    def test_minimum_age(self):

        loan = LoanProcessingSystem(
            "T001", 18, 50000, 0,
            750, "Salaried", 500000, 5
        )

        result = loan.process_loan()

        self.assertNotIn("Invalid age", str(result))


    # 2. Maximum age
    def test_maximum_age(self):

        loan = LoanProcessingSystem(
            "T002", 60, 50000, 0,
            750, "Salaried", 500000, 5
        )

        result = loan.process_loan()

        self.assertNotIn("Invalid age", str(result))


    # 3. Invalid age
    def test_invalid_age(self):

        loan = LoanProcessingSystem(
            "T003", 17, 50000, 0,
            750, "Salaried", 500000, 5
        )

        result = loan.process_loan()

        self.assertIn("Invalid age", result)


    # 4. Invalid salary
    def test_invalid_salary(self):

        loan = LoanProcessingSystem(
            "T004", 30, 0, 0,
            750, "Salaried", 500000, 5
        )

        result = loan.process_loan()

        self.assertIn("Invalid salary", result)


    # 5. Poor credit score
    def test_poor_credit_score(self):

        loan = LoanProcessingSystem(
            "T005", 30, 50000, 0,
            500, "Salaried", 500000, 5
        )

        result = loan.process_loan()

        self.assertIn("Poor credit score", result)


    # 6. Existing loan threshold
    def test_existing_loan_threshold(self):

        loan = LoanProcessingSystem(
            "T006", 30, 50000, 3000000,
            750, "Salaried", 500000, 5
        )

        result = loan.process_loan()

        self.assertIn(
            "Existing loan exceeds threshold",
            result
        )


    # 7. High DTI
    def test_high_dti(self):

        loan = LoanProcessingSystem(
            "T007", 30, 20000, 1000000,
            750, "Salaried", 100000, 5
        )

        result = loan.process_loan()

        self.assertIn(
            "High debt-to-income ratio",
            result
        )


    # 8. Salaried employment
    def test_salaried_employment(self):

        loan = LoanProcessingSystem(
            "T008", 30, 50000, 0,
            750, "Salaried", 500000, 5
        )

        result = loan.process_loan()

        self.assertEqual(
            result["Eligible Loan Amount"],
            1000000
        )


    # 9. Self-employed employment
    def test_self_employed(self):

        loan = LoanProcessingSystem(
            "T009", 30, 50000, 0,
            750, "Self-Employed", 500000, 5
        )

        result = loan.process_loan()

        self.assertEqual(
            result["Eligible Loan Amount"],
            750000
        )


    # 10. Boundary loan amount
    def test_boundary_loan_amount(self):

        loan = LoanProcessingSystem(
            "T010", 30, 50000, 0,
            750, "Salaried", 1000000, 5
        )

        result = loan.process_loan()

        self.assertEqual(
            result["Status"],
            "APPROVED"
        )


    # 11. EMI accuracy
    def test_emi_accuracy(self):

        loan = LoanProcessingSystem(
            "T011", 30, 50000, 0,
            750, "Salaried", 500000, 5
        )

        emi = loan.calculate_emi(
            500000,
            8,
            5
        )

        self.assertAlmostEqual(
            emi,
            10138.20,
            places=1
        )


    # 12. Invalid loan amount
    def test_invalid_loan_amount(self):

        loan = LoanProcessingSystem(
            "T012", 30, 50000, 0,
            750, "Salaried", -5000, 5
        )

        result = loan.process_loan()

        self.assertIn(
            "Invalid loan amount",
            result
        )


    # 13. Exception handling
    def test_exception_handling(self):

        with self.assertRaises(ValueError):

            int("ABC")


if __name__ == "__main__":

    print("\n===== RUNNING QA TESTS =====\n")

    unittest.main(verbosity=2)
