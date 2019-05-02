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
        response = self.cursor.fetchall()

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
        );
        """

        parameters = {
            'name': self.name
        }

        self.cursor.execute(sql, parameters)

    def get(self):
        """
        We already have the name field set, so we just have to get the cities
        """
        if not self.exists():
            raise Exception("User does not exist")

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
