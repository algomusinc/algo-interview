from ..services.weather_api import WeatherApi


class City(object):

    def __init__(self, connection, name=None, temp=None, pressure=None, humidity=None):
        self.connection = connection
        self.cursor = connection.cursor()
        self.name = name
        self.temp = temp
        self.pressure = pressure
        self.humidity = humidity
        self.weather_api = WeatherApi()

    def bootstrap(self):
        sql = """
        CREATE TABLE IF NOT EXISTS cities (
          name VARCHAR(255) UNIQUE,
          temp VARCHAR(255),
          pressure VARCHAR(255),
          humidity VARCHAR(255)
        )
        """
        self.cursor.execute(sql)

    def get_weather(self, update=True):
        response = self.weather_api.get_weather(self)
        self.temp = response['temp']
        self.pressure = response['pressure']
        self.humidity = response['humidity']

        if update:
            self.update()

    def update(self):
        sql = """
        UPDATE cities
        SET temp=%(temp)s,
            pressure=%(pressure)s,
            humidity=%(humidity)s
        WHERE name=%(name)s
        RETURNING
          name,
          temp,
          pressure,
          humidity;
        """

        parameters = {
            'temp': self.temp,
            'pressure': self.pressure,
            'humidity': self.humidity,
            'name': self.name
        }

        self.cursor.execute(sql, parameters)

    def _update_model(self):
        response = self.cursor.fetchone()
        self.name = response[0]
        self.temp = response[1]
        self.pressure = response[2]
        self.humidity = response[3]

    def create(self):
        sql = """
        INSERT INTO cities (
          name,
          temp,
          pressure,
          humidity
        ) VALUES (
          %(name)s,
          %(temp)s,
          %(pressure)s,
          %(humidity)s
        )
        RETURNING 
          name,
          temp,
          pressure,
          humidity;
        """

        parameters = {
            'name': self.name,
            'temp': self.temp,
            'pressure': self.pressure,
            'humidity': self.humidity
        }

        self.cursor.execute(sql, parameters)
        self._update_model()

    def get(self):
        sql = """
        SELECT
          name,
          temp,
          pressure,
          humidity
        FROM cities
        WHERE name=%(name)s
        """

        parameters = {
            'name': self.name
        }

        self.cursor.execute(sql, parameters)
        self._update_model()

    def exists(self):
        sql = """
        SELECT COUNT(1)
        FROM cities
        WHERE name=%(name)s
        """

        parameters = {
            'name': self.name
        }

        self.cursor.execute(sql, parameters)
        response = self.cursor.fetchone()

        return response[0] > 0

    def __str__(self):
        return "<City: name={name}, temp={temp}, pressure={pressure}, humidity={humidity}".format(
            name=self.name,
            temp=self.temp,
            pressure=self.pressure,
            humidity=self.humidity
        )

    def to_json(self):
        return {
            'name': self.name,
            'temp': self.temp,
            'pressure': self.pressure,
            'humidity': self.humidity
        }

    def close(self):
        if self.cursor:
            try:
                self.cursor.close()
            except Exception as exc:
                print("Failed to close cursor due to {message}".format(message=exc.message))