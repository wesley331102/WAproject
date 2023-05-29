from flask import Flask, request, jsonify
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask_cors import CORS
from bson import ObjectId
from email.mime.multipart import MIMEMultipart
import smtplib
import ssl
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText

load_dotenv()
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
DB_URI = "mongodb+srv://WebAppGroup12:VPFcc2XiRYgKZeJa@webapp.0lxbxxp.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(DB_URI, server_api=ServerApi('1'))
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
    try:
        db.Account.insert_one({
            "_id": email, 
            "username": username, 
            "password": password
        })
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
        if response is None:
            return jsonify({
                "result": False, 
                "username": ""
            })
    except Exception as e:
        print(e)
        return jsonify({
            "result": False, 
            "username": ""
        })

    if response["password"] == password:
        return jsonify({
            "result": True, 
            "username": response["username"]
        })
    else:
        return jsonify({
            "result": False, 
            "username": ""
        })
    
@app.route("/sign_out", methods=["POST"])
def sign_out():
    post_data = request.get_json()
    email = post_data.get("email")
    try:
        db.Account.find_one({"_id": email})
        return jsonify({"result": True})
    except Exception as e:
        print(e)
        return jsonify({"result": False})

@app.route("/post", methods=["POST"])
def post():
    post_data = request.get_json()
    username = post_data.get("username")
    email = post_data.get("email")
    animalname = post_data.get("animalname")
    path = post_data.get("path")
    animal = post_data.get("animal")
    breed = post_data.get("breed")
    gender = post_data.get("gender")
    color = post_data.get("color")
    content = post_data.get("content")
    try:
        db.Post.insert_one({
            "username": username, 
            "email": email, 
            "animalname": animalname, 
            "path": path, 
            "animal": animal, 
            "breed": breed, 
            "gender": gender, 
            "color": color, 
            "content": content
        })
    except Exception as e:
        print(e)
        return jsonify({"result": False})

    return jsonify({"result": True})

@app.route("/search", methods=["GET"])
def search():
    animal = int(request.args.get("animal"))
    breed = request.args.get("breed")
    gender = int(request.args.get("gender"))
    color = request.args.get("color")
    result = list()
    animal_list = [1, 2] if animal == 0 else [animal]
    gender_list = [1, 2] if gender == 0 else [gender]
    try:
        responses = db.Post.find({
            "animal": {"$in": animal_list},
            "breed": {"$regex": breed, '$options' : 'i'},
            "gender": {"$in": gender_list},
            "color": {"$regex": color, '$options' : 'i'}
        })
        for response in responses:
            result.append({
                "pid": str(response["_id"]), 
                "username": response["username"],
                "animalname": response["animalname"],
                "path": response["path"], 
                "animal": response["animal"], 
                "breed": response["breed"], 
                "gender": response["gender"], 
                "color": response["color"], 
                "content": response["content"]
            })
    except Exception as e:
        print(e)
        return jsonify({"result": result})
    return jsonify({"result": result})

@app.route("/accept", methods=["POST"])
def accept():
    post_data = request.get_json()
    email = post_data.get("email")
    pid = post_data.get("pid")
    try:
        response = db.Post.find_one({"_id": ObjectId(pid)})
        if response is None:
            return jsonify({"result": False})
        
        message = "Your case was accepted, please contact {}.".format(email)
        msg = MIMEText(message)
        msg['Subject'] = "Sent from WA project"
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = response["email"]
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp_server:
            smtp_server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp_server.sendmail(EMAIL_ADDRESS, response["email"], msg.as_string())

    except Exception as e:
        print(e)
        return jsonify({"result": False})
    return jsonify({"result": True})

@app.route("/my_post", methods=["POST"])
def my_post():
    post_data = request.get_json()
    email = post_data.get("email")
    result = list()
    try:
        responses = db.Post.find({"email": email})
        for response in responses:
            result.append({
                "pid": str(response["_id"]), 
                "username": response["username"],
                "animalname": response["animalname"], 
                "path": response["path"], 
                "animal": response["animal"], 
                "breed": response["breed"], 
                "gender": response["gender"], 
                "color": response["color"], 
                "content": response["content"]
            })
    except Exception as e:
        print(e)
        return jsonify({"result": result})
    return jsonify({"result": result})

@app.route("/delete", methods=["POST"])
def delete():
    post_data = request.get_json()
    pid = post_data.get("pid")
    try:
        db.Post.delete_one({"_id": ObjectId(pid)})
    except Exception as e:
        print(e)
        return jsonify({"result": False})
    return jsonify({"result": True})

if __name__ == '__main__':
    app.run()