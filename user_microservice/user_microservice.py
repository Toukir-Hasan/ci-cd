from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

# MongoDB connection setup
client = MongoClient("mongodb+srv://Toukir:1234@cluster0.c7fq4ik.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['my_assignment_db']
user_collection = db['user']

class User(Resource):
    def post(self):
        """
        Create a new user.
        """
        user_data = request.get_json()
        if user_collection.find_one({"email": user_data['email']}):
            return {"message": "User already exists"}, 400
        
        user_collection.insert_one(user_data)
        return {"message": "User created successfully,hurray"}, 201

    def put(self):
        """
        Update user's email or delivery address.
        """
        user_data = request.get_json()
        email = user_data.get('email')
        new_email = user_data.get('new_email')
        new_address = user_data.get('new_delivery_address')

        # Find the user by email and update the fields
        user = user_collection.find_one({"email": email})
        if not user:
            return {"message": "User not found"}, 404

        update_fields = {}
        if new_email:
            update_fields['email'] = new_email
        if new_address:
            update_fields['delivery_address'] = new_address
        
        user_collection.update_one({"email": email}, {"$set": update_fields})
        return {"message": "User updated successfully"}, 200


api.add_resource(User, '/v1/user')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5001, debug=True)
