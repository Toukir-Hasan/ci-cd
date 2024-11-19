from flask import Flask, request, jsonify
import random
import json
import requests

app = Flask(__name__)

# Load configuration from file
with open('config.json') as config_file:
    config = json.load(config_file)
    P = config.get('route_percentage', 50)  # Default to 50% if not specified
    print(P)

# Endpoint URLs for v1 and v2
USER_V1_URL = 'http://192.168.0.18:5001/v1/user'
USER_V2_URL = 'http://192.168.0.18:5002/v2/user'

@app.route('/user', methods=['POST', 'PUT'])
def route_user_request():
     # Determine which version to route to based on P
    r= random.randint(1,100)
    if r <= P:
        target_url = USER_V1_URL
        print("Routing to version v1",r)  # Print which version is being used
    else:
        target_url = USER_V2_URL
        print("Routing to version v2",r)  # Print which version is being used

   

    # Forward the request to the chosen version
    response = requests.request(
        method=request.method,
        url=target_url,
        json=request.get_json()
    )

    # Return the response from the target service
    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000, debug=True)
