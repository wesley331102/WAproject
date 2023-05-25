from flask import Flask, request, jsonify
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://WebAppGroup12:VPFcc2XiRYgKZeJa@webapp.0lxbxxp.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.db

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

app = Flask(__name__)

@app.route("/theme1/function1", methods=["POST"])
def function1():
    post_data = request.get_json()
    account = post_data.get("account")
    password = post_data.get("password")
    try:
        db.Account.insert_one({"account": account, "password": password})
    except Exception as e:
        print(e)
        return jsonify({"message": "failed"})

    return jsonify({"message": "success"})
    # json1 = {
    #     "res": column1
    # }
    # return jsonify(json1)

if __name__ == '__main__':
    app.run()