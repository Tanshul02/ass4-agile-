class LoanProcessingSystem:

    def __init__(self, customer_id, age, salary, existing_loan,
                 credit_score, employment_type, requested_loan, tenure):

        self.customer_id = customer_id
        self.age = age
        self.salary = salary
        self.existing_loan = existing_loan
        self.credit_score = credit_score
        self.employment_type = employment_type
        self.requested_loan = requested_loan
        self.tenure = tenure

    def calculate_dti(self):
        if self.salary <= 0:
            return float("inf")

        monthly_existing_payment = self.existing_loan / 60
        return (monthly_existing_payment / self.salary) * 100

    def calculate_eligible_amount(self):

        if self.employment_type.lower() == "salaried":
            multiplier = 20
        elif self.employment_type.lower() == "self-employed":
            multiplier = 15
        else:
            multiplier = 10

        return self.salary * multiplier

    def calculate_interest_rate(self):

        if self.credit_score >= 750:
            return 8.0
        elif self.credit_score >= 650:
            return 10.0
        else:
            return 12.0

    def calculate_emi(self, principal, annual_rate, tenure):

        monthly_rate = annual_rate / (12 * 100)
        months = tenure * 12

        if monthly_rate == 0:
            return principal / months

        emi = (
            principal * monthly_rate *
            (1 + monthly_rate) ** months
        ) / (
            (1 + monthly_rate) ** months - 1
        )

        return emi

    def process_loan(self):

        # Age validation
        if self.age < 18 or self.age > 60:
            return "REJECTED: Invalid age"

        # Salary validation
        if self.salary <= 0:
            return "REJECTED: Invalid salary"

        # Credit score validation
        if self.credit_score < 600:
            return "REJECTED: Poor credit score"

        # Existing loan validation
        if self.existing_loan > self.salary * 50:
            return "REJECTED: Existing loan exceeds threshold"

        # DTI validation
        dti = self.calculate_dti()

        if dti > 50:
            return "REJECTED: High debt-to-income ratio"

        # Eligible amount
        eligible_amount = self.calculate_eligible_amount()

        # Requested loan validation
        if self.requested_loan <= 0:
            return "REJECTED: Invalid loan amount"

        if self.requested_loan > eligible_amount:
            return "REJECTED: Requested amount exceeds eligibility"

        # Interest rate
        interest_rate = self.calculate_interest_rate()

        # EMI
        emi = self.calculate_emi(
            self.requested_loan,
            interest_rate,
            self.tenure
        )

        return {
            "Customer ID": self.customer_id,
            "DTI": round(dti, 2),
            "Eligible Loan Amount": round(eligible_amount, 2),
            "Interest Rate": interest_rate,
            "EMI": round(emi, 2),
            "Status": "APPROVED"
        }


# Automatic execution - NO USER INPUT
if __name__ == "__main__":

    loan = LoanProcessingSystem(
        "C001",
        30,
        50000,
        100000,
        780,
        "Salaried",
        500000,
        5
    )

    result = loan.process_loan()

    print("===== BANKING LOAN APPROVAL SYSTEM =====")

    if isinstance(result, dict):

        for key, value in result.items():
            print(f"{key}: {value}")

    else:
        print(result)
