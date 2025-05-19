import json
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

user = os.getenv("MONGODB_USER")
password = os.getenv("MONGODB_PASSWORD")
cluster = os.getenv("MONGODB_CLUSTER")

client = MongoClient(f"mongodb+srv://{user}:{password}@{cluster}/?retryWrites=true&w=majority&appName=Cluster0")

db = client["ecommerce"]  
products_col = db["products"]
reviews_col = db["reviews"]


with open("./data/sample_products.json", "r", encoding="utf-8") as f:
    products = json.load(f)
    products_col.insert_many(products)

with open("./data/sample_reviews.json", "r", encoding="utf-8") as f:
    reviews = json.load(f)
    reviews_col.insert_many(reviews)

print("Data successfully inserted into MongoDB!")
