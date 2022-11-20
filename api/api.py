from flask import Flask

from classes.client import Client

app = Flask(__name__)


@app.route('/api/example_client')
def get_example_client():
    my_client = Client.get_client('ola')
    return {
        'username': my_client.username,
        'cars': my_client.cars
        }
