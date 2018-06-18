from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

users = [
    {
        "name": "Nicholas",
        "amount": 250000,
        "status": "Processing"
    },
    {
        "name": "Ashley",
        "amount": 12000,
        "status": "Approved"
    },
    {
        "name": "Jass",
        "amount": 22,
        "status": "Rejected"
    }
]

class Status(Resource):
    def get(self, name):
        for user in users:
            if(name == user["name"]):
                return user, 200
        return "User not found", 404

    def post(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("amount")
        parser.add_argument("status")
        args = parser.parse_args()

        for user in users:
            if(name == user["name"]):
                return "User with name {} already exists".format(name), 400

        user = {
            "name": name,
            "amount": args["amount"],
            "status": "Pending"
        }
        users.append(user)
        return user, 201

    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("amount")
        parser.add_argument("status")
        args = parser.parse_args()

        for user in users:
            if(name == user["name"]):
                user["amount"] = args["amount"]
                user["status"] = args["status"]
                return user, 200
        
        user = {
            "name": name,
            "amount": args["amount"],
            "status": args["status"]
        }
        users.append(user)
        return user, 201

    def delete(self, name):
        global users
        users = [user for user in users if user["name"] != name]
        return "{} is deleted.".format(name), 200
      
api.add_resource(Status, "/status/<string:name>")

app.run(debug=True)