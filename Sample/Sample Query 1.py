from pymongo import MongoClient

# Connect to the MongoDB database
client = MongoClient()
db = client["dbms"]

# Define the input and output collection names
input_collection_name = "co-purchases"
output_collection_name = "co-purchases-with-metadata"

# Define the MongoDB $lookup pipeline
pipeline = [
    {
        "$unwind": "$co_purchases"
    },
    {
        "$lookup": {
            "from": "amazon-metadata",
            "localField": "co_purchases",
            "foreignField": "Id",
            "as": "metadata"
        }
    },
    {
        "$group": {
            "_id": "$product_id",
            "co_purchases": {"$push": "$co_purchases"},
            "metadata": {"$push": "$metadata"}
        }
    },
    {
        "$project": {
            "_id": 0,
            "product_id": "$_id",
            "co_purchases": 1,
            "metadata.Id": 1,
            "metadata.title": 1
        }
    }
]

# Run the MongoDB $lookup operation and store the output in a new collection
db[input_collection_name].aggregate(pipeline, allowDiskUse=True, batchSize=1000).to_collection(output_collection_name)
