from flask import Flask, render_template, redirect, url_for
from flask_socketio import SocketIO, send
from database.db_connector import db_cur, DBConn
from classes.client import Client

app = Flask(__name__)
app.config['SECRET'] = "secret!123"
socketio = SocketIO(app, cors_allowed_origins="*")


@socketio.on('message')
def handle_message(message):
    if message != "User connected!":
        print("Received message: " + message)
        user, data = message.split(": ")
        client = example(data)
        if client:
            send(user + " asked for user " + client.username, broadcast=True)
            for car in client.cars:
                send("car: " + car[0], broadcast=True)
        else:
            send("Specify correct user!", broadcast=True)


@app.route('/')
def index():
    return render_template("index.html")


def prepare_db():
    """Either create database and tables using DBConn().execute(schema_path)
        or just insert sample data with insert_path"""
    schema_path = "database/schema_16112022.sql"
    insert_path = "database/populate_db_16112022.sql"
    # DBConn().execute(schema_path)
    DBConn().execute(insert_path)


def example(username):
    my_client = Client.get_client(username)
    return my_client


if __name__ == "__main__":
    socketio.run(app, host="localhost", allow_unsafe_werkzeug=True)
