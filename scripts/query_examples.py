from pymongo import MongoClient
from dotenv import load_dotenv
import os
from urllib.parse import quote_plus
import pandas as pd
import matplotlib.pyplot as plt

load_dotenv()
user = os.getenv("MONGODB_USER")
password = os.getenv("MONGODB_PASSWORD")
cluster = os.getenv("MONGODB_CLUSTER")

client = MongoClient(f"mongodb+srv://{user}:{password}@{cluster}/?retryWrites=true&w=majority&appName=Cluster0")

db = client["ecommerce"]
products_col = db["products"]
reviews_col = db["reviews"]

print("\n All Products:")
for product in products_col.find({}, {"_id":0, "product_id":1, "name":1, "price":1}):
    print(product)

print("\n Reviews for product P0001:")
for review in reviews_col.find({"product_id":"P1001"},{"_id":0, "user":1, "rating":1, "comment":1}):
    print(review)

print("\n Average Rating per Product:")
pipeline = [
    {
        "$group":{
            "_id":"$product_id", 
            "avg_rating":{"$avg":"$rating"},
            "review_count":{"$sum":1}       
        }
    },
    {
        "$sort":{"avg_rating":-1}
    }
]
results = list(reviews_col.aggregate(pipeline))
for result in results:
    print(f"Product {result['_id']} -  Average Rating: {round(result['avg_rating'], 2)}  ({result['review_count']} reviews)")

df = pd.DataFrame(results)
df.rename(columns={"_id": "product_id"}, inplace=True)

csv_path = "data/average_ratings.csv"
df.to_csv(csv_path, index=False)

plt.figure(figsize=(10, 5))
plt.bar(df["product_id"], df["avg_rating"])
plt.xlabel("Product ID")
plt.ylabel("Average Rating")
plt.title("Average Rating per Product")
plt.xticks(rotation=45)
plt.tight_layout()
plt.grid(axis='y')
plt.show()

    