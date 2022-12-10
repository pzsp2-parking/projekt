import json
import random
from flask import Flask, request, jsonify
from datetime import datetime, timedelta, timezone
from flask_jwt_extended import create_access_token, get_jwt, \
                               get_jwt_identity, unset_jwt_cookies, \
                               jwt_required, JWTManager


from classes.account import Client
from classes.car import Car

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "parpa-parpa-parpa"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt = JWTManager(app)


@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            data = response.get_json()
            if type(data) is dict:
                data["access_token"] = access_token
                response.data = json.dumps(data)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original respone
        return response


@app.route('/api/token', methods=["POST"])
def create_token():
    login = request.json.get("login", None)
    password = request.json.get("password", None)

    cli = Client.get_client(login)

    if cli == -1:
        return {"msg": "No account with given login"}, 401
    elif not cli.check_password(password):
        return {"msg": "Wrong password"}, 401

    access_token = create_access_token(identity=login)
    response = {"access_token": access_token}
    return response


@app.route('/api/newAcc', methods=["POST"])
def create_account():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    email = request.json.get("email", None)
    phone_nr = request.json.get("phone_nr", None)

    cli = Client.add_client(username, password, email, phone_nr)

    if cli == -1:
        return {"msg": "Could not create account with given data"}, 401

    access_token = create_access_token(identity=username)
    response = {"access_token": access_token}
    return response


@app.route('/api/addCar', methods=["POST"])
@jwt_required()
def add_car():
    vin = request.json.get("vin", None)
    reg_no = request.json.get("reg_no", None)
    model = request.json.get("model", None)
    brand = request.json.get("brand", None)
    capacity = request.json.get("capacity", None)

    username = get_jwt_identity()
    cli = Client.get_client(username)

    car = Car.add_car(cli, vin, reg_no, model, brand, capacity)

    return {'reg_no': car.reg_no}


@app.route("/api/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response


@app.route('/api/client_data')
@jwt_required()
def get_client_data():
    username = get_jwt_identity()
    cli = Client.get_client(username)
    return {
        'username': cli.username,
        'cars': [{
            'reg_no': car.reg_no,
            'model': car.model,
            'brand': car.brand,
            'parked': random.random() > 0.5  # TODO: Return if car is parked
            } for car in cli.cars]
        }