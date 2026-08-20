class OrderManagement:

    def __init__(self, products, coupon=None):
        self.products = products
        self.coupon = coupon

    def calculate_subtotal(self):
        subtotal = 0

        for product in self.products:
            if product["quantity"] <= 0:
                continue

            subtotal += (
                product["quantity"] *
                product["unit_price"]
            )

        return subtotal

    def calculate_category_discount(self, subtotal):
        discount = 0

        for product in self.products:

            if product["quantity"] <= 0:
                continue

            value = (
                product["quantity"] *
                product["unit_price"]
            )

            category = product["category"].lower()

            if category == "electronics":
                discount += value * 0.10

            elif category == "clothing":
                discount += value * 0.15

            elif category == "grocery":
                discount += value * 0.05

        # Maximum discount limit = 20%
        maximum_discount = subtotal * 0.20

        return min(discount, maximum_discount)

    def calculate_coupon_discount(self, amount):

        coupons = {
            "SAVE10": 0.10,
            "SAVE20": 0.20,
            "WELCOME": 0.15
        }

        if self.coupon is None:
            return 0

        coupon = self.coupon.upper()

        if coupon not in coupons:
            return 0

        discount = amount * coupons[coupon]

        # Maximum coupon discount = ₹2000
        return min(discount, 2000)

    def calculate_gst(self, amount):
        return amount * 0.18

    def calculate_shipping(self, amount):

        # Free shipping above ₹5000
        if amount >= 5000:
            return 0

        return 100

    def calculate_bulk_discount(self, subtotal):

        total_quantity = 0

        for product in self.products:
            if product["quantity"] > 0:
                total_quantity += product["quantity"]

        # Bulk order discount
        if total_quantity >= 10:
            return subtotal * 0.05

        return 0

    def process_order(self):

        if not self.products:
            return {
                "status": "REJECTED",
                "message": "No products in order"
            }

        # Check products
        for product in self.products:

            if product["quantity"] < 0:
                return {
                    "status": "REJECTED",
                    "message": "Negative quantity"
                }

            if product["quantity"] == 0:
                return {
                    "status": "REJECTED",
                    "message": "Zero quantity"
                }

            if product["unit_price"] < 0:
                return {
                    "status": "REJECTED",
                    "message": "Invalid price"
                }

            if not product.get("valid", True):
                return {
                    "status": "REJECTED",
                    "message": "Invalid product"
                }

            if not product.get("in_stock", True):
                return {
                    "status": "REJECTED",
                    "message": "Product out of stock"
                }

        subtotal = self.calculate_subtotal()

        category_discount = self.calculate_category_discount(
            subtotal
        )

        amount_after_category = subtotal - category_discount

        coupon_discount = self.calculate_coupon_discount(
            amount_after_category
        )

        bulk_discount = self.calculate_bulk_discount(
            subtotal
        )

        # Maximum total discount = 30% of subtotal
        maximum_total_discount = subtotal * 0.30

        total_discount = min(
            category_discount +
            coupon_discount +
            bulk_discount,
            maximum_total_discount
        )

        taxable_amount = subtotal - total_discount

        gst = self.calculate_gst(taxable_amount)

        shipping = self.calculate_shipping(taxable_amount)

        final_amount = taxable_amount + gst + shipping

        return {
            "status": "APPROVED",
            "subtotal": round(subtotal, 2),
            "category_discount": round(category_discount, 2),
            "coupon_discount": round(coupon_discount, 2),
            "bulk_discount": round(bulk_discount, 2),
            "gst": round(gst, 2),
            "shipping": round(shipping, 2),
            "final_amount": round(final_amount, 2)
        }


# Automatic demonstration
if __name__ == "__main__":

    products = [
        {
            "product_id": "P001",
            "category": "Electronics",
            "quantity": 2,
            "unit_price": 2000,
            "in_stock": True,
            "valid": True
        },
        {
            "product_id": "P002",
            "category": "Clothing",
            "quantity": 1,
            "unit_price": 1000,
            "in_stock": True,
            "valid": True
        }
    ]

    order = OrderManagement(
        products,
        "SAVE10"
    )

    result = order.process_order()

    print("===== E-COMMERCE ORDER PROCESSING =====")

    for key, value in result.items():
        print(key, ":", value)
