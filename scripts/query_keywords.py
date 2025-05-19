from pymongo import MongoClient
from dotenv import load_dotenv
import os
from urllib.parse import quote_plus

load_dotenv()
user = os.getenv("MONGODB_USER")
password = os.getenv("MONGODB_PASSWORD")
cluster = os.getenv("MONGODB_CLUSTER")

client = MongoClient(f"mongodb+srv://{user}:{password}@{cluster}/?retryWrites=true&w=majority&appName=Cluster0")
db = client["ecommerce"]  
reviews_col = db["reviews"]

keyword = input("Enter keyword to serach in comments: ").lower()
max_rating = int(input("Enter maximum rating to filter:"))

query = {
    "$and":[
        {"comment":{"$regex":keyword, "$options":"i"}},
        {"rating":{"$lte": max_rating}}
        ]
    }

results = reviews_col.find(
    query,
    {"_id":0, "product_id":1, "user":1, "rating":1, "comment":1}
    )

found = False
for r in results:
    found = True
    print(f"\n product:{r['product_id']} \n user:{r['user']} \n rating:{r['rating']} \n comment:{r['comment']}")

if not found:
    print("No comment found containing that keyword.")