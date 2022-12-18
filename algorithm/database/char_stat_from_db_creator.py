from database.db_connector import db_cur
from classes.charging_station import Charging_station
from classes.charging_car import Charging_car

class Char_stat_from_db_creator():
    @staticmethod
    def get_charging_stations(parking_id):
        charging_stations = []
        stmt = f"SELECT * FROM cars_charging WHERE car_park_id={parking_id};"
        db_cur.execute(stmt)
        char_stat_vals = [car_charg for car_charg in db_cur.fetchall()]
        for char_stat_val in char_stat_vals:
            charge_level, base_charge_level, datetime, departure_datetime, capacity, maximal_power, charger_type, charger_id, car_park_id, car_vin = char_stat_val 
            car = Charging_car(charge_level, base_charge_level,  departure_datetime, capacity, charger_type, maximal_power, car_vin) 
            charging_station = Charging_station(car, charger_id, car_park_id)
            charging_stations.append(charging_station)
        return charging_stations

    @staticmethod
    def get_curr_time():
        stmt2 = "SELECT now()::timestamp;"
        db_cur.execute(stmt2)
        curr_time = db_cur.fetchone()
        return curr_time

