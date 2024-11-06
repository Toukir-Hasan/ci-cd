from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_restful import Api, Resource
from bson import ObjectId




app = Flask(__name__)
api = Api(app)

# MongoDB connection setup
client = MongoClient("mongodb+srv://Toukir:1234@cluster0.c7fq4ik.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['my_assignment_db']
order_collection = db['order']
user_collection = db['user']
# Helper function to convert ObjectId to string
def objectid_to_str(o):
        if isinstance(o, ObjectId):
            return str(o)
        raise TypeError("Object of type ObjectId is not serializable")
    
    
class Order(Resource):
  
    def get(self):
        """
        Get orders based on status.
        """
        status = request.args.get('status')
        orders = list(order_collection.find({"status": status}))
        
        # Iterate over the orders and convert ObjectId to string for each one
        for order in orders:
            # Convert the _id field to a string
            order["_id"] = objectid_to_str(order["_id"])
        
        return jsonify(orders)
       

    def post(self):
        """
        Create a new order.
        """
        order_data = request.get_json()
        
        if not user_collection.find_one({"email": order_data['user_email']}):
            return {"message": "User not found"}, 404
        
        order_collection.insert_one(order_data)
        return {"message": "Order created successfully"}, 201

    def put(self):
        """
        Update order status or email/delivery address.
        """
        order_data = request.get_json()
        order_id = order_data.get("order_id")
        status = order_data.get("status")
        new_email = order_data.get('new_email')
        new_address = order_data.get('new_delivery_address')

        order = order_collection.find_one({"order_id": order_id})
        

        if not order:
            return {"message": "Order not found"}, 404
        
        update_fields = {}
        if status:
            update_fields['status'] = status
        if new_email:
            update_fields['user_email'] = new_email
        if new_address:
            update_fields['delivery_address'] = new_address
            
        
        user_collection.update_one({"email": order['user_email']}, {"$set": {"email": new_email, "delivery_address":new_address}})
        order_collection.update_many({"user_email": order['user_email']}, {"$set": {"user_email": new_email, "delivery_address": new_address}})
        order_collection.update_one({"order_id": order_id}, {"$set": update_fields})
        return {"message": "Order updated successfully"}, 200


api.add_resource(Order, '/order')

if __name__ == '__main__':
    app.run(debug=True)
