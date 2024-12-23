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


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), 400

# generate sitemap with all your endpoints   #what is this
@app.route('/')
def sitemap():
    return generate_sitemap(app), 200


@app.route('/members', methods=['GET'])
def get_all_members():

    members = jackson_family.get_all_members()
    response_body = {
        "Jackson": "world",
        "family": members,
        "age" : "age",
        "lucky_numbers" : []
    }
    return jsonify(response_body), 200

@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    data = jackson_family.get_member(member_id)
    return jsonify({"data": data}), 200
    

@app.route('/members', methods=['POST'])
def add_member():
    data = request.json
    try:
        jackson_family.add_member(data)
        return jsonify({"Message": "member added successfully"}), 201
    except Exception as error:
        return jsonify({error})

@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    member = jackson_family.get_member(member_id)
    if member is None:
        return jsonify({"error": "Member not found"}), 404
    else:
        jackson_family.delete_member(member_id)
        return jsonify({"done": True}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
