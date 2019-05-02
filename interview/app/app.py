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
    return json.dumps({
        'name': name
    })


@app.route("/users/<user_name>", methods=['GET'])
def get_user(user_name):
    user = User(connection=persistence.connection, name=user_name)
    try:
        user.get()
    except Exception as exc:
        response = app.response_class(
            response=json.dumps({
                'message': "User does not exist"
            }),
            status=400,
            mimetype='application/json'
        )
        return response
    finally:
        user.close()

    response = app.response_class(
        response=json.dumps(user.to_json()),
        status=200,
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
        city.get()
    else:
        city.create()

    try:
        user.add_city(city=city)
    except Exception as exc:
        response = app.response_class(
            response=json.dumps({
                'message': "City already added to user"
            }),
            status=400,
            mimetype='application/json'
        )
        return response
    finally:
        user.close()
        city.close()

    response = app.response_class(
        response=json.dumps(user.to_json()),
        status=201,
        mimetype='application/json'
    )
    return response


if __name__ == '__main__':
    app.run_server(debug=True)
