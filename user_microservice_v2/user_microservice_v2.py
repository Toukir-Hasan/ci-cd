from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

# MongoDB connection setup
client = MongoClient("mongodb+srv://Toukir:1234@cluster0.c7fq4ik.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['my_assignment_db']
user_collection = db['user']

class UserV2(Resource):
    def post(self):
        """
        Create a new user (v2) with additional validations or fields.
        """
        user_data = request.get_json()
        if user_collection.find_one({"email": user_data['email']}):
            return {"message": "User already exists"}, 400
        
        # Additional field checks or default values can be added here
        user_data.setdefault("status", "active")  # Example: Adding a default status field
        user_collection.insert_one(user_data)
        return {"message": "User created successfully", "user_id": str(user_data["_id"])}, 201

    def put(self):
        """
        Update user's email or delivery address (v2) with improved validation or handling.
        """
        user_data = request.get_json()
        email = user_data.get('email')
        new_email = user_data.get('new_email')
        new_address = user_data.get('new_delivery_address')

        # Additional validation or logging
        if not email:
            return {"message": "Email is required for update"}, 400

        user = user_collection.find_one({"email": email})
        if not user:
            return {"message": "User not found"}, 404

        update_fields = {}
        if new_email:
            update_fields['email'] = new_email
        if new_address:
            update_fields['delivery_address'] = new_address

        # You could add logging or other logic here for monitoring changes
        user_collection.update_one({"email": email}, {"$set": update_fields})
        return {"message": "User updated successfully with v2"}, 200

# Add the resources with versioned endpoints
api.add_resource(UserV2, '/v2/user')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5002, debug=True)
