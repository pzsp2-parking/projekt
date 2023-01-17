import json
from flask import Flask, request, jsonify
from datetime import datetime, timedelta, timezone
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    unset_jwt_cookies,
    jwt_required,
    JWTManager,
)


from classes.account import Client, Employee
from classes.car import Car
from classes.parking import Parking

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


@app.route("/api/token", methods=["POST"])
def create_token():
    login = request.json.get("login", None)
    password = request.json.get("password", None)

    cli = Client.get_client(login)

    if cli == -1:
        emp = Employee.get_employee(login)

        if emp == -1:
            return {"msg": "No account with given login"}, 401
        elif not emp.check_password(password):
            return {"msg": "Wrong password"}, 401

        access_token = create_access_token(identity=login)
        response = {
            "access_token": access_token,
            "account_type": "emp"
        }
        return response
    elif not cli.check_password(password):
        return {"msg": "Wrong password"}, 401

    access_token = create_access_token(identity=login)
    response = {
        "access_token": access_token,
        "account_type": "cli"
    }
    return response


@app.route("/api/newAcc", methods=["POST"])
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


@app.route("/api/addCar", methods=["POST"])
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

    return {"reg_no": car.reg_no}


@app.route("/api/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response


@app.route("/api/client_data")
@jwt_required()
def get_client_data():
    username = get_jwt_identity()
    cli = Client.get_client(username)
    return {
        "username": cli.username,
        "cars": [
            {
                "vin": car.vin,
                "reg_no": car.reg_no,
                "model": car.model,
                "brand": car.brand,
                "parked": car.is_parked(),
            }
            for car in cli.cars
        ],
    }


@app.route("/api/leave", methods=["POST"])
@jwt_required()
def leave():
    vin = request.json.get("vin", None)
    car = Car.get_car(vin)
    car.unpark()
    response = jsonify({"msg": "leave successful"})
    return response


@app.route("/api/park", methods=["POST"])
@jwt_required()
def park():
    vin = request.json.get("vin", None)
    car = Car.get_car(vin)
    charge = request.json.get("currentCharge", None)
    charger = request.json.get("chosenCharger", None)
    leave = request.json.get("leaveDatetime", None)
    leaveDatetime = datetime.strptime(leave, "%Y-%m-%dT%H:%M:%S.%fz")
    leaveDatetime += timedelta(hours=1)
    car.park(charge, charger, leaveDatetime)
    response = jsonify({"msg": "park successful"})
    return response


@app.route("/api/carparks", methods=["POST"])
@jwt_required()
def get_carparks():
    parks = Parking.get_all_parkings()
    return {
        "parks": [
            {
                "id": park.id,
                "address": park.street + " " + park.addr_nr + ", " + park.city,
            }
            for park in parks
        ],
    }


@app.route("/api/changeLeaveDate", methods=["POST"])
@jwt_required()
def changeLeaveDate():
    vin = request.json.get("vin", None)
    car = Car.get_car(vin)
    leave = request.json.get("leaveDate", None)
    leaveDatetime = datetime.strptime(leave, "%Y-%m-%dT%H:%M:%S.%fz")
    leaveDatetime += timedelta(hours=1)
    car.change_departure(leaveDatetime)
    response = jsonify({"msg": "change date successful"})
    return response


@app.route("/api/getDetails", methods=["POST"])
@jwt_required()
def getDetails():
    vin = request.json.get("vin", None)
    car = Car.get_car(vin)
    leaveDatetime = datetime.now() + timedelta(hours=8)
    leaveDatetime -= timedelta(hours=1)
    strDate = leaveDatetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    currCharging = car.get_charging_history(True)
    history = car.get_all_charging_history()
    hist = []
    for key in history.keys():
        hist.append({
            'leave': datetime.strptime(key.split('.')[0], "%Y-%m-%d %H:%M:%S"),
            'records': history[key]
        })
    return {
        "leaveDate": strDate,
        "currCharging": currCharging,
        "history": hist,
    }


@app.route("/api/getCurrCharging", methods=["POST"])
@jwt_required()
def getCurrCharging():
    vin = request.json.get("vin", None)
    car = Car.get_car(vin)
    currCharging = car.get_charging_history(True)
    return {"currCharging": currCharging}


@app.route("/api/getMap", methods=["POST"])
@jwt_required()
def getMap():
    parkId = request.json.get("parkId", None)
    parkMap = Parking.get_parking_map(parkId)
    strParkMap = ''
    for row in parkMap:
        for elem in row:
            strParkMap += str(elem)
        strParkMap += '\n'
    return {"parkMap": strParkMap[:-1]}


@app.route("/api/empData", methods=["POST"])
@jwt_required()
def empData():
    username = get_jwt_identity()
    emp = Employee.get_employee(username)
    park = Parking.get_employee_parking(username)
    cars = park.get_all_cars()

    parkMap = Parking.get_parking_map(emp.parking)
    strParkMap = ''
    for row in parkMap:
        for elem in row:
            strParkMap += str(elem)
        strParkMap += '\n'

    return {
        "parkAddress": park.street + " " + park.addr_nr + ", " + park.city,
        "parkMap": strParkMap[:-1],
        "cars": [
            {
                "vin": car.vin,
                "reg_no": car.reg_no,
                "model": car.model,
                "brand": car.brand,
                "parked": car.is_parked(),
            }
            for car in cars
        ],
    }
