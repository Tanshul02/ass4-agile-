import unittest

from OrderManagement import OrderManagement


class TestOrderManagement(unittest.TestCase):

    # ------------------------------------------------
    # 1. Single product
    # ------------------------------------------------
    def test_single_product(self):

        products = [
            {
                "product_id": "P001",
                "category": "Electronics",
                "quantity": 1,
                "unit_price": 1000,
                "in_stock": True,
                "valid": True
            }
        ]

        result = OrderManagement(products).process_order()

        self.assertEqual(result["status"], "APPROVED")
        self.assertEqual(result["subtotal"], 1000)


    # ------------------------------------------------
    # 2. Multiple products
    # ------------------------------------------------
    def test_multiple_products(self):

        products = [
            {
                "product_id": "P001",
                "category": "Electronics",
                "quantity": 2,
                "unit_price": 1000,
                "in_stock": True,
                "valid": True
            },
            {
                "product_id": "P002",
                "category": "Clothing",
                "quantity": 2,
                "unit_price": 500,
                "in_stock": True,
                "valid": True
            }
        ]

        result = OrderManagement(products).process_order()

        self.assertEqual(result["status"], "APPROVED")
        self.assertEqual(result["subtotal"], 3000)


    # ------------------------------------------------
    # 3. Zero quantity
    # ------------------------------------------------
    def test_zero_quantity(self):

        products = [
            {
                "product_id": "P003",
                "category": "Grocery",
                "quantity": 0,
                "unit_price": 500,
                "in_stock": True,
                "valid": True
            }
        ]

        result = OrderManagement(products).process_order()

        self.assertEqual(result["status"], "REJECTED")


    # ------------------------------------------------
    # 4. Negative quantity
    # ------------------------------------------------
    def test_negative_quantity(self):

        products = [
            {
                "product_id": "P004",
                "category": "Grocery",
                "quantity": -2,
                "unit_price": 500,
                "in_stock": True,
                "valid": True
            }
        ]

        result = OrderManagement(products).process_order()

        self.assertEqual(result["message"], "Negative quantity")


    # ------------------------------------------------
    # 5. Invalid product
    # ------------------------------------------------
    def test_invalid_product(self):

        products = [
            {
                "product_id": "INVALID",
                "category": "Electronics",
                "quantity": 1,
                "unit_price": 1000,
                "in_stock": True,
                "valid": False
            }
        ]

        result = OrderManagement(products).process_order()

        self.assertEqual(result["message"], "Invalid product")


    # ------------------------------------------------
    # 6. Out of stock
    # ------------------------------------------------
    def test_out_of_stock(self):

        products = [
            {
                "product_id": "P005",
                "category": "Electronics",
                "quantity": 1,
                "unit_price": 1000,
                "in_stock": False,
                "valid": True
            }
        ]

        result = OrderManagement(products).process_order()

        self.assertEqual(result["message"], "Product out of stock")


    # ------------------------------------------------
    # 7. Invalid coupon
    # ------------------------------------------------
    def test_invalid_coupon(self):

        products = [
            {
                "product_id": "P006",
                "category": "Electronics",
                "quantity": 1,
                "unit_price": 1000,
                "in_stock": True,
                "valid": True
            }
        ]

        result = OrderManagement(
            products,
            "INVALID"
        ).process_order()

        self.assertEqual(result["coupon_discount"], 0)


    # ------------------------------------------------
    # 8. SAVE10 coupon
    # ------------------------------------------------
    def test_save10_coupon(self):

        products = [
            {
                "product_id": "P007",
                "category": "Electronics",
                "quantity": 1,
                "unit_price": 2000,
                "in_stock": True,
                "valid": True
            }
        ]

        result = OrderManagement(
            products,
            "SAVE10"
        ).process_order()

        self.assertGreater(
            result["coupon_discount"],
            0
        )


    # ------------------------------------------------
    # 9. SAVE20 coupon
    # ------------------------------------------------
    def test_save20_coupon(self):

        products = [
            {
                "product_id": "P008",
                "category": "Electronics",
                "quantity": 1,
                "unit_price": 2000,
                "in_stock": True,
                "valid": True
            }
        ]

        result = OrderManagement(
            products,
            "SAVE20"
        ).process_order()

        self.assertGreater(
            result["coupon_discount"],
            0
        )


    # ------------------------------------------------
    # 10. Maximum discount limit
    # ------------------------------------------------
    def test_maximum_discount(self):

        products = [
            {
                "product_id": "P009",
                "category": "Electronics",
                "quantity": 5,
                "unit_price": 10000,
                "in_stock": True,
                "valid": True
            }
        ]

        result = OrderManagement(
            products,
            "SAVE20"
        ).process_order()

        # Total discount cannot exceed 30%
        max_discount = result["subtotal"] * 0.30

        total_discount = (
            result["category_discount"] +
            result["coupon_discount"] +
            result["bulk_discount"]
        )

        self.assertLessEqual(
            total_discount,
            max_discount
        )


    # ------------------------------------------------
    # 11. GST calculation
    # ------------------------------------------------
    def test_gst_calculation(self):

        products = [
            {
                "product_id": "P010",
                "category": "Grocery",
                "quantity": 1,
                "unit_price": 1000,
                "in_stock": True,
                "valid": True
            }
        ]

        result = OrderManagement(products).process_order()

        expected_gst = (
            result["subtotal"]
            - result["category_discount"]
        ) * 0.18

        self.assertAlmostEqual(
            result["gst"],
            expected_gst,
            places=2
        )


    # ------------------------------------------------
    # 12. Free shipping
    # ------------------------------------------------
    def test_free_shipping(self):

        products = [
            {
                "product_id": "P011",
                "category": "Electronics",
                "quantity": 1,
                "unit_price": 6000,
                "in_stock": True,
                "valid": True
            }
        ]

        result = OrderManagement(products).process_order()

        self.assertEqual(
            result["shipping"],
            0
        )


    # ------------------------------------------------
    # 13. Shipping below threshold
    # ------------------------------------------------
    def test_shipping_charge(self):

        products = [
            {
                "product_id": "P012",
                "category": "Grocery",
                "quantity": 1,
                "unit_price": 500,
                "in_stock": True,
                "valid": True
            }
        ]

        result = OrderManagement(products).process_order()

        self.assertEqual(
            result["shipping"],
            100
        )


    # ------------------------------------------------
    # 14. Bulk order
    # ------------------------------------------------
    def test_bulk_order(self):

        products = [
            {
                "product_id": "P013",
                "category": "Grocery",
                "quantity": 10,
                "unit_price": 100,
                "in_stock": True,
                "valid": True
            }
        ]

        result = OrderManagement(products).process_order()

        self.assertGreater(
            result["bulk_discount"],
            0
        )


    # ------------------------------------------------
    # 15. Clothing discount
    # ------------------------------------------------
    def test_clothing_discount(self):

        products = [
            {
                "product_id": "P014",
                "category": "Clothing",
                "quantity": 2,
                "unit_price": 1000,
                "in_stock": True,
                "valid": True
            }
        ]

        result = OrderManagement(products).process_order()

        self.assertEqual(
            result["category_discount"],
            300
        )


    # ------------------------------------------------
    # 16. Electronics discount
    # ------------------------------------------------
    def test_electronics_discount(self):

        products = [
            {
                "product_id": "P015",
                "category": "Electronics",
                "quantity": 2,
                "unit_price": 1000,
                "in_stock": True,
                "valid": True
            }
        ]

        result = OrderManagement(products).process_order()

        self.assertEqual(
            result["category_discount"],
            200
        )


    # ------------------------------------------------
    # 17. Grocery discount
    # ------------------------------------------------
    def test_grocery_discount(self):

        products = [
            {
                "product_id": "P016",
                "category": "Grocery",
                "quantity": 2,
                "unit_price": 1000,
                "in_stock": True,
                "valid": True
            }
        ]

        result = OrderManagement(products).process_order()

        self.assertEqual(
            result["category_discount"],
            100
        )


    # ------------------------------------------------
    # 18. WELCOME coupon
    # ------------------------------------------------
    def test_welcome_coupon(self):

        products = [
            {
                "product_id": "P017",
                "category": "Grocery",
                "quantity": 1,
                "unit_price": 2000,
                "in_stock": True,
                "valid": True
            }
        ]

        result = OrderManagement(
            products,
            "WELCOME"
        ).process_order()

        self.assertGreater(
            result["coupon_discount"],
            0
        )


    # ------------------------------------------------
    # 19. Empty order
    # ------------------------------------------------
    def test_empty_order(self):

        result = OrderManagement([]).process_order()

        self.assertEqual(
            result["status"],
            "REJECTED"
        )


    # ------------------------------------------------
    # 20. Final amount calculation
    # ------------------------------------------------
    def test_final_amount(self):

        products = [
            {
                "product_id": "P018",
                "category": "Electronics",
                "quantity": 1,
                "unit_price": 1000,
                "in_stock": True,
                "valid": True
            }
        ]

        result = OrderManagement(products).process_order()

        expected = (
            result["subtotal"]
            - result["category_discount"]
            - result["coupon_discount"]
            - result["bulk_discount"]
            + result["gst"]
            + result["shipping"]
        )

        self.assertAlmostEqual(
            result["final_amount"],
            expected,
            places=2
        )


if __name__ == "__main__":

    print("\n======================================")
    print(" E-COMMERCE ORDER MANAGEMENT - QA")
    print("======================================\n")

    unittest.main(verbosity=2)
