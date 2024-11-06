from pymongo import MongoClient

def connect_to_mongo(uri, db_name):
    """
    Connect to MongoDB and return the specified database.
    """
    client = MongoClient(uri)
    return client[db_name]

def get_user_data():
    """
    Collect user data from input and return a dictionary.
    """
    user_account_id = input("Enter user account ID: ")
    email = input("Enter email: ")
    delivery_address = input("Enter delivery address: ")
    
    return {
        "user_account_id": user_account_id,
        "email": email,
        "delivery_address": delivery_address
    }

def get_order_data(db):
    """
    Collect order data from input and ensure synchronization with user collection.
    The email and delivery address must match the user data.
    """
    user_collection = db['user']
    
    while True:
        user_email = input("Enter user email: ")
        delivery_address = input("Enter delivery address: ")
        
        # Check if the email exists in the user collection
        user_data = user_collection.find_one({"email": user_email})
        
        if user_data:
            # Check if the provided delivery address matches the stored address
            if user_data["delivery_address"] == delivery_address:
                print("Email and delivery address match the existing data.")
                break
            else:
                print("The provided delivery address does not match the existing one. Please try again.")
        else:
            print("Email not found in user data. Please enter valid email and delivery address.")

    order_id = input("Enter order ID: ")
    items = input("Enter items (comma-separated): ").split(",")
    status = input("Enter order status (under process, shipping, delivered): ")

    return {
        "order_id": order_id,
        "user_email": user_email,
        "delivery_address": delivery_address,
        "items": [item.strip() for item in items],
        "status": status
    }

def insert_data(db):
    """
    Insert user and order data into MongoDB collections and ensure synchronization.
    """
    user_collection = db['user']
    order_collection = db['order']
    
    # Get user and order data from input
    user_data = get_user_data()
    
    # Insert user data (if not exists)
    if not user_collection.find_one({"user_account_id": user_data["user_account_id"]}):
        user_collection.insert_one(user_data)
        print("New user data inserted successfully.")
    else:
        print("User already exists. Skipping user data insertion.")
    
    # Get and insert order data
    order_data = get_order_data(db)
    order_collection.insert_one(order_data)
    print("Order data inserted successfully!")

# Connect to MongoDB and insert data
mongo_uri = "mongodb+srv://Toukir:1234@cluster0.c7fq4ik.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"  # Use MongoDB Atlas URI if connecting to Atlas
db_name = "my_assignment_db"
db = connect_to_mongo(mongo_uri, db_name)
insert_data(db)
