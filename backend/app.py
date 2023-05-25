from flask import Flask, request, jsonify
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask_cors import CORS

uri = "mongodb+srv://WebAppGroup12:VPFcc2XiRYgKZeJa@webapp.0lxbxxp.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.db

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

app = Flask(__name__)
CORS(app)

@app.route("/sign_up", methods=["POST"])
def sign_up():
    post_data = request.get_json()
    username = post_data.get("username")
    email = post_data.get("email")
    password = post_data.get("password")
    intro = post_data.get("intro")
    try:
        db.Account.insert_one({"_id": email, "username": username, "password": password, "intro": intro})
    except Exception as e:
        print(e)
        return jsonify({"result": False})

    return jsonify({"result": True})

@app.route("/sign_in", methods=["POST"])
def sign_in():
    post_data = request.get_json()
    email = post_data.get("email")
    password = post_data.get("password")
    try:
        response = db.Account.find_one({"_id": email})
    except Exception as e:
        print(e)
        return jsonify({"result": False, "username": ""})

    if response["password"] == password:
        return jsonify({"result": True, "username": response["username"]})
    else:
        return jsonify({"result": False, "username": ""})

if __name__ == '__main__':
    app.run()