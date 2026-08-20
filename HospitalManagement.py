class HospitalManagement:

    def __init__(self, patient_name, age, appointment_type,
                 lab_tests, medicines, insurance):

        self.patient_name = patient_name
        self.age = age
        self.appointment_type = appointment_type
        self.lab_tests = lab_tests
        self.medicines = medicines
        self.insurance = insurance

    def consultation_fee(self):

        if self.appointment_type == "Emergency":
            fee = 1500

        elif self.appointment_type == "Follow-up":
            fee = 500

        else:
            fee = 1000

        # Senior citizen discount
        if self.age >= 60 and self.appointment_type != "Emergency":
            fee = fee * 0.80

        return fee

    def lab_charges(self):

        prices = {
            "Blood": 300,
            "Urine": 200,
            "Xray": 500,
            "MRI": 3000,
            "CT Scan": 2500
        }

        total = 0

        for test in self.lab_tests:
            total += prices.get(test, 0)

        return total

    def medicine_charges(self):

        total = 0

        for medicine in self.medicines:
            total += medicine["price"] * medicine["quantity"]

        return total

    def insurance_coverage(self, total):

        if self.insurance is None:
            return 0

        percentage = self.insurance["coverage"]
        maximum = self.insurance["max_amount"]

        coverage = total * percentage / 100

        return min(coverage, maximum)

    def generate_bill(self):

        consultation = self.consultation_fee()

        lab = self.lab_charges()

        medicine = self.medicine_charges()

        total = consultation + lab + medicine

        insurance = self.insurance_coverage(total)

        payable = total - insurance

        return {
            "Patient": self.patient_name,
            "Consultation Fee": consultation,
            "Lab Charges": lab,
            "Medicine Charges": medicine,
            "Total Bill": total,
            "Insurance Coverage": insurance,
            "Patient Payable": payable
        }


# ==========================================
# MAIN PROGRAM
# ==========================================

print("==========================================")
print("     HOSPITAL APPOINTMENT & BILLING")
print("==========================================")

patient = HospitalManagement(
    patient_name="Rahul",
    age=35,
    appointment_type="Regular",

    lab_tests=[
        "Blood",
        "Xray"
    ],

    medicines=[
        {
            "name": "Paracetamol",
            "price": 100,
            "quantity": 2
        },
        {
            "name": "Antibiotic",
            "price": 200,
            "quantity": 1
        }
    ],

    insurance={
        "coverage": 50,
        "max_amount": 5000
    }
)

bill = patient.generate_bill()

print("\n----- BILL DETAILS -----")

for key, value in bill.items():
    print(key, ":", value)

print("\n==========================================")
print("        BILL GENERATED SUCCESSFULLY")
print("==========================================")
