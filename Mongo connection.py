
import json
from pymongo import MongoClient

client = MongoClient()  # Connect to MongoDB
db = client["dbms"]  # Select the database


data_global = None
# Open the co-purchase adjacency file and read the data
with open("data/March 02 2003.json", "rt") as f:
    data = f.read()
    data_global = json.loads(data)

# Create a dictionary mapping each product ID to a list of co-purchased product IDs
product_dict = {}
for json_element in data_global:
    from_id = json_element["From"]
    to_id = json_element["To"]
    if from_id not in product_dict:
        product_dict[from_id] = []
    product_dict[from_id].append(to_id)

for product_id, co_purchases in product_dict.items():
    product_doc = {
        "product_id": product_id,
        "co_purchases": co_purchases
    }
    db.products.insert_one(product_doc)
    
with open(f"data/updated_adm.json", "w") as out_file:
    json.dump(product_dict, out_file)
