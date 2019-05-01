from flask import (
    Flask,
    request
)
import json
from .services.persistence import Persistence
from .models.cities import City
from .models.users import User

app = Flask(__name__)

persistence = Persistence()
City(connection=persistence.connection).bootstrap()
User(connection=persistence.connection).bootstrap()


@app.route("/users", methods=['POST'])
def create_user():
    name = request.get_json()['name']
    return {
        'name': name
    }


@app.route("/users/<user_name>", methods=['GET'])
def get_user(user_name):
    user = User(connection=persistence.connection, name=user_name)
    user.get()
    user.close()

    response = app.response_class(
        response=json.dumps(user.to_json()),
        status=201,
        mimetype='application/json'
    )
    return response


@app.route("/users/<user_name>/cities", methods=['POST'])
def add_city_to_user(user_name):
    city_name = request.get_json()['name']
    user = User(connection=persistence.connection, name=user_name)
    user.get()
    city = City(connection=persistence.connection, name=city_name)
    if city.exists():
        print("exists")
        city.get()
    else:
        print("new")
        city.create()

    user.add_city(city=city)
    user.close()
    city.close()

    response = app.response_class(
        response=json.dumps(user.to_json()),
        status=201,
        mimetype='application/json'
    )
    return response


@app.route("/users/<user_name>/cities/<city_name>", methods=['DELETE'])
def remove_city_from_user(user_name, city_name):
    user = User(connection=persistence.connection, name=user_name)
    city = City(connection=persistence.connection, name=city_name)
    user.remove_city(city=city)
    user.close()
    city.close()

    response = app.response_class(
        response=json.dumps(user.to_json()),
        status=200,
        mimetype='application/json'
    )
    return response

if __name__ == '__main__':
    app.run_server(debug=True)
