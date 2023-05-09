'''
Module to preprocess the edges data into meaningful format.
co-purchase.json will be generated 
'''
import json
import os
from tqdm import tqdm

file_names = ["March 02 2003.json", "March 12 2003.json", "May 05 2003.json", "June 01 2003.json"]

products = []

for file_name in tqdm(file_names):
    with open(os.path.join("data",file_name), "r") as f:
        data = json.load(f)

    month = file_name.split()[0]

    product_dict = {}
    for line_dict in tqdm(data):
        from_id = line_dict["From"]
        to_id = line_dict["To"]
        if from_id not in product_dict:
            product_dict[from_id] = []
        product_dict[from_id].append(to_id)

    for product_id, co_purchases in product_dict.items():
        product = {
            "product_id": product_id,
            "co_purchases": co_purchases,
            "Date": file_name.split('.')[0],
            "month": month
        }
        products.append(product)

with open(os.path.join("data","co-purchases.json"), "w") as f:
    json.dump(products, f)
