"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

john_jackson = {
    "first_name": 'John',
    "age": 33,
    "lucky_numbers": [7,13,12]
}

jane_jackson = {
    "first_name": 'Jane',
    "age": 35,
    "lucky_numbers": [10,14,3]
}

jimmy_jackson =  {
    "first_name": 'Jimmy',
    "age": 5,
    "lucky_numbers": [1]
}

jackson_family.add_member(john_jackson)
jackson_family.add_member(jane_jackson)
jackson_family.add_member(jimmy_jackson)

print('jacksons ---->', jackson_family.get_all_members())

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), 400

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app), 200


@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "Jackson": "world",
        "family": members
    }
    return jsonify(response_body), 200

@app.route('/members', methods=['POST'])
def add_member():
    data = request.json
    jackson_family.add_member(data)
    return jsonify({"Message": "member added successfully"}), 201
    

## elimar ->

#  try:
#     response = requests.get('https://jsonplaceholder.typicode.com/posts/1')
#     response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
#     data = response.json()  # Parse the JSON response
#     print(data)
# except requests.exceptions.RequestException as error:
#     print("Error:", error)
# ##

@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(id):
    member = jackson_family.get_member(id)
    if member in None:
        return jsonify({"error": "Member not found"}), 404
    else:
        jackson_family.delete_member(id)
        return jsonify({"done": True}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
