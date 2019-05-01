import requests


class WeatherApi(object):
    """
    This class is used to interact with the weather API and transform the responses to models.

    Each API call costs $1
    """

    def __init__(self):
        self.api_key = "c2add952037e3da0643849cf22dbecbc"

    def parse_city_from_response(self, response):
        return {
            'name': response['name'],
            'temp': response['main']['temp'],
            'pressure': response['main']['pressure'],
            'humidity': response['main']['humidity']
        }

    def get_weather(self, city):
        response = requests.get(
            url="http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=imperial".format(
                city_name=city.name,
                api_key=self.api_key
            )
        )

        if response.status_code >= 400:
            raise Exception("Failed to get weather for city={city_name} due to {error}".format(
                city_name=city.name,
                error=response.content
            ))

        try:
            city_weather = self.parse_city_from_response(response.json())
        except Exception as exc:
            raise Exception("Failed to parse get weather response to model due to {error}".format(
                error=exc
            ))

        return city_weather
