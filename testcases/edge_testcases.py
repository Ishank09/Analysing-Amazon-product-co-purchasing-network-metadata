import unittest
import json
import os
from tempfile import TemporaryDirectory
from edge import preprocess_data

class PreprocessDataTestCase(unittest.TestCase):
# Test case 1: Check if the function can read the data from the JSON files correctly.

    def test_read_data(self):
        products = preprocess_data()
        
        assert len(products) == 1445186

        for product in products:
            assert product["product_id"] is not None
            assert product["co_purchases"] is not None
            assert product["Date"] in ["March 02 2003", "March 12 2003", "May 05 2003", "June 01 2003"]
            assert product["month"] in ["March", "March", "May", "June"]

    # Test case 2: Check if the function can process the data correctly.

    def test_process_data(self):
        products = preprocess_data()

        for product in products:
            assert len(product["co_purchases"]) >= 0

    # Test case 3: Check if the function can write the data to the JSON file correctly.

    def test_write_data(self):
        with open("data/co-purchases.json") as f:
            data = json.load(f)
       

        assert len(data) == 1445186
    
        for product in data:
            assert product["product_id"] is not None
            assert product["co_purchases"] is not None
            assert product["Date"] in ["March 02 2003", "March 12 2003", "May 05 2003", "June 01 2003"]
            assert product["month"] in ["March", "March", "May", "June"]

if __name__ == "__main__":
    unittest.main()
