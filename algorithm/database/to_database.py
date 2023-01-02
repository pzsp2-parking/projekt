
from database.db_connector import db_cur, db_conn

class To_database:
    @staticmethod
    def insert_requests(request, expenditure, carpark_id):
        """
        Inserts operator requests to database.

        Args:
            request:        Operator's energy demand.
            expenditure:    Energy used by carpark.
            carpark_id:     Id of the carpark.
        """
        curr_time = To_database.get_curr_time()
        stmt = f"INSERT INTO requests (datetime, request, expenditure, cpa_car_park_id) VALUES ('{curr_time}', {request}, {expenditure}, {carpark_id})"
        db_conn.exec(stmt)

    @staticmethod
    def get_curr_time():
        """
        Gets current time from database.
        """
        stmt2 = "SELECT now()::timestamp;"
        db_cur.execute(stmt2)
        curr_time = db_cur.fetchone()
        return curr_time[0]

    @staticmethod
    def insert_new_charging(stations):
        """
        Inserts charging history of given cars to database.

        Args:
            stations:       List of active charging_stations.
        """
        curr_time = To_database.get_curr_time()
        for station in stations:
            stmt = (
                f"INSERT INTO charging (datetime, base_charge_level, charge_level, departure_datetime, cha_charger_id, car_vin)"
                f"VALUES (\'{curr_time}\', {station.car.start_charge_level}, {station.new_charge_level}, \'{station.car.pickup_time}\',"
                f"{station.charger_id}, \'{station.car.car_vin}\');"
            )
            db_conn.exec(stmt)


