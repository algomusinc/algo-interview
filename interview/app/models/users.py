from .cities import City


class User(object):

    def __init__(self, connection, name=None, cities=[]):
        self.connection = connection
        self.cursor = connection.cursor()
        self.name = name
        self.cities = cities

    def bootstrap(self):
        sql = """
        CREATE TABLE IF NOT EXISTS users (
          name VARCHAR(255) UNIQUE
        );
        
        CREATE TABLE IF NOT EXISTS user_cities (
          user_name VARCHAR(255) REFERENCES users(name) ON DELETE CASCADE NOT NULL,
          city_name VARCHAR(255) REFERENCES cities(name) ON DELETE CASCADE NOT NULL
        );
        
        ALTER TABLE user_cities ADD UNIQUE (user_name, city_name);
        """
        self.cursor.execute(sql)

    def _update_user_model(self):
        response = self.cursor.fetchone()
        self.name = response[0]

    def _update_cities_model(self):
        sql = """
        SELECT DISTINCT
          c.name,
          c.temp,
          c.pressure,
          c.humidity
        FROM users u
        INNER JOIN user_cities uc ON uc.user_name = u.name
        INNER JOIN cities c ON c.name = uc.city_name
        WHERE u.name = %(name)s
        """

        parameters = {
            'name': self.name
        }

        self.cursor.execute(sql, parameters)
        response = self.cursor.fetchmany()

        cities = [
            City(
                connection=self.connection,
                name=row[0]
            ) for row in response
        ]

        for city in cities:
            city.get_weather(update=True)

        self.cities = cities

    def create(self):
        sql = """
        INSERT INTO users (
          name
        ) VALUES (
          %(name)s
        )
        RETURNING
          name;
        """

        parameters = {
            'name': self.name
        }

        self.cursor.execute(sql, parameters)
        self._update_user_model()

    def get(self):
        sql = """
        SELECT
          name
        FROM users
        WHERE name=%(name)s
        """

        parameters = {
            'name': self.name
        }

        self.cursor.execute(sql, parameters)
        self._update_user_model()

        sql = """
        SELECT *
        FROM user_cities
        WHERE user_name=%(user_name)s
        """

        parameters = {
            'user_name': self.name
        }

        self.cursor.execute(sql, parameters)
        self._update_cities_model()

    def exists(self):
        sql = """
        SELECT COUNT(1)
        FROM users
        WHERE name=%(name)s
        """

        parameters = {
            'name': self.name
        }

        self.cursor.execute(sql, parameters)
        response = self.cursor.fetchone()

        return response[0] > 0

    def remove_city(self, city):
        sql = """
        DELETE FROM user_cities 
        WHERE user_name=%(user_name)s
          AND city_name=%(city_name)s
        """

        parameters = {
            'user_name': self.name,
            'city_name': city.name
        }

        self.cursor.execute(sql, parameters)
        self._update_cities_model()

    def add_city(self, city):
        sql = """
        INSERT INTO user_cities (
          user_name,
          city_name
        ) VALUES (
          %(user_name)s,
          %(city_name)s
        )
        RETURNING
          user_name,
          city_name
        """

        parameters = {
            'user_name': self.name,
            'city_name': city.name
        }

        self.cursor.execute(sql, parameters)
        self._update_cities_model()

    def __str__(self):
        return "<User: name={name}".format(
            name=self.name
        )

    def to_json(self):
        return {
            'name': self.name,
            'cities': [city.to_json() for city in self.cities]
        }

    def close(self):
        if self.cursor:
            try:
                self.cursor.close()
            except Exception as exc:
                print("Failed to close cursor due to {message}".format(message=exc.message))
