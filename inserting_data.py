from pymongo import MongoClient

# Connect to MongoDB (replace <username>, <password>, and <cluster_url> for MongoDB Atlas)
client = MongoClient("mongodb+srv://Toukir:1234@cluster0.c7fq4ik.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")  # For local MongoDB
# For MongoDB Atlas: client = MongoClient("mongodb+srv://<username>:<password>@<cluster_url>")

# Create or access databases and collections
db = client['my_assignment_db']
user_collection = db['user']
order_collection = db['order']

# Sample data for user and order collections
users = [
    {"user_account_id": "user123", "email": "user123@example.com", "delivery_address": "123 Maple St"},
    {"user_account_id": "user456", "email": "user456@example.com", "delivery_address": "456 Oak St"},
]

orders = [
    {"order_id": "order001", "user_email": "user123@example.com", "delivery_address": "123 Maple St", "items": ["item1", "item2"], "status": "under process"},
    {"order_id": "order002", "user_email": "user456@example.com", "delivery_address": "456 Oak St", "items": ["item3", "item4"], "status": "shipping"},
]

# Insert data into the collections
user_collection.insert_many(users)
order_collection.insert_many(orders)

print("Data inserted successfully!")
