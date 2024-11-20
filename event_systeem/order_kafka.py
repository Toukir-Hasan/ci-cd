from kafka import KafkaConsumer
import json
from pymongo import MongoClient

# Initialize Kafka consumer
consumer = KafkaConsumer(
    'user_updates',
    bootstrap_servers=['kafka:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# Connect to MongoDB
client = MongoClient('mongodb+srv://Toukir:1234@cluster0.c7fq4ik.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
order_db = client['my_assignment_db']
order_collection = order_db['order']

# Listen for updates and process them
for message in consumer:
    event = message.value
    old_email = event['old_email']
    user_email = event['new_email']
    delivery_address = event['new_delivery_address']
    
    # Update relevant orders in the order collection
    order_collection.update_many(
        {"user_email": old_email},
        {"$set": {"user_email":user_email,"delivery_address": delivery_address}}
    )
    print("Order database synchronized successfully.")
